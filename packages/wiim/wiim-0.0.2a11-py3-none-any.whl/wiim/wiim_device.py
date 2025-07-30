# wiim/wiim_device.py
from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, List, Optional, cast
from urllib.parse import urlparse, urljoin # MODIFIED: Added urljoin

from async_upnp_client.client import UpnpDevice, UpnpService, UpnpStateVariable
from async_upnp_client.exceptions import UpnpConnectionError, UpnpError
from async_upnp_client.event_handler import UpnpEventHandler
# from async_upnp_client.utils import async_get_url_relative_to_base # REMOVED: This was causing ImportError
from async_upnp_client.aiohttp import AiohttpNotifyServer 

from .consts import (
    SDK_LOGGER,
    MANUFACTURER_WIIM,
    UPNP_AV_TRANSPORT_SERVICE_ID,
    UPNP_RENDERING_CONTROL_SERVICE_ID,
    UPNP_WIIM_PLAY_QUEUE_SERVICE_ID,
    DeviceAttribute,
    PlayerAttribute,
    PlayingStatus,
    PlayingMode,
    EqualizerMode,
    LoopMode,
    MuteMode,
    WiimHttpCommand,
)
from .endpoint import WiimApiEndpoint
from .exceptions import WiimDeviceException, WiimRequestException
from .handler import parse_last_change_event
from .manufacturers import get_info_from_project


