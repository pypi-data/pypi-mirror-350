from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, List
from urllib.parse import urlparse
from aiohttp import ClientTimeout, TCPConnector, ClientSession

from async_upnp_client.client import UpnpDevice
# from async_upnp_client.discover import DiscoverListener, SsdpListener # For more control
from async_upnp_client.aiohttp import AiohttpNotifyServer, AiohttpRequester
from async_upnp_client.ssdp import SSDP_IP_V4, SSDP_PORT
from async_upnp_client.search import async_search # Can be used for simpler discovery too
from async_upnp_client.exceptions import UpnpConnectionError

from .consts import (
    SDK_LOGGER,
    UPNP_DEVICE_TYPE, # Standard MediaRenderer
    MANUFACTURER_WIIM,
)
from .wiim_device import WiimDevice
from .endpoint import WiimApiEndpoint
from .exceptions import WiimRequestException

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from async_upnp_client.server import UpnpNotifyServer
    from zeroconf import Zeroconf # For Home Assistant context

# Timeout for device discovery attempts
DISCOVERY_TIMEOUT = 10 # seconds
DEVICE_VERIFICATION_TIMEOUT = 5 # seconds

async def verify_wiim_device(
    location: str, session: ClientSession
) -> UpnpDevice | None:
    """
    Verifies if a device at a given location (URL to description.xml) is a WiiM device.
    Returns a UpnpDevice object if verified, otherwise None.
    """
    logger = SDK_LOGGER
    requester = AiohttpRequester(session, timeout=DEVICE_VERIFICATION_TIMEOUT)
    try:
        device = await UpnpDevice.async_create_device(requester, location)
        logger.debug("Verifying device: %s, Manufacturer: %s, Model: %s, UDN: %s",
                     device.friendly_name, device.manufacturer, device.model_name, device.udn)

        # Primary check: Manufacturer string in device description
        if device.manufacturer and MANUFACTURER_WIIM.lower() in device.manufacturer.lower():
            logger.info("Verified WiiM device by manufacturer: %s (%s)", device.friendly_name, device.udn)
            return device
        
        # Secondary checks (e.g., model name patterns, specific services)
        # if "wiim" in device.model_name.lower():
        #     logger.info("Verified WiiM device by model name: %s (%s)", device.friendly_name, device.udn)
        #     return device

        # Check for known WiiM project IDs if we can fetch initial HTTP status quickly
        # This might be too slow for initial discovery verification.
        # For now, relying on manufacturer string is common for UPnP.

        logger.debug("Device %s at %s does not appear to be a WiiM device.", device.friendly_name, location)
        return None
    except (UpnpConnectionError, asyncio.TimeoutError, WiimRequestException) as e:
        logger.debug("Failed to verify device at %s: %s", location, e)
        return None
    except Exception as e: # pylint: disable=broad-except
        logger.error("Unexpected error verifying device at %s: %s", location, e, exc_info=True)
        return None


