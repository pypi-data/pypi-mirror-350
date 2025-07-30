# wiim/__init__.py
"""WiiM Asynchronous Python SDK."""

from .__version__ import __version__
from .wiim_device import WiimDevice
from .controller import WiimController
from .endpoint import WiimApiEndpoint, WiimBaseEndpoint
from .exceptions import (
    WiimException,
    WiimRequestException,
    WiimInvalidDataException,
    WiimDeviceException,
)
from .consts import (
    # Enums likely to be used by consumers of the SDK
    PlayingStatus,
    PlayingMode,
    LoopMode,
    EqualizerMode,
    MuteMode,
    ChannelType,
    SpeakerType,
    AudioOutputHwMode,
    # Attribute Enums if consumers need to parse raw data (less common)
    # DeviceAttribute,
    # PlayerAttribute,
    # MultiroomAttribute,
    # MetaInfo,
    # MetaInfoMetaData,
    # HTTP Commands (usually internal to SDK but can be exposed if advanced use needed)
    # WiimHttpCommand,
)
from .handler import parse_last_change_event # If useful externally

__all__ = [
    "__version__",
    "WiimDevice",
    "WiimController",
    "WiimApiEndpoint",
    "WiimBaseEndpoint",
    "WiimException",
    "WiimRequestException",
    "WiimInvalidDataException",
    "WiimDeviceException",
    "PlayingStatus",
    "PlayingMode",
    "LoopMode",
    "EqualizerMode",
    "MuteMode",
    "ChannelType",
    "SpeakerType",
    "AudioOutputHwMode",
    "parse_last_change_event",
]

# custom_components/wiim/__init__.py
# (No changes needed here regarding utils.py, as the previous update already handled it
# by directly using hass.helpers.aiohttp_client.async_get_clientsession in async_setup_entry.
# The original LinkPlay __init__.py had the import, but my refactored version for WiiM
# in ha_config_init_location_fix immersive already uses the HA helper.)

# Let's re-verify the config_flow.py for utils.py usage.
# The previous version of config_flow.py (in ha_config_init_location_fix)
# already uses `from homeassistant.helpers.aiohttp_client import async_get_clientsession`.
# So, no change needed there either regarding utils.py.

# Conclusion: The removal of a local utils.py and direct use of HA's aiohttp client session
# helper seems to have been incorporated in the previous steps for the HA integration files.
# The SDK's __init__.py is now provided.

