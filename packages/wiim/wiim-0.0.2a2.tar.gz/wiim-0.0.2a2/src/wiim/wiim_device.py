from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, List, Optional, cast
from urllib.parse import urlparse

from async_upnp_client.client import UpnpDevice, UpnpService, UpnpStateVariable
from async_upnp_client.exceptions import UpnpConnectionError, UpnpError
from async_upnp_client.utils import async_get_url_relative_to_base

from .consts import (
    LOGGER as SDK_LOGGER, # Use a distinct logger for the SDK
    MANUFACTURER_WIIM,
    UPNP_AV_TRANSPORT_SERVICE_ID,
    UPNP_RENDERING_CONTROL_SERVICE_ID,
    UPNP_WIIM_PLAY_QUEUE_SERVICE_ID, # Custom WiiM service
    DeviceAttribute,
    PlayerAttribute,
    PlayingStatus,
    PlayingMode,
    EqualizerMode,
    LoopMode,
    MuteMode,
    WiimHttpCommand, # Renamed from LinkPlayCommand
)
from .endpoint import WiimApiEndpoint # Renamed
from .exceptions import WiimDeviceException, WiimRequestException # Renamed
from .handler import parse_last_change_event
from .manufacturers import get_info_from_project


if TYPE_CHECKING:
    from aiohttp import ClientSession

EventCallback = Callable[["WiimDevice"], Awaitable[None]]