async def async_discover_wiim_devices_upnp(
    session: ClientSession,
    timeout: int = DISCOVERY_TIMEOUT,
    target_device_type: str = UPNP_DEVICE_TYPE, # "urn:schemas-upnp-org:device:MediaRenderer:1"
) -> List[WiimDevice]:
    """
    Discovers WiiM devices on the network using UPnP (SSDP).
    Creates WiimDevice instances for verified devices.
    """
    logger = SDK_LOGGER
    discovered_devices: dict[str, WiimDevice] = {} # UDN: WiimDevice
    found_locations: set[str] = set()

    async def device_found_callback(udn: str, location: str, device_type: str):
        nonlocal found_locations
        if location in found_locations: # Avoid processing duplicates from multiple announcements
            return
        found_locations.add(location)

        logger.debug("UPnP Discovery: Found %s at %s (type: %s)", udn, location, device_type)
        if target_device_type and target_device_type not in device_type:
            logger.debug("Ignoring device %s, does not match target type %s", udn, target_device_type)
            return

        upnp_device = await verify_wiim_device(location, session)
        if upnp_device and upnp_device.udn not in discovered_devices:
            # Create HTTP endpoint for the WiimDevice
            host = urlparse(location).hostname
            http_api = None            
            if host:
                # Attempt to create HTTPS first, then HTTP as fallback for WiimApiEndpoint
                # This logic could be more sophisticated based on device capabilities
                try:
                    # Try common HTTPS ports if applicable, or just default HTTP
                    # For simplicity, using default HTTP for now.
                    # The wiim_factory_httpapi_bridge in old code tried https 443/4443 then http 80   
                    sessions = ClientSession(connector=TCPConnector(ssl=False))                 
                    http_api = WiimApiEndpoint(protocol="https", port=443, endpoint=host, session=sessions)
                    # A quick check if HTTP API is responsive (optional, adds delay)
                    await http_api.json_request("getStatusEx")
                except Exception: # pylint: disable=broad-except
                    logger.warning("Could not establish default HTTP API for %s, some features might be limited.", host)
                    http_api = None


            wiim_dev = WiimDevice(upnp_device, session, http_api_endpoint=http_api)
            # Initialize services and subscribe. If it fails, device won't be added.
            if await wiim_dev.async_init_services_and_subscribe():
                discovered_devices[upnp_device.udn] = wiim_dev
                logger.info("Successfully created and initialized WiimDevice: %s (%s)",
                            wiim_dev.name, wiim_dev.udn)
            else:
                logger.warning("Failed to initialize WiimDevice after discovery: %s", upnp_device.friendly_name)


    # Using SsdpListener for more control over the discovery process
    # You'll need a source_ip for SsdpListener, or use a higher-level discoverer
    # For simplicity in this context, we can use async_search if a specific source_ip is hard to get.
    # However, for robust SDK, providing source_ip or using a library that handles it is better.

    # Alternative using async_search (simpler but less control):
    # results = await async_search(
    #     service_type=target_device_type, # or "ssdp:all" and filter later
    #     timeout=timeout,
    #     session=session, # async_search might create its own requester if session not directly usable
    # )
    # for result in results:
    #    await device_found_callback(result.get("UDN", ""), result.get("LOCATION", ""), result.get("ST", ""))

    # Using a DiscoverListener approach:
    # This requires a notify server, which might be overkill if only doing one-shot discovery.
    # For continuous discovery or if HA's zeroconf/ssdp infrastructure is not used by SDK directly.

    # For now, let's simulate finding devices and calling the callback.
    # In a real scenario, you'd integrate with an SSDP listener.
    # For Home Assistant, its own SSDP integration would feed this.
    # If SDK is standalone, it needs its own SSDP listener.

    # Simplified approach for this refactor, assuming locations can be found:
    # This part needs to be implemented with a proper SSDP discovery mechanism.
    # For example, using `async_ssdp_search` from `aioupnp` or similar.
    # Or, if this SDK is *only* for HA, HA's discovery mechanisms would provide the initial IPs/locations.

    logger.warning("async_discover_wiim_devices_upnp: SSDP discovery mechanism needs to be fully implemented "
                   "or integrated with HA's discovery if SDK is HA-specific.")
    # Placeholder for actual SSDP search results:
    # Example:
    # locations_from_ssdp = await some_actual_ssdp_search_function(timeout, target_device_type)
    # for loc in locations_from_ssdp:
    #     await device_found_callback("udn_from_ssdp", loc, "type_from_ssdp")

    # This function would typically be called by a higher-level discovery manager
    # or by the Home Assistant config flow using its own mDNS/SSDP results.

    return list(discovered_devices.values())


async def async_discover_wiim_devices_zeroconf(
    session: ClientSession, zeroconf_instance: "Zeroconf", service_type: str = "_linkplay._tcp.local."
) -> List[WiimDevice]:
    """
    Discovers WiiM devices using Zeroconf (mDNS) and then verifies them via UPnP.
    This is more aligned with how Home Assistant's config flow might initiate discovery.
    `zeroconf_instance` would be `hass.data[ZEROCONF_INSTANCE]` in HA.
    """
    logger = SDK_LOGGER
    discovered_wiim_devices: dict[str, WiimDevice] = {} # UDN: WiimDevice
    
    # This function relies on an external Zeroconf discovery mechanism
    # that provides IPs/ports of potential devices.
    # Home Assistant's `async_step_zeroconf` in config_flow provides this.
    # This function is more of a "processor" for zeroconf results.

    # Example of how it might be used if you get a list of ZeroconfServiceInfo objects:
    # for service_info in list_of_zeroconf_service_infos:
    #     host = service_info.host
    #     # UPnP device description is usually on a standard port (often 80 or others like 1900 for SSDP announce)
    #     # but the XML location can vary. We need the UPnP description URL.
    #     # Zeroconf for UPnP might directly provide the path to description.xml in properties.
    #     # e.g., service_info.properties.get(b'path', b'/description.xml').decode()
    #
    #     # If Zeroconf only gives IP, we might need to probe common UPnP description paths
    #     # or perform a targeted SSDP M-SEARCH to that IP to get the LOCATION header.
    #     # This is complex.
    #
    #     # For now, assume `host` is enough to construct a potential description URL
    #     # or that a more complete UPnP discovery is done after mDNS gives the IP.
    #
    #     # Simplification: Assume mDNS gives IP, then we do UPnP discovery on that IP.
    #     # This is not ideal as mDNS for UPnP should give the description path.
    #     # If `_linkplay._tcp.local.` is a custom service, its TXT records might contain the UPnP location.

    logger.warning("async_discover_wiim_devices_zeroconf: Relies on external Zeroconf to provide IPs. "
                   "Further UPnP probing is needed to get description.xml location from just an IP.")

    # This function is more of a conceptual placeholder for how Zeroconf results would feed into UPnP verification.
    # The actual Zeroconf discovery and parsing of its results (TXT records for path to description.xml)
    # would happen in the HA config_flow.py.
    # Then, `verify_wiim_device` would be called with the correct description.xml URL.

    return list(discovered_wiim_devices.values())