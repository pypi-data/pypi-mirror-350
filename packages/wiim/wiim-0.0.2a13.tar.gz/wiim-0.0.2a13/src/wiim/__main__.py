# wiim/__main__.py
import asyncio
import logging

from aiohttp import ClientSession

from wiim.controller import WiimController # New SDK
from .wiim_device import WiimDevice # New SDK
from wiim.consts import SDK_LOGGER # SDK's logger
# from wiim.utils import async_create_unverified_client_session # This util might need update or replacement

# A simple helper to create a session for the CLI tool if the old util is not suitable.
async def _create_cli_session() -> ClientSession:
    """Create an aiohttp client session for CLI use."""
    # In a real CLI tool, you might want to handle SSL verification more robustly.
    # For local network discovery, often unverified is acceptable for testing.
    # connector = TCPConnector(ssl=False)
    # return ClientSession(connector=connector)
    return ClientSession()


async def main_cli():
    """
    Command-line interface for discovering and interacting with WiiM devices.
    """
    # Setup basic logging for the CLI tool
    SDK_LOGGER.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    SDK_LOGGER.info("Starting WiiM SDK CLI discovery...")

    async with await _create_cli_session() as session:
        # The controller can be used to discover and manage multiple devices
        # The event_callback is optional for CLI, but useful for continuous monitoring
        controller = WiimController(session)

        # Discover devices using UPnP (SSDP)
        # The SDK's discover_and_add_devices now uses async_discover_wiim_devices_upnp
        await controller.discover_and_add_devices()

        if not controller.devices:
            SDK_LOGGER.info("No WiiM devices found on the network.")
            return

        SDK_LOGGER.info(f"Found {len(controller.devices)} WiiM device(s):")
        for device_idx, device in enumerate(controller.devices):
            print(f"\n--- Device {device_idx + 1} ---")
            if not device.available:
                print(f"Name: {device.name} (UDN: {device.udn}) - Currently Unavailable")
                continue

            # WiimDevice properties are updated by UPnP events or initial HTTP fetch
            # For CLI, we might want to explicitly fetch/refresh if not relying on continuous events.
            # The async_init_services_and_subscribe in WiimDevice already fetches initial state.
            
            print(f"  Name: {device.name}")
            print(f"  UDN: {device.udn}")
            print(f"  Model: {device.model_name}")
            print(f"  Manufacturer: {device.manufacturer}")
            print(f"  IP Address: {device.ip_address}")
            print(f"  Firmware: {device.firmware_version or 'N/A'}")
            print(f"  HTTP API URL: {device.http_api_url or 'N/A'}")
            print(f"  UPnP Device URL: {device.upnp_device.device_url if device.upnp_device else 'N/A'}")

            # Display current media state from WiimDevice
            print(f"  Status: {device.playing_status.value if device.playing_status else 'N/A'}")
            print(f"  Volume: {device.volume}% {'(Muted)' if device.is_muted else ''}")
            print(f"  Source (Play Mode): {device.play_mode.value if device.play_mode else 'N/A'}")
            print(f"  Repeat Mode: {device.loop_mode.value if device.loop_mode else 'N/A'}")
            print(f"  EQ Mode: {device.equalizer_mode.value if device.equalizer_mode else 'N/A'}")

            if device.playing_status == device.playing_status.PLAYING or device.playing_status == device.playing_status.PAUSED:
                track_info = device.current_track_info
                print(f"  Current Track:")
                print(f"    Title: {track_info.get('title', 'N/A')}")
                print(f"    Artist: {track_info.get('artist', 'N/A')}")
                print(f"    Album: {track_info.get('album', 'N/A')}")
                print(f"    Duration: {device.current_track_duration}s")
                print(f"    Position: {device.current_position}s")
                print(f"    Album Art URI: {device.album_art_uri or 'N/A'}")
            
            # Example: Get UPnP service state variables (if needed for deep diagnostics)
            # if device.av_transport:
            #     print("  AVTransport Service Variables (sample):")
            #     try:
            #         # Fetching all state variables can be verbose
            #         # transport_info = await device.av_transport.action('GetTransportInfo').async_call(InstanceID=0)
            #         # print(f"    TransportState: {transport_info.get('CurrentTransportState')}")
            #         # position_info = await device.av_transport.action('GetPositionInfo').async_call(InstanceID=0)
            #         # print(f"    TrackDuration: {position_info.get('TrackDuration')}, RelTime: {position_info.get('RelTime')}")
            #         pass # Add specific calls if needed
            #     except Exception as e:
            #         print(f"    Error getting AVTransport info: {e}")


        # Example of multiroom info
        SDK_LOGGER.info("\nChecking multiroom groups (via HTTP on leaders)...")
        # The controller's discover_multirooms was called by discover_and_add_devices or needs separate call
        # await controller.async_update_all_multiroom_status() # Ensure it's up-to-date

        if controller._multiroom_groups: # Accessing internal for CLI example
            print("\n--- Multiroom Groups ---")
            for leader_udn, follower_udns in controller._multiroom_groups.items():
                leader_device = controller.get_device(leader_udn)
                if leader_device:
                    follower_names = [controller.get_device(fudn).name for fudn in follower_udns if controller.get_device(fudn)]
                    print(f"  Leader: {leader_device.name} (UDN: {leader_udn})")
                    if follower_names:
                        print(f"    Followers: {', '.join(follower_names)}")
                    else:
                        print(f"    Followers: None")
        else:
            print("  No active multiroom groups found or reported by devices.")

        # Clean up: Disconnect devices to release resources (e.g., UPnP subscriptions)
        # This is important if the CLI tool is not long-running.
        print("\nDisconnecting from devices...")
        for device in controller.devices:
            await device.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main_cli())
    except KeyboardInterrupt:
        SDK_LOGGER.info("Discovery process interrupted by user.")
    except Exception as e:
        SDK_LOGGER.error(f"An error occurred: {e}", exc_info=True)

