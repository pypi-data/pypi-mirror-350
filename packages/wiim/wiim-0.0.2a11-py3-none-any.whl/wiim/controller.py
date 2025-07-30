from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, List, Optional, Dict

from .consts import SDK_LOGGER # Use SDK logger
from .wiim_device import WiimDevice, EventCallback
from .exceptions import WiimException
from .consts import WiimHttpCommand, MultiroomAttribute, DeviceAttribute # Renamed
from .discovery import async_discover_wiim_devices_upnp
from .exceptions import WiimDeviceException, WiimRequestException

if TYPE_CHECKING:
    from aiohttp import ClientSession


class WiimController:
    """Manages multiple WiiM devices and multiroom groups."""

    def __init__(self, session: ClientSession, event_callback: EventCallback | None = None):
        self.session = session
        self._devices: Dict[str, WiimDevice] = {}  # UDN: WiimDevice
        self._multiroom_groups: Dict[str, List[str]] = {} # Leader UDN: [Follower UDNs]
        self._event_callback = event_callback # Callback for device state changes
        self.logger = SDK_LOGGER

    def get_device(self, udn: str) -> WiimDevice | None:
        """Get a device by its UDN."""
        return self._devices.get(udn)

    @property
    def devices(self) -> List[WiimDevice]:
        """Return a list of all managed WiiM devices."""
        return list(self._devices.values())

    async def add_device(self, wiim_device: WiimDevice) -> None:
        """Add a WiiM device to the controller."""
        if wiim_device.udn in self._devices:
            self.logger.debug("Device %s already managed.", wiim_device.udn)
            # Potentially update existing device object if new one is more current
            # For now, just return if already exists.
            return

        # Set the controller's event callback if the device doesn't have one
        if not wiim_device._event_callback and self._event_callback:
             wiim_device._event_callback = self._event_callback # Propagate callback

        self._devices[wiim_device.udn] = wiim_device
        self.logger.info("Added device %s (%s) to controller.", wiim_device.name, wiim_device.udn)
        # Optionally, update multiroom status after adding a new device
        await self.async_update_all_multiroom_status()


    async def remove_device(self, udn: str) -> None:
        """Remove a WiiM device from the controller."""
        device = self._devices.pop(udn, None)
        if device:
            await device.disconnect() # Clean up device's resources (e.g., UPnP subscriptions)
            self.logger.info("Removed device %s (%s) from controller.", device.name, udn)
            # Update multiroom status as a device was removed
            await self.async_update_all_multiroom_status()
        else:
            self.logger.debug("Device %s not found for removal.", udn)

    async def discover_and_add_devices(self) -> None:
        """Discover devices using UPnP and add them."""
        # This is a simplified call; in practice, you might pass more discovery params
        # or use a specific discovery strategy (e.g., from HA's Zeroconf results)
        self.logger.info("Starting UPnP discovery for WiiM devices...")
        discovered = await async_discover_wiim_devices_upnp(self.session)
        for dev in discovered:
            if dev.udn not in self._devices:
                await self.add_device(dev)
        self.logger.info("Discovery finished. Total managed devices: %s", len(self._devices))
        await self.async_update_all_multiroom_status()


    async def async_update_multiroom_status(self, leader_device: WiimDevice) -> None:
        """
        Updates the multiroom status for a group where leader_device is the leader.
        Multiroom grouping is typically done via HTTP API for Linkplay/WiiM.
        """
        if not leader_device._http_api:
            self.logger.debug("Leader device %s has no HTTP API, cannot update multiroom status.", leader_device.name)
            # Clear any existing group info for this leader
            if leader_device.udn in self._multiroom_groups:
                del self._multiroom_groups[leader_device.udn]
            return

        try:
            response = await leader_device._http_request(WiimHttpCommand.MULTIROOM_LIST)
            num_followers = int(response.get(MultiroomAttribute.NUM_FOLLOWERS, 0))
            follower_udns: List[str] = []

            if num_followers > 0:
                slaves_list = response.get(MultiroomAttribute.FOLLOWER_LIST, [])
                if isinstance(slaves_list, list): # Ensure it's a list
                    for slave_info in slaves_list:
                        if isinstance(slave_info, dict):
                            slave_uuid = slave_info.get(MultiroomAttribute.UUID) # Assuming UDN is in 'uuid' field
                            if slave_uuid:
                                # Find the WiimDevice object for this follower UDN
                                follower_device = self.get_device(slave_uuid)
                                if follower_device:
                                    follower_udns.append(slave_uuid)
                                else:
                                    self.logger.warning("Multiroom follower %s for leader %s not found in managed devices.",
                                                        slave_uuid, leader_device.name)
                        else:
                            self.logger.warning("Unexpected slave_info format: %s", slave_info)
                else:
                    self.logger.warning("Follower list is not a list: %s", slaves_list)


            self._multiroom_groups[leader_device.udn] = follower_udns
            self.logger.info("Updated multiroom status for leader %s: %s followers (%s)",
                             leader_device.name, len(follower_udns), follower_udns)

        except WiimRequestException as e:
            self.logger.error("Failed to get multiroom list for leader %s: %s", leader_device.name, e)
            # If request fails, assume it's not a leader or group is gone
            if leader_device.udn in self._multiroom_groups:
                del self._multiroom_groups[leader_device.udn]
        except (ValueError, TypeError) as e:
            self.logger.error("Error parsing multiroom data for leader %s: %s", leader_device.name, e)
            if leader_device.udn in self._multiroom_groups:
                del self._multiroom_groups[leader_device.udn]


    async def async_update_all_multiroom_status(self) -> None:
        """Updates multiroom status for all managed devices that could be leaders."""
        self.logger.debug("Updating all multiroom statuses...")
        # Clear existing groups first, as leadership might change or groups dissolve
        current_leaders = list(self._multiroom_groups.keys())
        self._multiroom_groups.clear()

        # Check each device if it's a leader of a new/existing group
        # This assumes any device *could* be a leader.
        # A more optimized way might be needed if devices report leadership status.
        for device in self._devices.values():
            # Heuristic: if a device was a leader, or if it's not known to be a follower of an existing group
            # For simplicity, try to update for all, `async_update_multiroom_status` handles non-leaders.
            await self.async_update_multiroom_status(device)

        # Remove devices from follower lists if they are now leaders of their own group
        all_followers_being_led = set()
        for leader_udn, follower_udns in self._multiroom_groups.items():
            for follower_udn in follower_udns:
                all_followers_being_led.add(follower_udn)

        final_groups = {}
        for leader_udn, follower_udns in self._multiroom_groups.items():
            if leader_udn not in all_followers_being_led: # Only keep it as a leader if it's not also a follower
                final_groups[leader_udn] = follower_udns
        self._multiroom_groups = final_groups


    def get_group_members(self, device_udn: str) -> List[WiimDevice]:
        """Get all members of the group the given device belongs to (including itself)."""
        # Check if it's a leader
        if device_udn in self._multiroom_groups:
            leader = self.get_device(device_udn)
            if not leader: return []
            followers = [self.get_device(f_udn) for f_udn in self._multiroom_groups[device_udn] if self.get_device(f_udn)]
            return [leader] + followers

        # Check if it's a follower
        for leader_udn, follower_udns in self._multiroom_groups.items():
            if device_udn in follower_udns:
                leader = self.get_device(leader_udn)
                if not leader: return []
                group_followers = [self.get_device(f_udn) for f_udn in follower_udns if self.get_device(f_udn)]
                # Ensure the current device is included if it's in the follower list
                current_device_in_group = self.get_device(device_udn)
                all_members = [leader] + group_followers
                if current_device_in_group and current_device_in_group not in all_members: # Should not happen if logic is correct
                    all_members.append(current_device_in_group)
                return list(set(all_members)) # Ensure uniqueness

        # Not in a group, just itself
        device = self.get_device(device_udn)
        return [device] if device else []

    async def async_join_group(self, leader_udn: str, follower_udn: str) -> None:
        """Make follower_udn join the group led by leader_udn."""
        leader = self.get_device(leader_udn)
        follower = self.get_device(follower_udn)

        if not leader or not follower:
            raise WiimException("Leader or follower device not found.")
        if not leader._http_api or not follower._http_api:
            raise WiimException("HTTP API not available for leader or follower.")
        if not leader._device_info_properties.get(DeviceAttribute.ETH0) and not leader.ip_address: # Need leader's IP/eth for command
             raise WiimException("Leader IP/Ethernet info not available.")


        # The command MULTIROOM_JOIN = "ConnectMasterAp:JoinGroupMaster:eth{}:uuid={}"
        # Needs leader's IP (or eth interface name if that's what 'eth{}' means) and leader's UDN (uuid)
        # Assuming 'eth{}' refers to the IP address for simplicity here.
        # The original SDK used `leader.device.eth` which might be an IP or interface name.
        # Using IP address as a more general approach.
        leader_ip_for_cmd = leader._device_info_properties.get(DeviceAttribute.ETH0) or leader.ip_address

        if not leader_ip_for_cmd:
            raise WiimException(f"Cannot determine leader's IP/ETH identifier for JoinGroup command for {leader.name}")

        try:
            # The command is executed on the FOLLOWER device
            await follower._http_command_ok(WiimHttpCommand.MULTIROOM_JOIN, f"{leader_ip_for_cmd}:{leader.udn}")
            self.logger.info("Device %s successfully sent join command to leader %s", follower.name, leader.name)
            await self.async_update_multiroom_status(leader) # Update group status
        except WiimRequestException as e:
            self.logger.error("Failed to make %s join %s: %s", follower.name, leader.name, e)
            raise

    async def async_ungroup_device(self, device_udn: str) -> None:
        """Make a device leave its current group."""
        device = self.get_device(device_udn)
        if not device or not device._http_api:
            raise WiimException("Device not found or HTTP API unavailable.")

        # Determine if it's a leader or follower
        is_leader = device_udn in self._multiroom_groups
        leader_of_this_device: WiimDevice | None = None

        if not is_leader:
            for l_udn, f_udns in self._multiroom_groups.items():
                if device_udn in f_udns:
                    leader_of_this_device = self.get_device(l_udn)
                    break
        
        original_leader_to_update: WiimDevice | None = None

        if is_leader:
            # Device is a leader, ungroup the whole group
            await device._http_command_ok(WiimHttpCommand.MULTIROOM_UNGROUP)
            self.logger.info("Ungrouped multiroom group led by %s", device.name)
            if device_udn in self._multiroom_groups:
                del self._multiroom_groups[device_udn]
            original_leader_to_update = device # Update itself after ungrouping
        elif leader_of_this_device:
            # Device is a follower, kick it from the group (leader executes kick)
            # MULTIROOM_KICK = "multiroom:SlaveKickout:{}" (takes follower's IP/eth)
            follower_ip_for_cmd = device._device_info_properties.get(DeviceAttribute.ETH0) or device.ip_address
            if not follower_ip_for_cmd:
                 raise WiimException(f"Cannot determine follower's IP/ETH for Kick command for {device.name}")
            if not leader_of_this_device._http_api:
                raise WiimException(f"Leader {leader_of_this_device.name} HTTP API unavailable for Kick command.")

            await leader_of_this_device._http_command_ok(WiimHttpCommand.MULTIROOM_KICK, follower_ip_for_cmd)
            self.logger.info("Kicked device %s from group led by %s", device.name, leader_of_this_device.name)
            original_leader_to_update = leader_of_this_device
        else:
            self.logger.info("Device %s is not part of any multiroom group.", device.name)
            return # Not in a group

        if original_leader_to_update:
            await self.async_update_multiroom_status(original_leader_to_update)
        else: # If it was a standalone device or some edge case, refresh all.
            await self.async_update_all_multiroom_status()