if TYPE_CHECKING:
    from aiohttp import ClientSession
    from async_upnp_client.client import UpnpRequester

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
        self.logger = SDK_LOGGER

        self._name: str = upnp_device.friendly_name
        self._udn: str = upnp_device.udn
        self._model_name: str = upnp_device.model_name or "WiiM Device"
        self._manufacturer: str = upnp_device.manufacturer or MANUFACTURER_WIIM
        self._device_type: str = upnp_device.device_type
        self._presentation_url: str | None = upnp_device.presentation_url

        self.av_transport: UpnpService | None = None
        self.rendering_control: UpnpService | None = None
        self.play_queue_service: UpnpService | None = None

        # Initialize UPnP event handler
        self._notify_server: AiohttpNotifyServer | None = None
        self._event_handler: UpnpEventHandler | None = None
        
        if hasattr(self.upnp_device, 'requester') and self.upnp_device.requester:
            # Create a notify server for the event handler
            # The AiohttpNotifyServer needs the requester's source_ip and a free port.
            # It also needs the asyncio loop.
            try:
                loop = asyncio.get_event_loop()
                self._notify_server = AiohttpNotifyServer(
                    requester=self.upnp_device.requester, # type: ignore
                    source_ip=self.upnp_device.requester.source_ip, # type: ignore
                    loop=loop
                )
                # Now create the event handler with the notify server
                self._event_handler = UpnpEventHandler(
                    notify_server=self._notify_server,
                    requester=self.upnp_device.requester # type: ignore
                )
                self.logger.debug("Device %s: UpnpEventHandler and AiohttpNotifyServer initialized.", self.name)
            except Exception as e:
                self.logger.error(
                    "Device %s: Failed to initialize AiohttpNotifyServer or UpnpEventHandler: %s. Eventing will be disabled.",
                    self.name, e, exc_info=True
                )
                self._notify_server = None # Ensure it's None if init fails
                self._event_handler = None
        else:
            self.logger.error(
                "Device %s: UpnpDevice has no requester. Eventing will not be available.",
                self.name
            )

        self.volume: int = 0
        self.is_muted: bool = False
        self.playing_status: PlayingStatus = PlayingStatus.STOPPED
        self.current_track_info: dict[str, Any] = {}
        self.play_mode: PlayingMode = PlayingMode.NETWORK
        self.loop_mode: LoopMode = LoopMode.PLAY_IN_ORDER
        self.equalizer_mode: EqualizerMode = EqualizerMode.NONE
        self.current_position: int = 0
        self.current_track_duration: int = 0
        self.next_track_uri: str | None = None

        self._http_api: WiimApiEndpoint | None = http_api_endpoint
        self._device_info_properties = dict.fromkeys(DeviceAttribute.__members__.values(), "")
        self._player_properties = dict.fromkeys(PlayerAttribute.__members__.values(), "")
        self._custom_player_properties = {}

        self._available: bool = True
        self._cancel_event_renewal: asyncio.TimerHandle | None = None
        self._event_handler_started: bool = False

    async def async_init_services_and_subscribe(self) -> bool:
        """
        Initialize UPnP services and subscribe to events.
        Also fetches initial HTTP status as a baseline.
        Returns True if successful, False otherwise.
        """
        try:
            # self.logger.error("Available service types: %s", list(self.upnp_device.services.keys()))

            self.av_transport = self.upnp_device.service(UPNP_AV_TRANSPORT_SERVICE_ID)
            self.rendering_control = self.upnp_device.service(UPNP_RENDERING_CONTROL_SERVICE_ID)
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
                # self._available = False
                # return False
            
            # Subscribe to events if services and event handler are available
            if self._event_handler and self.av_transport and self.rendering_control:
                if self._event_handler and self._notify_server: # Check both are initialized
                    if not self._event_handler_started:
                        try:
                            # Start the notify server first, then the event handler (if it has its own start)
                            await self._notify_server.async_start()
                            # UpnpEventHandler itself doesn't have an async_start, it uses the notify_server's start
                            self._event_handler_started = True
                            self.logger.info("Device %s: AiohttpNotifyServer for UPnP events started at: %s",
                                            self.name, self._notify_server.callback_url)
                        except Exception as e:
                            self.logger.error("Device %s: Failed to start AiohttpNotifyServer: %s", self.name, e, exc_info=True)
                            self._event_handler_started = False # Ensure flag is false
                    
                    if self._event_handler_started:
                        if self.av_transport:
                            await self._event_handler.async_subscribe(self.av_transport, self._handle_av_transport_event)
                        if self.rendering_control:
                            await self._event_handler.async_subscribe(self.rendering_control, self._handle_rendering_control_event)
                        if self.play_queue_service: # Only subscribe if service exists
                            await self._event_handler.async_subscribe(self.play_queue_service, self._handle_play_queue_event)
                        self.logger.info("Device %s: Subscribed to available UPnP service events.", self.name)
                    else:
                        self.logger.warning("Device %s: Notify server not started, cannot subscribe to service events.", self.name)
                elif not self._event_handler: # If _event_handler is None due to init failure
                    self.logger.warning("Device %s: No event handler (init failed), cannot subscribe to service events.", self.name)

            await self.async_update_http_status()
            # Then try to get initial state from UPnP LastChange (some devices might not support this well)
            if self._event_handler_started: # Only if eventing is up
                await self._fetch_initial_upnp_states()

            self._available = True
            self.logger.info("Device %s: Successfully initialized services and subscribed to events.", self.name)
            return True

        except UpnpError as err: # Errors during service discovery or initial UPnP state fetch
            self.logger.error("Device %s: Error initializing UPnP aspects: %s", self.name, err)
            # If UPnP part fails, HTTP might still work.
            # self._available = False # Decide if this makes the whole device unavailable
            # For now, let HTTP status determine availability if UPnP init fails.
            # If async_update_http_status also fails, then it's truly not ready.
            try:
                await self.async_update_http_status() # Check if HTTP is okay
                self._available = True # HTTP is okay
                return True # Degraded mode (HTTP only)
            except WiimRequestException:
                self._available = False # Both UPnP and HTTP failed
                return False
        except WiimRequestException as err: # Errors from async_update_http_status
            self.logger.error("Device %s: Error fetching initial HTTP status: %s", self.name, err)
            self._available = False
            return False
        except Exception as err: # Catch any other unexpected error during init
            self.logger.error("Device %s: Unexpected error during async_init_services_and_subscribe: %s", self.name, err, exc_info=True)
            self._available = False
            return False

    async def _fetch_initial_upnp_states(self):
        """Fetch initial state from UPnP LastChange variables if possible."""
        if self.rendering_control and self.rendering_control.has_state_variable("LastChange"):
            try:
                last_change_xml = await self.rendering_control.async_get_state_variable_value("LastChange")
                if last_change_xml:
                    self._update_state_from_rendering_control_event_data(
                        parse_last_change_event(str(last_change_xml), self.logger) # Ensure string
                    )
            except UpnpError as e:
                self.logger.debug("Device %s: Could not get initial RenderingControl LastChange: %s", self.name, e)

        if self.av_transport and self.av_transport.has_state_variable("LastChange"):
            try:
                last_change_xml = await self.av_transport.async_get_state_variable_value("LastChange")
                if last_change_xml:
                    self._update_state_from_av_transport_event_data(
                         parse_last_change_event(str(last_change_xml), self.logger) # Ensure string
                    )
            except UpnpError as e:
                self.logger.debug("Device %s: Could not get initial AVTransport LastChange: %s", self.name, e)

    async def _renew_subscriptions(self) -> None:
        """Renew UPnP event subscriptions."""
        if not self._event_handler or not self._event_handler_started:
            self.logger.warning("Device %s: Event handler not available or not started, cannot renew subscriptions.", self.name)
            self._available = False 
            if self._event_callback: await self._event_callback(self)
            return

        self.logger.debug("Device %s: Renewing UPnP subscriptions.", self.name)
        try:
            # Resubscribe only if the service object exists
            if self.av_transport:
                await self._event_handler.async_resubscribe(self.av_transport)
            if self.rendering_control:
                await self._event_handler.async_resubscribe(self.rendering_control)
            if self.play_queue_service:
                await self._event_handler.async_resubscribe(self.play_queue_service)
            self.logger.info("Device %s: Successfully renewed UPnP subscriptions.", self.name)
        except UpnpError as err:
            self.logger.error("Device %s: Failed to renew subscriptions: %s. Device might become unresponsive.", self.name, err)
            self._available = False 
            if self._event_callback:
                await self._event_callback(self) 
        except Exception as err: 
            self.logger.error("Device %s: Unexpected error during subscription renewal: %s", self.name, err, exc_info=True)
            self._available = False
            if self._event_callback:
                await self._event_callback(self)

    def _schedule_subscription_renewal(self, timeout: int) -> None:
        """Schedule the next subscription renewal."""
        renew_in = max(30, timeout - 60)
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
        if "LastChange" in changed_vars and changed_vars["LastChange"] is not None:
            event_data = parse_last_change_event(str(changed_vars["LastChange"]), self.logger)
            self._update_state_from_av_transport_event_data(event_data)

        if service.event_subscription_sid and service.event_timeout:
            self._schedule_subscription_renewal(service.event_timeout)
        elif self.logger.isEnabledFor(logging.DEBUG): # Log if details are missing, but this might be normal before first successful sub
             self.logger.debug("Device %s: AVTransport service SID or Timeout not yet available for renewal scheduling.", self.name)

        if self._event_callback:
            asyncio.create_task(self._event_callback(self))

    def _update_state_from_av_transport_event_data(self, event_data: Dict[str, Any]):
        """Update device state based on parsed AVTransport event data."""
        if "TransportState" in event_data:
            state_map = {
                "PLAYING": PlayingStatus.PLAYING,
                "PAUSED_PLAYBACK": PlayingStatus.PAUSED,
                "STOPPED": PlayingStatus.STOPPED,
                "TRANSITIONING": PlayingStatus.LOADING,
                "NO_MEDIA_PRESENT": PlayingStatus.STOPPED,
            }
            self.playing_status = state_map.get(event_data["TransportState"], self.playing_status)

        if "CurrentTrackMetaData" in event_data:
            meta = event_data["CurrentTrackMetaData"]
            if isinstance(meta, dict): # Ensure meta is a dict after parsing
                self.current_track_info["title"] = meta.get("title", "Unknown Title")
                self.current_track_info["artist"] = meta.get("artist", "Unknown Artist")
                self.current_track_info["album"] = meta.get("album", "Unknown Album")
                self.current_track_info["album_art_uri"] = self._make_absolute_url(meta.get("albumArtURI"))
                self.current_track_info["uri"] = meta.get("res")

        if "CurrentTrackDuration" in event_data:
            self.current_track_duration = self._parse_duration(event_data["CurrentTrackDuration"])
        if "RelativeTimePosition" in event_data:
            self.current_position = self._parse_duration(event_data["RelativeTimePosition"])

        if "NextAVTransportURI" in event_data and event_data["NextAVTransportURI"]:
             self.next_track_uri = event_data["NextAVTransportURI"]
        else:
            self.next_track_uri = None

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
        if "LastChange" in changed_vars and changed_vars["LastChange"] is not None:
            event_data = parse_last_change_event(str(changed_vars["LastChange"]), self.logger)
            self._update_state_from_rendering_control_event_data(event_data)

        if service.event_subscription_sid and service.event_timeout:
            self._schedule_subscription_renewal(service.event_timeout)
        elif self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Device %s: RenderingControl service SID or Timeout not yet available for renewal scheduling.", self.name)

        if self._event_callback:
            asyncio.create_task(self._event_callback(self))

    def _update_state_from_rendering_control_event_data(self, event_data: Dict[str, Any]):
        """Update device state based on parsed RenderingControl event data."""
        if "Volume" in event_data:
            vol_data = event_data["Volume"]
            if isinstance(vol_data, list) and vol_data:
                master_vol = next((ch_vol for ch_vol in vol_data if ch_vol.get("channel") == "Master"), None)
                if master_vol and master_vol.get("val") is not None:
                    try: self.volume = int(master_vol.get("val")) 
                    except ValueError: self.logger.warning("Invalid volume value from event: %s", master_vol.get("val"))
                elif vol_data[0].get("val") is not None:
                    try: self.volume = int(vol_data[0].get("val"))
                    except ValueError: self.logger.warning("Invalid volume value from event: %s", vol_data[0].get("val"))
            elif isinstance(vol_data, dict) and vol_data.get("val") is not None:
                 try: self.volume = int(vol_data.get("val"))
                 except ValueError: self.logger.warning("Invalid volume value from event: %s", vol_data.get("val"))

        if "Mute" in event_data:
            mute_data = event_data["Mute"]
            if isinstance(mute_data, list) and mute_data:
                master_mute = next((ch_mute for ch_mute in mute_data if ch_mute.get("channel") == "Master"), None)
                if master_mute and master_mute.get("val") is not None:
                    self.is_muted = master_mute.get("val") == "1"
                elif mute_data[0].get("val") is not None:
                    self.is_muted = mute_data[0].get("val") == "1"
            elif isinstance(mute_data, dict) and mute_data.get("val") is not None:
                self.is_muted = mute_data.get("val") == "1"

        self._player_properties[PlayerAttribute.VOLUME] = str(self.volume)
        self._player_properties[PlayerAttribute.MUTED] = MuteMode.MUTED if self.is_muted else MuteMode.UNMUTED

        self.logger.debug("Device %s: Updated RenderingControl state: Volume=%s, Muted=%s",
                         self.name, self.volume, self.is_muted)


    def _handle_play_queue_event(
        self, service: UpnpService, state_variables: List[UpnpStateVariable]
    ) -> None:
        """Handle state variable changes for the custom PlayQueue service."""
        self.logger.debug("Device %s: PlayQueue event: %s", self.name, state_variables)

        if service.event_subscription_sid and service.event_timeout:
            self._schedule_subscription_renewal(service.event_timeout)
        elif self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug("Device %s: PlayQueue service SID or Timeout not yet available for renewal scheduling.", self.name)

        if self._event_callback:
            asyncio.create_task(self._event_callback(self))

    async def _http_request(self, command: WiimHttpCommand | str, params: str | None = None) -> dict[str, Any]:
        """Make an HTTP request to the device."""
        if not self._http_api:
            raise WiimDeviceException(f"Device {self.name}: HTTP API endpoint not configured.")
        
        # Ensure command is a string for formatting
        cmd_str = command.value if isinstance(command, WiimHttpCommand) else command
        full_command = cmd_str.format(params) if params else cmd_str
        
        try:
            return await self._http_api.json_request(full_command)
        except WiimRequestException as err:
            self.logger.error("Device %s: HTTP request failed for command %s: %s", self.name, full_command, err)
            raise

    async def _http_command_ok(self, command: WiimHttpCommand | str, params: str | None = None) -> None:
        """Make an HTTP request and expect 'OK'."""
        if not self._http_api:
            raise WiimDeviceException(f"Device {self.name}: HTTP API endpoint not configured.")

        cmd_str = command.value if isinstance(command, WiimHttpCommand) else command
        full_command = cmd_str.format(params) if params else cmd_str
        try:
            await self._http_api.request(full_command)
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
            # self.logger.debug("Device %s: Fetched HTTP device status: %s", self.name, self._device_info_properties.get(DeviceAttribute.DEVICE_NAME))

            player_data = await self._http_request(WiimHttpCommand.PLAYER_STATUS)
            self._player_properties.update(cast(Dict[PlayerAttribute, str], player_data))
            # self.logger.debug("Device %s: Fetched HTTP player status: %s", self.name, self._player_properties.get(PlayerAttribute.PLAYING_STATUS))

            # Update internal state from these HTTP properties as a baseline
            # This might be overwritten by more timely UPnP events
            # Only update if value exists in player_data to avoid overwriting with defaults
            if PlayerAttribute.VOLUME in self._player_properties:
                try: self.volume = int(self._player_properties[PlayerAttribute.VOLUME])
                except ValueError: self.logger.warning("Invalid volume in HTTP status: %s", self._player_properties[PlayerAttribute.VOLUME])
            
            if PlayerAttribute.MUTED in self._player_properties:
                self.is_muted = self._player_properties[PlayerAttribute.MUTED] == MuteMode.MUTED
            
            http_playing_status_str = self._player_properties.get(PlayerAttribute.PLAYING_STATUS)
            if http_playing_status_str:
                try:
                    http_playing_status = PlayingStatus(http_playing_status_str)
                    # Prefer UPnP state unless HTTP indicates a significant change from a non-active state
                    if self.playing_status in [PlayingStatus.STOPPED, PlayingStatus.LOADING, None] or \
                       (http_playing_status == PlayingStatus.STOPPED and self.playing_status != PlayingStatus.STOPPED):
                        self.playing_status = http_playing_status
                except ValueError:
                     self.logger.warning("Invalid playing_status in HTTP status: %s", http_playing_status_str)


            http_play_mode_str = self._player_properties.get(PlayerAttribute.PLAYBACK_MODE)
            if http_play_mode_str:
                try: self.play_mode = PlayingMode(http_play_mode_str)
                except ValueError: self.logger.warning("Invalid playback_mode in HTTP status: %s", http_play_mode_str)
            
            http_name = self._device_info_properties.get(DeviceAttribute.DEVICE_NAME)
            if http_name and http_name != self._name:
                self.logger.info("Device %s: Name updated via HTTP from '%s' to '%s'", self._udn, self._name, http_name)
                self._name = http_name

            project_id = self._device_info_properties.get(DeviceAttribute.PROJECT)
            if project_id:
                manufacturer, model = get_info_from_project(project_id)
                self._manufacturer = manufacturer
                self._model_name = model
            
            # If this is the first time we get status, and no UPnP event has fired yet,
            # trigger a callback to HA.
            if self._event_callback: # Ensure callback is set
                 asyncio.create_task(self._event_callback(self))


        except WiimRequestException as err:
            self.logger.warning("Device %s: Failed to update status via HTTP: %s", self.name, err)
            # Don't mark as unavailable solely due to HTTP failure if UPnP is active or expected
            raise # Re-raise to be caught by async_init_services_and_subscribe
        except ValueError as err:
            self.logger.warning("Device %s: Error parsing HTTP status data: %s. Player Data: %s, Device Data: %s", 
                                self.name, err, self._player_properties, self._device_info_properties)
            # Don't raise, but log, as some fields might be okay.


    async def _invoke_upnp_action(self, service_name: str, action_name: str, **kwargs) -> dict:
        """Helper to invoke a UPnP action."""
        service: UpnpService | None = None
        if service_name == "AVTransport" and self.av_transport:
            service = self.av_transport
        elif service_name == "RenderingControl" and self.rendering_control:
            service = self.rendering_control
        elif service_name == "PlayQueue" and self.play_queue_service:
            service = self.play_queue_service
        
        if not service: # Check if service was found and is not None
            raise WiimDeviceException(f"Device {self.name}: Service {service_name} is not available or not initialized.")

        if not hasattr(service, 'has_action') or not service.has_action(action_name):
            raise WiimDeviceException(f"Device {self.name}: Service {service_name} has no action {action_name}")

        action = service.action(action_name)
        try:
            self.logger.debug("Device %s: Invoking UPnP Action %s.%s with %s", self.name, service_name, action_name, kwargs)
            if "InstanceID" not in kwargs:
                kwargs["InstanceID"] = 0
            result = await action.async_call(**kwargs) # type: ignore
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
            # Provide a minimal valid DIDL-Lite if metadata is None, as some renderers require it.
            didl_metadata = metadata or \
                '<DIDL-Lite xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"><item id="0" parentID="-1" restricted="1"><dc:title>Unknown</dc:title><upnp:class>object.item.audioItem.musicTrack</upnp:class></item></DIDL-Lite>'
            await self._invoke_upnp_action(
                "AVTransport",
                "SetAVTransportURI",
                CurrentURI=uri,
                CurrentURIMetaData=didl_metadata,
            )
        await self._invoke_upnp_action("AVTransport", "Play", Speed="1")
        self.playing_status = PlayingStatus.PLAYING

    async def async_pause(self) -> None:
        """Pause playback."""
        await self._invoke_upnp_action("AVTransport", "Pause")
        self.playing_status = PlayingStatus.PAUSED

    async def async_stop(self) -> None:
        """Stop playback."""
        await self._invoke_upnp_action("AVTransport", "Stop")
        self.playing_status = PlayingStatus.STOPPED

    async def async_next(self) -> None:
        """Play next track."""
        await self._invoke_upnp_action("AVTransport", "Next")

    async def async_previous(self) -> None:
        """Play previous track."""
        await self._invoke_upnp_action("AVTransport", "Previous")

    async def async_seek(self, position_seconds: int) -> None:
        """Seek to a position in the current track (in seconds)."""
        time_str = self._format_duration(position_seconds)
        await self._invoke_upnp_action("AVTransport", "Seek", Unit="REL_TIME", Target=time_str)

    async def async_set_volume(self, volume_percent: int) -> None:
        """Set volume (0-100)."""
        if not 0 <= volume_percent <= 100:
            self.logger.warning("Attempted to set volume outside 0-100 range: %s", volume_percent)
            volume_percent = max(0, min(100, volume_percent)) # Clamp value
            # raise ValueError("Volume must be between 0 and 100") # Or clamp
        await self._invoke_upnp_action(
            "RenderingControl",
            "SetVolume",
            Channel="Master",
            DesiredVolume=volume_percent,
        )
        self.volume = volume_percent

    async def async_set_mute(self, mute: bool) -> None:
        """Set mute state."""
        await self._invoke_upnp_action(
            "RenderingControl",
            "SetMute",
            Channel="Master",
            DesiredMute=1 if mute else 0,
        )
        self.is_muted = mute

    async def async_set_play_mode(self, mode: PlayingMode) -> None:
        """Set the playback source/mode using HTTP API."""
        from .consts import PLAY_MODE_HTTP_PARAM_MAP # Import here to avoid circularity if moved from consts
        http_mode_val = PLAY_MODE_HTTP_PARAM_MAP.get(mode)
        if http_mode_val and self._http_api:
            try:
                await self._http_command_ok(WiimHttpCommand.SWITCH_MODE, http_mode_val)
                self.play_mode = mode # Optimistic update
            except WiimRequestException as e:
                self.logger.error("Device %s: Failed to set play mode to %s via HTTP: %s", self.name, mode.value, e)
                raise
        elif not self._http_api:
            self.logger.error("Device %s: HTTP API unavailable, cannot set play mode %s.", self.name, mode.value)
            raise WiimDeviceException(f"HTTP API unavailable to set play mode {mode.value}")
        else: # http_mode_val is None
            self.logger.warning("Device %s: No HTTP command mapping for play mode %s.", self.name, mode.value)
            raise WiimDeviceException(f"Cannot set play mode {mode.value} without HTTP mapping.")


    async def async_set_loop_mode(self, loop: LoopMode) -> None:
        """Set loop/repeat mode using UPnP."""
        upnp_play_mode_map = {
            LoopMode.PLAY_IN_ORDER: "NORMAL",
            LoopMode.CONTINUOUS_PLAYBACK: "REPEAT_ALL",
            LoopMode.CONTINOUS_PLAY_ONE_SONG: "REPEAT_ONE",
            LoopMode.RANDOM_PLAYBACK: "SHUFFLE_NOREPEAT", # Or "SHUFFLE"
            LoopMode.LIST_CYCLE: "REPEAT_ALL",
            LoopMode.SHUFF_DISABLED_REPEAT_DISABLED: "NORMAL",
            LoopMode.SHUFF_ENABLED_REPEAT_ENABLED_LOOP_ONCE: "SHUFFLE", # This implies shuffle all once
        }
        upnp_mode = upnp_play_mode_map.get(loop, "NORMAL")
        await self._invoke_upnp_action("AVTransport", "SetPlayMode", NewPlayMode=upnp_mode)
        self.loop_mode = loop

    async def async_set_equalizer_mode(self, eq_mode: EqualizerMode) -> None:
        """Set equalizer mode using HTTP API."""
        if self.manufacturer == MANUFACTURER_WIIM and self._http_api:
            try:
                if eq_mode == EqualizerMode.NONE:
                    await self._http_command_ok(WiimHttpCommand.WIIM_EQUALIZER_OFF)
                else:
                    await self._http_command_ok(WiimHttpCommand.WIIM_EQ_LOAD, eq_mode.value)
                self.equalizer_mode = eq_mode
                self._custom_player_properties[PlayerAttribute.EQUALIZER_MODE] = eq_mode.value
                return
            except WiimRequestException as e:
                self.logger.error("Device %s: Failed to set WiiM EQ mode via HTTP: %s", self.name, e)
                raise
        self.logger.warning("Device %s: Set equalizer mode not supported or HTTP API unavailable.", self.name)
        raise WiimDeviceException("Set equalizer mode not supported or HTTP API unavailable.")


    async def async_get_queue_items(self) -> list:
        """Get items from the PlayQueue service (speculative)."""
        if not self.play_queue_service:
            self.logger.warning("Device %s: PlayQueue service not available.", self.name)
            return []
        try:
            result = await self._invoke_upnp_action("PlayQueue", "GetQueue", QueueID=0, StartingIndex=0, RequestedCount=100)
            return self._parse_queue_data(result.get("QueueData", ""))
        except WiimDeviceException:
            return []

    def _parse_queue_data(self, queue_data_str: str) -> list:
        """Parse queue data from PlayQueue service (needs actual format)."""
        self.logger.debug("Device %s: Parsing queue data (first 100 chars): %s", self.name, queue_data_str[:100])
        if not queue_data_str:
            return []
        try:
            # This is highly dependent on the format WiiM uses.
            # If it's XML (like DIDL-Lite), use an XML parser.
            # If it's JSON, use json.loads().
            # Placeholder:
            return [{"title": "Queue item (actual parsing logic needed for PlayQueue)"}]
        except Exception as e: # pylint: disable=broad-except
            self.logger.error("Device %s: Failed to parse queue data: %s", self.name, e)
            return []

    @property
    def name(self) -> str:
        """Return the name of the device."""
        http_name = self._device_info_properties.get(DeviceAttribute.DEVICE_NAME)
        return http_name or self._name

    @property
    def udn(self) -> str:
        """Return the UDN (Unique Device Name) of the device."""
        return self._udn

    @property
    def model_name(self) -> str:
        """Return the model name of the device."""
        project_id = self._device_info_properties.get(DeviceAttribute.PROJECT)
        if project_id:
            _, model = get_info_from_project(project_id)
            if model != "WiiM":
                return model
        return self.upnp_device.model_name if self.upnp_device else "WiiM Device"


    @property
    def firmware_version(self) -> str | None:
        """Return the firmware version from HTTP API."""
        return self._device_info_properties.get(DeviceAttribute.FIRMWARE)

    @property
    def ip_address(self) -> str | None:
        """Return the IP address of the device."""
        if self.upnp_device and self.upnp_device.device_url:
            try:
                return urlparse(self.upnp_device.device_url).hostname
            except ValueError: # Handle potential malformed URLs
                 pass
        if self._http_api: 
            try:
                return urlparse(str(self._http_api)).hostname
            except ValueError:
                pass
        return None
    
    @property
    def http_api_url(self) -> str | None:
        """Return the base URL for the HTTP API if configured."""
        return str(self._http_api) if self._http_api else None

    @property
    def available(self) -> bool:
        """Return True if the device is considered available."""
        # _available is set by init and error handling.
        # Also check underlying upnp_device's availability if it's a full object.
        upnp_dev_available = True # Assume true if it's a shell
        if hasattr(self.upnp_device, 'available'): # Check if it's a real UpnpDevice
            upnp_dev_available = self.upnp_device.available
        return self._available and upnp_dev_available


    @property
    def album_art_uri(self) -> str | None:
        """Return the current track's album art URI."""
        return self.current_track_info.get("album_art_uri")


    def _parse_duration(self, time_str: str | None) -> int: # Allow None
        """Parse HH:MM:SS or HH:MM:SS.mmm duration string to seconds."""
        if not time_str: return 0
        # Handle potential "NOT_IMPLEMENTED" or empty strings
        if time_str.upper() == "NOT_IMPLEMENTED" or not time_str.strip():
            return 0
            
        parts = time_str.split('.')[0].split(':')
        try:
            if len(parts) == 3: # HH:MM:SS
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            elif len(parts) == 2: # MM:SS
                return int(parts[0]) * 60 + int(parts[1])
            elif len(parts) == 1: # SS
                return int(parts[0])
        except ValueError:
            self.logger.warning("Could not parse duration string: '%s'", time_str)
            return 0
        self.logger.warning("Unhandled duration string format: '%s'", time_str)
        return 0 # Default if format is unexpected

    def _format_duration(self, seconds: int) -> str:
        """Format seconds into HH:MM:SS string."""
        if not isinstance(seconds, (int, float)) or seconds < 0:
            seconds = 0 # Default to 0 if invalid input
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02}:{m:02}:{s:02}"

    def _make_absolute_url(self, relative_url: str | None) -> str | None:
        """Convert a relative URL from UPnP metadata to an absolute one."""
        if not relative_url:
            return None
        # Use urllib.parse.urljoin for robust URL joining
        # It needs a base URL that includes the scheme and netloc.
        # The device_url of the UpnpDevice object is the URL to the description.xml,
        # which is suitable as a base.
        if self.upnp_device and self.upnp_device.device_url:
            return urljoin(self.upnp_device.device_url, relative_url)
        # Fallback if device_url is not available (e.g. shell UpnpDevice)
        # Try to construct from presentation_url or http_api_url if they exist
        base_for_url_join = None
        if self.upnp_device and self.upnp_device.presentation_url:
             base_for_url_join = self.upnp_device.presentation_url
        elif self.http_api_url:
             base_for_url_join = self.http_api_url
        
        if base_for_url_join:
            return urljoin(base_for_url_join, relative_url)
            
        self.logger.warning("Cannot make URL absolute: No base URL (device_url, presentation_url, or http_api_url) available for relative path %s", relative_url)
        return relative_url # Return as is if no base can be determined


    async def disconnect(self) -> None:
        """Clean up resources, unsubscribe from events."""
        self.logger.info("Device %s: Disconnecting...", self.name)
        if self._cancel_event_renewal:
            self._cancel_event_renewal.cancel()
            self._cancel_event_renewal = None
        
        # Stop and unsubscribe UPnP event handling
        if self._event_handler and self._event_handler_started:
            try:
                # Unsubscribe from services first
                if self.av_transport and self.av_transport.event_subscription_sid:
                    await self._event_handler.async_unsubscribe(self.av_transport)
                if self.rendering_control and self.rendering_control.event_subscription_sid:
                    await self._event_handler.async_unsubscribe(self.rendering_control)
                if self.play_queue_service and self.play_queue_service.event_subscription_sid: # Check service exists
                    await self._event_handler.async_unsubscribe(self.play_queue_service)
            except UpnpError as err:
                self.logger.warning("Device %s: Error during UPnP unsubscribe: %s", self.name, err)
            except Exception as err:
                self.logger.error("Device %s: Unexpected error during UPnP unsubscribe: %s", self.name, err, exc_info=True)

        if self._notify_server: # Stop the notify server
            try:
                await self._notify_server.async_stop()
                self.logger.info("Device %s: AiohttpNotifyServer stopped.", self.name)
            except Exception as err:
                self.logger.error("Device %s: Error stopping AiohttpNotifyServer: %s", self.name, err, exc_info=True)
        
        self._event_handler_started = False # Mark as not started
        self._available = False
        
        if self._event_callback: 
            try:
                await self._event_callback(self)
            except Exception as e: 
                self.logger.error("Error in event_callback during disconnect for %s: %s", self.name, e)
            
    def _format_time_for_sync(self) -> str:
        """Helper to format current time for TIMESYNC HTTP command."""
        import time
        return time.strftime("%Y%m%d%H%M%S")