class WiimDevice:
    """
    Represents a WiiM device, handling state and UPnP/HTTP interactions.
    """
    # pylint: disable=too-many-instance-attributes,too-many-public-methods

    _device_info_properties: dict[DeviceAttribute, str]
    _player_properties: dict[PlayerAttribute, str]

    def __init__(
        self,
        upnp_device: UpnpDevice,
        session: ClientSession,
        http_api_endpoint: WiimApiEndpoint | None = None,
        event_callback: EventCallback | None = None,
    ):
        """Initialize the WiiM device."""
        self.upnp_device = upnp_device
        self._session = session
        self._event_callback = event_callback
        self.logger = SDK_LOGGER # Use the SDK's logger

        self._name: str = upnp_device.friendly_name
        self._udn: str = upnp_device.udn
        self._model_name: str = upnp_device.model_name or "WiiM Device"
        self._manufacturer: str = upnp_device.manufacturer or MANUFACTURER_WIIM
        self._device_type: str = upnp_device.device_type
        self._presentation_url: str | None = upnp_device.presentation_url

        # Services
        self.av_transport: UpnpService | None = None
        self.rendering_control: UpnpService | None = None
        self.play_queue_service: UpnpService | None = None # Custom WiiM service

        # State attributes (will be updated by UPnP events and HTTP polling as fallback)
        self.volume: int = 0
        self.is_muted: bool = False
        self.playing_status: PlayingStatus = PlayingStatus.STOPPED
        self.current_track_info: dict[str, Any] = {} # title, artist, album, album_art_uri, duration, uri
        self.play_mode: PlayingMode = PlayingMode.NETWORK # Default, will be updated
        self.loop_mode: LoopMode = LoopMode.PLAY_IN_ORDER
        self.equalizer_mode: EqualizerMode = EqualizerMode.NONE
        self.current_position: int = 0 # in seconds
        self.current_track_duration: int = 0 # in seconds
        self.next_track_uri: str | None = None

        self._http_api: WiimApiEndpoint | None = http_api_endpoint
        self._device_info_properties = dict.fromkeys(DeviceAttribute.__members__.values(), "")
        self._player_properties = dict.fromkeys(PlayerAttribute.__members__.values(), "")
        self._custom_player_properties = {} # For things like WiiM specific EQ mode

        self._available: bool = True # Internal availability state
        self._cancel_event_renewal: asyncio.TimerHandle | None = None

    async def async_init_services_and_subscribe(self) -> bool:
        """
        Initialize UPnP services and subscribe to events.
        Also fetches initial HTTP status as a baseline.
        Returns True if successful, False otherwise.
        """
        try:
            self.av_transport = self.upnp_device.service(UPNP_AV_TRANSPORT_SERVICE_ID)
            self.rendering_control = self.upnp_device.service(UPNP_RENDERING_CONTROL_SERVICE_ID)
            # Attempt to get the custom PlayQueue service
            self.play_queue_service = self.upnp_device.service(UPNP_WIIM_PLAY_QUEUE_SERVICE_ID)
            if not self.play_queue_service:
                self.logger.warning(
                    "Device %s: Custom PlayQueue service (%s) not found.",
                    self.name, UPNP_WIIM_PLAY_QUEUE_SERVICE_ID
                )

            if not self.av_transport or not self.rendering_control:
                self.logger.error(
                    "Device %s: Missing required UPnP services (AVTransport or RenderingControl).", self.name
                )
                self._available = False
                return False

            # Subscribe to events
            self.upnp_device.client.event_handler.subscribe(
                self.av_transport, self._handle_av_transport_event
            )
            self.upnp_device.client.event_handler.subscribe(
                self.rendering_control, self._handle_rendering_control_event
            )
            if self.play_queue_service:
                self.upnp_device.client.event_handler.subscribe(
                    self.play_queue_service, self._handle_play_queue_event
                )

            # Fetch initial state via HTTP as UPnP might not send all initial states immediately
            await self.async_update_http_status()
            # Then try to get initial state from UPnP LastChange (some devices might not support this well)
            await self._fetch_initial_upnp_states()


            self._available = True
            self.logger.info("Device %s: Successfully initialized services and subscribed to events.", self.name)
            return True

        except UpnpError as err:
            self.logger.error("Device %s: Error initializing UPnP services or subscribing: %s", self.name, err)
            self._available = False
            return False
        except WiimRequestException as err:
            self.logger.error("Device %s: Error fetching initial HTTP status: %s", self.name, err)
            # We can still proceed if UPnP is fine, HTTP is a fallback/enhancement
            return True # Or False if HTTP baseline is critical

    async def _fetch_initial_upnp_states(self):
        """Fetch initial state from UPnP LastChange variables if possible."""
        if self.rendering_control and self.rendering_control.has_state_variable("LastChange"):
            try:
                last_change_xml = await self.rendering_control.async_get_state_variable_value("LastChange")
                if last_change_xml:
                    self._update_state_from_rendering_control_event_data(
                        parse_last_change_event(last_change_xml, self.logger)
                    )
            except UpnpError as e:
                self.logger.debug("Device %s: Could not get initial RenderingControl LastChange: %s", self.name, e)

        if self.av_transport and self.av_transport.has_state_variable("LastChange"):
            try:
                last_change_xml = await self.av_transport.async_get_state_variable_value("LastChange")
                if last_change_xml:
                    self._update_state_from_av_transport_event_data(
                         parse_last_change_event(last_change_xml, self.logger)
                    )
            except UpnpError as e:
                self.logger.debug("Device %s: Could not get initial AVTransport LastChange: %s", self.name, e)
        # Add for PlayQueue if it has LastChange

    async def _renew_subscriptions(self) -> None:
        """Renew UPnP event subscriptions."""
        self.logger.debug("Device %s: Renewing UPnP subscriptions.", self.name)
        try:
            if self.av_transport:
                await self.upnp_device.client.event_handler.async_resubscribe(self.av_transport)
            if self.rendering_control:
                await self.upnp_device.client.event_handler.async_resubscribe(self.rendering_control)
            if self.play_queue_service:
                await self.upnp_device.client.event_handler.async_resubscribe(self.play_queue_service)
        except UpnpError as err:
            self.logger.error("Device %s: Failed to renew subscriptions: %s. Device might become unresponsive.", self.name, err)
            self._available = False # Or attempt re-initialization
            if self._event_callback:
                await self._event_callback(self)


    def _schedule_subscription_renewal(self, timeout: int) -> None:
        """Schedule the next subscription renewal."""
        # Renew slightly before the timeout (e.g., 90% of timeout or timeout - 30s)
        renew_in = max(30, timeout - 60) # Ensure at least 30s, renew 60s before expiry
        self.logger.debug("Device %s: Scheduling next subscription renewal in %s seconds.", self.name, renew_in)
        if self._cancel_event_renewal:
            self._cancel_event_renewal.cancel()
        loop = asyncio.get_event_loop()
        self._cancel_event_renewal = loop.call_later(renew_in, lambda: asyncio.create_task(self._renew_subscriptions()))


    def _handle_av_transport_event(
        self, service: UpnpService, state_variables: List[UpnpStateVariable]
    ) -> None:
        """Handle state variable changes for AVTransport."""
        self.logger.debug("Device %s: AVTransport event: %s", self.name, state_variables)
        changed_vars = {sv.name: sv.value for sv in state_variables if sv.name == "LastChange"}
        if "LastChange" in changed_vars:
            event_data = parse_last_change_event(changed_vars["LastChange"], self.logger)
            self._update_state_from_av_transport_event_data(event_data)

        # SID and Timeout for renewal
        if service.event_subscription_sid and service.event_timeout:
            self._schedule_subscription_renewal(service.event_timeout)

        if self._event_callback:
            asyncio.create_task(self._event_callback(self))

    def _update_state_from_av_transport_event_data(self, event_data: Dict[str, Any]):
        """Update device state based on parsed AVTransport event data."""
        if "TransportState" in event_data:
            state_map = {
                "PLAYING": PlayingStatus.PLAYING,
                "PAUSED_PLAYBACK": PlayingStatus.PAUSED,
                "STOPPED": PlayingStatus.STOPPED,
                "TRANSITIONING": PlayingStatus.LOADING, # Or a more specific buffering state
                "NO_MEDIA_PRESENT": PlayingStatus.STOPPED, # Or IDLE
            }
            self.playing_status = state_map.get(event_data["TransportState"], self.playing_status)

        if "CurrentTrackMetaData" in event_data:
            # This is often DIDL-Lite XML, needs parsing
            # For simplicity, assuming it's parsed into a dict by parse_last_change_event
            meta = event_data["CurrentTrackMetaData"]
            self.current_track_info["title"] = meta.get("title", "Unknown Title")
            self.current_track_info["artist"] = meta.get("artist", "Unknown Artist")
            self.current_track_info["album"] = meta.get("album", "Unknown Album")
            self.current_track_info["album_art_uri"] = self._make_absolute_url(meta.get("albumArtURI"))
            self.current_track_info["uri"] = meta.get("res") # The actual stream URI

        if "CurrentTrackDuration" in event_data:
            self.current_track_duration = self._parse_duration(event_data["CurrentTrackDuration"])
        if "RelativeTimePosition" in event_data: # or AbsoluteTimePosition
            self.current_position = self._parse_duration(event_data["RelativeTimePosition"])

        if "AVTransportURI" in event_data:
            # This can indicate the current source or stream
            # Might need logic to map this URI to a PlayingMode
            pass
        if "NextAVTransportURI" in event_data and event_data["NextAVTransportURI"]:
             self.next_track_uri = event_data["NextAVTransportURI"]
        else:
            self.next_track_uri = None


        # Update player_properties for consistency if needed
        self._player_properties[PlayerAttribute.PLAYING_STATUS] = self.playing_status.value
        self._player_properties[PlayerAttribute.TITLE] = self.current_track_info.get("title", "")
        self._player_properties[PlayerAttribute.ARTIST] = self.current_track_info.get("artist", "")
        self._player_properties[PlayerAttribute.ALBUM] = self.current_track_info.get("album", "")
        self._player_properties[PlayerAttribute.TOTAL_LENGTH] = str(self.current_track_duration * 1000)
        self._player_properties[PlayerAttribute.CURRENT_POSITION] = str(self.current_position * 1000)

        self.logger.debug("Device %s: Updated AVTransport state: Status=%s, Track=%s",
                         self.name, self.playing_status, self.current_track_info.get("title"))


    def _handle_rendering_control_event(
        self, service: UpnpService, state_variables: List[UpnpStateVariable]
    ) -> None:
        """Handle state variable changes for RenderingControl."""
        self.logger.debug("Device %s: RenderingControl event: %s", self.name, state_variables)
        changed_vars = {sv.name: sv.value for sv in state_variables if sv.name == "LastChange"}
        if "LastChange" in changed_vars:
            event_data = parse_last_change_event(changed_vars["LastChange"], self.logger)
            self._update_state_from_rendering_control_event_data(event_data)

        if service.event_subscription_sid and service.event_timeout:
            self._schedule_subscription_renewal(service.event_timeout)

        if self._event_callback:
            asyncio.create_task(self._event_callback(self))

    def _update_state_from_rendering_control_event_data(self, event_data: Dict[str, Any]):
        """Update device state based on parsed RenderingControl event data."""
        if "Volume" in event_data: # Usually per-channel, look for 'Master' or first channel
            vol_data = event_data["Volume"]
            if isinstance(vol_data, list) and vol_data: # List of channel volumes
                master_vol = next((ch_vol for ch_vol in vol_data if ch_vol.get("channel") == "Master"), None)
                if master_vol:
                    self.volume = int(master_vol.get("val", self.volume))
                else: # Fallback to first channel if Master not found
                    self.volume = int(vol_data[0].get("val", self.volume))
            elif isinstance(vol_data, dict) and "val" in vol_data: # Single value
                 self.volume = int(vol_data.get("val", self.volume))


        if "Mute" in event_data:
            mute_data = event_data["Mute"]
            if isinstance(mute_data, list) and mute_data:
                master_mute = next((ch_mute for ch_mute in mute_data if ch_mute.get("channel") == "Master"), None)
                if master_mute:
                    self.is_muted = master_mute.get("val") == "1"
                else:
                    self.is_muted = mute_data[0].get("val") == "1"
            elif isinstance(mute_data, dict) and "val" in mute_data:
                self.is_muted = mute_data.get("val") == "1"

        # Update player_properties for consistency
        self._player_properties[PlayerAttribute.VOLUME] = str(self.volume)
        self._player_properties[PlayerAttribute.MUTED] = MuteMode.MUTED if self.is_muted else MuteMode.UNMUTED

        self.logger.debug("Device %s: Updated RenderingControl state: Volume=%s, Muted=%s",
                         self.name, self.volume, self.is_muted)


    def _handle_play_queue_event(
        self, service: UpnpService, state_variables: List[UpnpStateVariable]
    ) -> None:
        """Handle state variable changes for the custom PlayQueue service."""
        self.logger.debug("Device %s: PlayQueue event: %s", self.name, state_variables)
        # Assuming PlayQueue also uses LastChange or has specific state variables
        # This is speculative as the PlayQueue service is custom.
        # Example:
        # changed_vars = {sv.name: sv.value for sv in state_variables}
        # if "QueueLength" in changed_vars:
        #     self.queue_length = int(changed_vars["QueueLength"])
        # if "CurrentIndex" in changed_vars:
        #     self.current_queue_index = int(changed_vars["CurrentIndex"])
        # if "QueueData" in changed_vars: # This would likely be XML or JSON
        #     self.queue_items = self._parse_queue_data(changed_vars["QueueData"])

        if service.event_subscription_sid and service.event_timeout:
            self._schedule_subscription_renewal(service.event_timeout)

        if self._event_callback:
            asyncio.create_task(self._event_callback(self))

    # --- HTTP API Methods (Fallback and Specific Commands) ---
    async def _http_request(self, command: WiimHttpCommand | str, params: str | None = None) -> dict[str, Any]:
        """Make an HTTP request to the device."""
        if not self._http_api:
            raise WiimDeviceException(f"Device {self.name}: HTTP API endpoint not configured.")
        full_command = command.format(params) if params else command
        try:
            return await self._http_api.json_request(full_command)
        except WiimRequestException as err:
            self.logger.error("Device %s: HTTP request failed for command %s: %s", self.name, full_command, err)
            raise

    async def _http_command_ok(self, command: WiimHttpCommand | str, params: str | None = None) -> None:
        """Make an HTTP request and expect 'OK'."""
        if not self._http_api:
            raise WiimDeviceException(f"Device {self.name}: HTTP API endpoint not configured.")
        full_command = command.format(params) if params else command
        try:
            await self._http_api.request(full_command) # This checks for "OK"
        except WiimRequestException as err:
            self.logger.error("Device %s: HTTP command_ok failed for %s: %s", self.name, full_command, err)
            raise

    async def async_update_http_status(self) -> None:
        """Fetch device and player status via HTTP API."""
        if not self._http_api:
            self.logger.debug("Device %s: No HTTP API, skipping HTTP status update.", self.name)
            return

        try:
            device_data = await self._http_request(WiimHttpCommand.DEVICE_STATUS)
            self._device_info_properties.update(cast(Dict[DeviceAttribute, str], device_data))
            self.logger.debug("Device %s: Fetched HTTP device status: %s", self.name, self._device_info_properties.get(DeviceAttribute.DEVICE_NAME))

            player_data = await self._http_request(WiimHttpCommand.PLAYER_STATUS)
            # TODO: Add fixup_player_properties if still needed from old SDK
            self._player_properties.update(cast(Dict[PlayerAttribute, str], player_data))
            self.logger.debug("Device %s: Fetched HTTP player status: %s", self.name, self._player_properties.get(PlayerAttribute.PLAYING_STATUS))

            # Update internal state from these HTTP properties as a baseline
            # This might be overwritten by more timely UPnP events
            self.volume = int(self._player_properties.get(PlayerAttribute.VOLUME, 0))
            self.is_muted = self._player_properties.get(PlayerAttribute.MUTED) == MuteMode.MUTED
            self.playing_status = PlayingStatus(self._player_properties.get(PlayerAttribute.PLAYING_STATUS, PlayingStatus.STOPPED))
            self.play_mode = PlayingMode(self._player_properties.get(PlayerAttribute.PLAYBACK_MODE, PlayingMode.NETWORK))
            # ... and so on for other relevant properties from player_properties

            # Update name from HTTP if it's different (mDNS might be stale)
            http_name = self._device_info_properties.get(DeviceAttribute.DEVICE_NAME)
            if http_name and http_name != self._name:
                self.logger.info("Device %s: Name updated via HTTP from '%s' to '%s'", self._udn, self._name, http_name)
                self._name = http_name

            # Update manufacturer/model from project ID if available
            project_id = self._device_info_properties.get(DeviceAttribute.PROJECT)
            if project_id:
                manufacturer, model = get_info_from_project(project_id)
                self._manufacturer = manufacturer
                self._model_name = model


        except WiimRequestException as err:
            self.logger.warning("Device %s: Failed to update status via HTTP: %s", self.name, err)
            # Don't mark as unavailable solely due to HTTP failure if UPnP is active
        except ValueError as err: # For Enum conversions
            self.logger.warning("Device %s: Error parsing HTTP status data: %s", self.name, err)


    # --- UPnP Control Actions ---
    async def _invoke_upnp_action(self, service_name: str, action_name: str, **kwargs) -> dict:
        """Helper to invoke a UPnP action."""
        service: UpnpService | None = None
        if service_name == "AVTransport" and self.av_transport:
            service = self.av_transport
        elif service_name == "RenderingControl" and self.rendering_control:
            service = self.rendering_control
        elif service_name == "PlayQueue" and self.play_queue_service:
            service = self.play_queue_service
        else:
            raise WiimDeviceException(f"Device {self.name}: Unknown or unavailable service {service_name}")

        if not service.has_action(action_name):
            raise WiimDeviceException(f"Device {self.name}: Service {service_name} has no action {action_name}")

        action = service.action(action_name)
        try:
            self.logger.debug("Device %s: Invoking UPnP Action %s.%s with %s", self.name, service_name, action_name, kwargs)
            # Default InstanceID to 0 if not provided, common for AVTransport/RenderingControl
            if "InstanceID" not in kwargs:
                kwargs["InstanceID"] = 0
            result = await action.async_call(**kwargs)
            self.logger.debug("Device %s: UPnP Action %s.%s result: %s", self.name, service_name, action_name, result)
            return result
        except UpnpError as err:
            self.logger.error("Device %s: UPnP action %s.%s failed: %s", self.name, service_name, action_name, err)
            raise WiimDeviceException(f"UPnP action {action_name} failed: {err}") from err

    async def async_play(self, uri: str | None = None, metadata: str | None = None) -> None:
        """
        Start playback. If URI is provided, plays that URI. Otherwise, resumes.
        Metadata is typically DIDL-Lite XML string.
        """
        if uri:
            await self._invoke_upnp_action(
                "AVTransport",
                "SetAVTransportURI",
                CurrentURI=uri,
                CurrentURIMetaData=metadata or "", # DIDL-Lite for metadata
            )
            # After setting URI, explicitly call Play
            await self._invoke_upnp_action("AVTransport", "Play", Speed="1")
        else:
            await self._invoke_upnp_action("AVTransport", "Play", Speed="1")
        self.playing_status = PlayingStatus.PLAYING # Optimistic update

    async def async_pause(self) -> None:
        """Pause playback."""
        await self._invoke_upnp_action("AVTransport", "Pause")
        self.playing_status = PlayingStatus.PAUSED # Optimistic update

    async def async_stop(self) -> None:
        """Stop playback."""
        await self._invoke_upnp_action("AVTransport", "Stop")
        self.playing_status = PlayingStatus.STOPPED # Optimistic update

    async def async_next(self) -> None:
        """Play next track."""
        await self._invoke_upnp_action("AVTransport", "Next")

    async def async_previous(self) -> None:
        """Play previous track."""
        await self._invoke_upnp_action("AVTransport", "Previous")

    async def async_seek(self, position_seconds: int) -> None:
        """Seek to a position in the current track (in seconds)."""
        time_str = self._format_duration(position_seconds)
        # 'REL_TIME' for relative, 'TRACK_NR' for track number (usually 1 for current)
        await self._invoke_upnp_action("AVTransport", "Seek", Unit="REL_TIME", Target=time_str)

    async def async_set_volume(self, volume_percent: int) -> None:
        """Set volume (0-100)."""
        if not 0 <= volume_percent <= 100:
            raise ValueError("Volume must be between 0 and 100")
        await self._invoke_upnp_action(
            "RenderingControl",
            "SetVolume",
            Channel="Master",
            DesiredVolume=volume_percent,
        )
        self.volume = volume_percent # Optimistic update

    async def async_set_mute(self, mute: bool) -> None:
        """Set mute state."""
        await self._invoke_upnp_action(
            "RenderingControl",
            "SetMute",
            Channel="Master",
            DesiredMute=1 if mute else 0,
        )
        self.is_muted = mute # Optimistic update

    async def async_set_play_mode(self, mode: PlayingMode) -> None:
        """
        Set the playback source/mode.
        This is often device-specific. UPnP standard way is SetAVTransportURI.
        WiiM devices might use HTTP commands for this more reliably.
        """
        # Try HTTP first if it's a known WiiM mode
        # PLAY_MODE_SEND_MAP_HTTP = { ... } # Map PlayingMode to HTTP command parameter
        # http_mode_val = PLAY_MODE_SEND_MAP_HTTP.get(mode)
        # if http_mode_val and self._http_api:
        #    try:
        #        await self._http_command_ok(WiimHttpCommand.SWITCH_MODE, http_mode_val)
        #        self.play_mode = mode
        #        return
        #    except WiimRequestException as e:
        #        self.logger.warning("Failed to set play mode via HTTP, falling back if possible: %s", e)

        # Fallback/General UPnP approach (might not work for all sources):
        # This would involve setting a specific URI for line-in, bluetooth, etc.
        # These URIs are highly device-specific. e.g., "x-rincon-stream:<UDN>" for Sonos line-in
        # For WiiM, check PDF or sniff traffic for these special URIs.
        # If mode is e.g. PlayingMode.LINE_IN, find the URI for line-in.
        # await self.async_play(uri_for_line_in, metadata_for_line_in)
        self.logger.warning("Device %s: async_set_play_mode via UPnP is highly device-specific and not fully implemented. Use HTTP for reliability.", self.name)
        # For now, just update optimistically if HTTP was used or if we assume it worked
        if self._http_api: # Assuming it was attempted via HTTP earlier or should be
             self.play_mode = mode
        # No standard UPnP action for "Switch Mode" directly.
        # It's usually done by setting AVTransportURI to a special value.

    async def async_set_loop_mode(self, loop: LoopMode) -> None:
        """Set loop/repeat mode using UPnP."""
        # UPnP standard: "NORMAL", "REPEAT_ONE", "REPEAT_ALL", "RANDOM", "SHUFFLE_NOREPEAT", "SHUFFLE_REPEAT_ONE"
        # Map our LoopMode to UPnP PlayMode
        upnp_play_mode_map = {
            LoopMode.PLAY_IN_ORDER: "NORMAL",
            LoopMode.CONTINUOUS_PLAYBACK: "REPEAT_ALL", # Or REPEAT_TRACKS
            LoopMode.CONTINOUS_PLAY_ONE_SONG: "REPEAT_ONE", # Or REPEAT_TRACK
            LoopMode.RANDOM_PLAYBACK: "SHUFFLE_NOREPEAT", # Or just SHUFFLE / RANDOM
            LoopMode.LIST_CYCLE: "REPEAT_ALL", # Closest match
            # Add others if needed
        }
        upnp_mode = upnp_play_mode_map.get(loop, "NORMAL")
        await self._invoke_upnp_action("AVTransport", "SetPlayMode", NewPlayMode=upnp_mode)
        self.loop_mode = loop # Optimistic

    async def async_set_equalizer_mode(self, eq_mode: EqualizerMode) -> None:
        """Set equalizer mode. This is typically non-standard UPnP."""
        # WiiM uses HTTP commands for this
        if self.manufacturer == MANUFACTURER_WIIM and self._http_api:
            try:
                if eq_mode == EqualizerMode.NONE:
                    await self._http_command_ok(WiimHttpCommand.WIIM_EQUALIZER_OFF)
                else:
                    # Ensure eq_mode.value matches what WIIM_EQ_LOAD expects
                    await self._http_command_ok(WiimHttpCommand.WIIM_EQ_LOAD, eq_mode.value)
                self.equalizer_mode = eq_mode
                self._custom_player_properties[PlayerAttribute.EQUALIZER_MODE] = eq_mode.value
                return
            except WiimRequestException as e:
                self.logger.error("Device %s: Failed to set WiiM EQ mode via HTTP: %s", self.name, e)
                raise
        self.logger.warning("Device %s: Set equalizer mode not supported or HTTP API unavailable.", self.name)


    # --- PlayQueue Service (Custom WiiM service - speculative) ---
    async def async_get_queue_items(self) -> list:
        """Get items from the PlayQueue service (speculative)."""
        if not self.play_queue_service:
            self.logger.warning("Device %s: PlayQueue service not available.", self.name)
            return []
        try:
            # Action name and parameters are guesses
            result = await self._invoke_upnp_action("PlayQueue", "GetQueue", QueueID=0, StartingIndex=0, RequestedCount=100)
            # Parse result["QueueData"] (e.g., XML or JSON string)
            return self._parse_queue_data(result.get("QueueData", ""))
        except WiimDeviceException:
            return [] # Or re-raise

    def _parse_queue_data(self, queue_data_str: str) -> list:
        """Parse queue data from PlayQueue service (needs actual format)."""
        # This is highly dependent on the format WiiM uses.
        # If it's XML (like DIDL-Lite), use an XML parser.
        # If it's JSON, use json.loads().
        self.logger.debug("Device %s: Parsing queue data: %s", self.name, queue_data_str[:100]) # Log snippet
        # Placeholder:
        if not queue_data_str:
            return []
        try:
            # Example if it were simple JSON list of dicts:
            # import json
            # return json.loads(queue_data_str)
            # Or if DIDL-Lite, use a proper parser
            return [{"title": "Queue item (parsing needed)"}]
        except Exception as e:
            self.logger.error("Device %s: Failed to parse queue data: %s", self.name, e)
            return []


    # --- Properties ---
    @property
    def name(self) -> str:
        """Return the name of the device."""
        # Prefer HTTP name if available and different, otherwise UPnP friendly name
        http_name = self._device_info_properties.get(DeviceAttribute.DEVICE_NAME)
        return http_name or self._name

    @property
    def udn(self) -> str:
        """Return the UDN (Unique Device Name) of the device."""
        return self._udn

    @property
    def model_name(self) -> str:
        """Return the model name of the device."""
        # Prefer HTTP derived model if available
        project_id = self._device_info_properties.get(DeviceAttribute.PROJECT)
        if project_id:
            _, model = get_info_from_project(project_id)
            if model != "WiiM": # Generic fallback
                return model
        return self.upnp_device.model_name or "WiiM Device"

    @property
    def firmware_version(self) -> str | None:
        """Return the firmware version from HTTP API."""
        return self._device_info_properties.get(DeviceAttribute.FIRMWARE)

    @property
    def ip_address(self) -> str | None:
        """Return the IP address of the device."""
        if self.upnp_device.device_url:
            return urlparse(self.upnp_device.device_url).hostname
        return None
    
    @property
    def http_api_url(self) -> str | None:
        """Return the base URL for the HTTP API if configured."""
        return str(self._http_api) if self._http_api else None

    @property
    def available(self) -> bool:
        """Return True if the device is considered available."""
        return self._available and self.upnp_device.available

    @property
    def album_art_uri(self) -> str | None:
        """Return the current track's album art URI."""
        return self.current_track_info.get("album_art_uri")


    # --- Utility Methods ---
    def _parse_duration(self, time_str: str) -> int:
        """Parse HH:MM:SS or HH:MM:SS.mmm duration string to seconds."""
        if not time_str: return 0
        parts = time_str.split('.')[0].split(':')
        if len(parts) == 3:
            try:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            except ValueError:
                return 0
        return 0

    def _format_duration(self, seconds: int) -> str:
        """Format seconds into HH:MM:SS string."""
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"

    def _make_absolute_url(self, relative_url: str | None) -> str | None:
        """Convert a relative URL from UPnP metadata to an absolute one."""
        if not relative_url:
            return None
        if self.upnp_device.device_url:
            return async_get_url_relative_to_base(self.upnp_device.device_url, relative_url)
        return relative_url # Or try to construct if presentation_url is available

    async def disconnect(self) -> None:
        """Clean up resources, unsubscribe from events."""
        self.logger.info("Device %s: Disconnecting...", self.name)
        if self._cancel_event_renewal:
            self._cancel_event_renewal.cancel()
            self._cancel_event_renewal = None
        try:
            if self.upnp_device.client.event_handler:
                if self.av_transport:
                    await self.upnp_device.client.event_handler.async_unsubscribe(self.av_transport)
                if self.rendering_control:
                    await self.upnp_device.client.event_handler.async_unsubscribe(self.rendering_control)
                if self.play_queue_service:
                    await self.upnp_device.client.event_handler.async_unsubscribe(self.play_queue_service)
        except UpnpError as err:
            self.logger.warning("Device %s: Error during UPnP unsubscribe: %s", self.name, err)
        except Exception as err: # pylint: disable=broad-except
            self.logger.error("Device %s: Unexpected error during disconnect: %s", self.name, err, exc_info=True)
        self._available = False
