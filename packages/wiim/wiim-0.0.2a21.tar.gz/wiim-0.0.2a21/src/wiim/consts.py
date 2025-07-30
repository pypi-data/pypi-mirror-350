import logging
from enum import IntFlag, StrEnum

# SDK_LOGGER should be distinct from HA's logger if SDK is standalone
SDK_LOGGER = logging.getLogger("wiim.sdk") # Changed logger name

API_ENDPOINT: str = "{}/httpapi.asp?command={}" # For WiimApiEndpoint
API_TIMEOUT: int = 10 # Increased default timeout slightly
UNKNOWN_TRACK_PLAYING: str = "Unknown"

# Standard UPnP Device Type for Media Renderers
UPNP_DEVICE_TYPE = "urn:schemas-upnp-org:device:MediaRenderer:1"

# Standard UPnP Service IDs
UPNP_AV_TRANSPORT_SERVICE_ID = "urn:schemas-upnp-org:service:AVTransport:1"
UPNP_RENDERING_CONTROL_SERVICE_ID = "urn:schemas-upnp-org:service:RenderingControl:1"
# Custom WiiM UPnP Service ID (as specified by user)
UPNP_WIIM_PLAY_QUEUE_SERVICE_ID = "urn:schemas-wiimu-com:service:PlayQueue:1"


# Renamed from LinkPlayCommand to WiimHttpCommand
class WiimHttpCommand(StrEnum):
    """Defines the WiiM HTTP API commands."""
    DEVICE_STATUS = "getStatusEx"
    # SYSLOG = "getsyslog" # Keep if used
    # UPDATE_SERVER = "GetUpdateServer" # Keep if used
    REBOOT = "reboot"
    PLAYER_STATUS = "getPlayerStatusEx"
    # NEXT = "setPlayerCmd:next"
    # PREVIOUS = "setPlayerCmd:prev"
    # UNMUTE = "setPlayerCmd:mute:0"
    # MUTE = "setPlayerCmd:mute:1"
    # RESUME = "setPlayerCmd:resume"
    # PLAY = "setPlayerCmd:play:{}" # Takes URL
    # SEEK = "setPlayerCmd:seek:{}" # Takes position in seconds or ms (check API)
    # VOLUME = "setPlayerCmd:vol:{}" # Takes 0-100
    # PLAYLIST = "setPlayerCmd:playlist:uri:{}" # Keep if used for specific playlist URIs
    # PAUSE = "setPlayerCmd:pause"
    # STOP = "setPlayerCmd:stop"
    # TOGGLE = "setPlayerCmd:onepause"
    # EQUALIZER_MODE = "setPlayerCmd:equalizer:{}" # General, WiiM uses specific
    WIIM_EQUALIZER_ON = "EQOn" # Not standard, seems WiiM specific
    WIIM_EQUALIZER_OFF = "EQOff"
    # LOOP_MODE = "setPlayerCmd:loopmode:{}" # Takes LoopMode int value
    SWITCH_MODE = "setPlayerCmd:switchmode:{}" # Takes mode string e.g. "line-in"
    # M3U_PLAYLIST = "setPlayerCmd:m3u:play:{}" # Keep if used
    MULTIROOM_LIST = "multiroom:getSlaveList"
    MULTIROOM_UNGROUP = "multiroom:ungroup"
    MULTIROOM_KICK = "multiroom:SlaveKickout:{}" # Takes follower's IP/eth
    MULTIROOM_VOL = "setPlayerCmd:slave_vol:{}" # Group volume
    MULTIROOM_MUTE = "setPlayerCmd:slave_mute:mute" # Group mute
    MULTIROOM_UNMUTE = "setPlayerCmd:slave_mute:unmute" # Group unmute
    # Format: leader_ip_or_eth:leader_uuid
    MULTIROOM_JOIN = "ConnectMasterAp:JoinGroupMaster:{}" # Executed on follower
    PLAY_PRESET = "MCUKeyShortClick:{}" # Takes preset number 1-based
    # TIMESYNC = "timeSync:{}" # Takes YYYYMMDDHHMMSS
    WIIM_EQ_LOAD = "EQLoad:{}" # Takes WiiM EQ mode name (e.g., "Rock")
    # META_INFO = "getMetaInfo" # For album art, etc.
    # AUDIO_OUTPUT_HW_MODE_SET = "setAudioOutputHardwareMode:{}" # Keep if used
    # AUDIO_OUTPUT_HW_MODE = "getNewAudioOutputHardwareMode" # Keep if used

# Enums (largely unchanged, ensure they match API responses)
class SpeakerType(StrEnum):
    MAIN_SPEAKER = "0"
    SUB_SPEAKER = "1"

class ChannelType(StrEnum):
    STEREO = "0"
    LEFT_CHANNEL = "1"
    RIGHT_CHANNEL = "2"

class PlayingMode(StrEnum):
    # Values are as per existing SDK, map to what getPlayerStatusEx returns for 'mode'
    IDLE = "-1" # Or "0" if API changed
    NONE = "0" # Often means idle or no source selected
    AIRPLAY = "1"
    DLNA = "2"
    QPLAY = "3"
    NETWORK = "10" # General network playback (UPnP stream, internet radio)
    # WIIMU_LOCAL = "11" # These seem specific, keep if API uses them
    # WIIMU_STATION = "12"
    # WIIMU_RADIO = "13"
    # WIIMU_SONGLIST = "14"
    # TF_CARD_1 = "16"
    # WIIMU_MAX = "19"
    # API = "20" # Playback via API command
    UDISK = "21" # USB disk
    # HTTP_MAX = "29"
    # ALARM = "30"
    SPOTIFY = "31"
    TIDAL = "32"
    LINE_IN = "40"
    BLUETOOTH = "41"
    OPTICAL = "43"
    RCA = "44"
    COAXIAL = "45"
    # FM = "46"
    LINE_IN_2 = "47"
    # XLR = "48"
    HDMI = "49" # Or ARC
    # CD = "50"
    USB_DAC = "51"
    # TF_CARD_2 = "52"
    # EXTERN_BLUETOOTH = "53"
    # PHONO = "54"
    OPTICAL_2 = "56"
    COAXIAL_2 = "57"
    ARC = "58" # HDMI ARC
    # TALK = "60" # Voice assistant?
    FOLLOWER = "99" # Multiroom follower state

# Map for sending SWITCH_MODE HTTP command
PLAY_MODE_HTTP_PARAM_MAP: dict[PlayingMode, str] = {
    PlayingMode.NETWORK: "wifi", # Or "net" - check API
    PlayingMode.LINE_IN: "line-in",
    PlayingMode.BLUETOOTH: "bluetooth",
    PlayingMode.OPTICAL: "optical",
    PlayingMode.RCA: "RCA",
    PlayingMode.COAXIAL: "co-axial",
    PlayingMode.LINE_IN_2: "line-in2",
    PlayingMode.HDMI: "hdmi", # Or "ARC" if they are distinct modes
    PlayingMode.ARC: "ARC",
    PlayingMode.USB_DAC: "PCUSB", # Or "usbdac"
    PlayingMode.SPOTIFY: "Spotify", # Usually initiated by Spotify Connect, not direct mode switch
    PlayingMode.TIDAL: "Tidal",
    PlayingMode.AIRPLAY: "Airplay", # Usually auto-switches
    # Add others as per API 1.03 documentation for setPlayerCmd:switchmode:
}


class LoopMode(StrEnum):
    # Values from getPlayerStatusEx 'loop' field
    CONTINOUS_PLAY_ONE_SONG = "-1" # Repeat one song
    PLAY_IN_ORDER = "0" # Play queue once, then stop
    CONTINUOUS_PLAYBACK = "1" # Repeat all (entire queue)
    RANDOM_PLAYBACK = "2" # Shuffle all
    LIST_CYCLE = "3" # Seems same as REPEAT_ALL
    # Values below might be specific combinations, map to simpler UPnP modes
    SHUFF_DISABLED_REPEAT_DISABLED = "4" # = PLAY_IN_ORDER
    SHUFF_ENABLED_REPEAT_ENABLED_LOOP_ONCE = "5" # = RANDOM_PLAYBACK (if loop once means play all shuffled items once)

class EqualizerMode(StrEnum):
    NONE = "None" # Or "off"
    # General EQ modes (may or may not be supported by WiiM HTTP API directly for setPlayerCmd:equalizer)
    CLASSIC = "Classic"
    POP = "Pop"
    JAZZ = "Jazz"
    VOCAL = "Vocal"
    # WiiM specific EQ modes for WIIM_EQ_LOAD command
    FLAT = "Flat"
    ACOUSTIC = "Acoustic"
    BASS_BOOSTER = "Bass Booster"
    BASS_REDUCER = "Bass Reducer"
    CLASSICAL = "Classical" # Note: different from "Classic"
    DANCE = "Dance"
    DEEP = "Deep"
    ELECTRONIC = "Electronic"
    HIP_HOP = "Hip-Hop"
    LATIN = "Latin"
    LOUDNESS = "Loudness"
    LOUNGE = "Lounge"
    PIANO = "Piano"
    R_B = "R&B" # Ensure no special chars if used as command param
    ROCK = "Rock"
    SMALL_SPEAKERS = "Small Speakers"
    SPOKEN_WORD = "Spoken Word"
    TREBLE_BOOSTER = "Treble Booster"
    TREBLE_REDUCER = "Treble Reducer"
    VOCAL_BOOSTER = "Vocal Booster"

class PlayingStatus(StrEnum):
    # Values from getPlayerStatusEx 'status' field
    PLAYING = "play"
    LOADING = "load" # Buffering/transitioning
    STOPPED = "stop" # Or "idle"
    PAUSED = "pause"

class MuteMode(StrEnum):
    # Values from getPlayerStatusEx 'mute' field
    UNMUTED = "0"
    MUTED = "1"

# InputMode flags for 'plm_support' from getStatusEx - keep if used for capability check
class InputMode(IntFlag):
    LINE_IN = 2
    BLUETOOTH = 4
    USB = 8 # Corresponds to UDISK
    OPTICAL = 16
    RCA = 32
    COAXIAL = 64
    # FM = 128 # If supported
    LINE_IN_2 = 256
    # XLR = 512 # If supported
    HDMI = 1024 # Includes ARC if not separate flag
    # CD = 2048 # If supported
    # TF_CARD_1 = 8192 # If supported
    # EXTERN_BLUETOOTH = 16384 # If supported
    USB_DAC = 32768
    # PHONO = 65536 # If supported
    OPTICAL_2 = 262144
    COAXIAL_2 = 524288
    # FOLLOWER = 2097152 # Indicates multiroom follower capability
    ARC = 4194304 # If separate from HDMI

# Map InputMode flags to PlayingMode enum for source listing
INPUT_MODE_TO_PLAYING_MODE: dict[InputMode, PlayingMode] = {
    InputMode.LINE_IN: PlayingMode.LINE_IN,
    InputMode.BLUETOOTH: PlayingMode.BLUETOOTH,
    InputMode.USB: PlayingMode.UDISK,
    InputMode.OPTICAL: PlayingMode.OPTICAL,
    InputMode.RCA: PlayingMode.RCA,
    InputMode.COAXIAL: PlayingMode.COAXIAL,
    # InputMode.FM: PlayingMode.FM,
    InputMode.LINE_IN_2: PlayingMode.LINE_IN_2,
    # InputMode.XLR: PlayingMode.XLR,
    InputMode.HDMI: PlayingMode.HDMI, # Or map to ARC if primary
    InputMode.ARC: PlayingMode.ARC,
    # InputMode.CD: PlayingMode.CD,
    # InputMode.TF_CARD_1: PlayingMode.TF_CARD_1, # Map to a generic SD card if needed
    # InputMode.EXTERN_BLUETOOTH: PlayingMode.EXTERN_BLUETOOTH, # If distinct from normal BT
    InputMode.USB_DAC: PlayingMode.USB_DAC,
    # InputMode.PHONO: PlayingMode.PHONO,
    InputMode.OPTICAL_2: PlayingMode.OPTICAL_2,
    InputMode.COAXIAL_2: PlayingMode.COAXIAL_2,
}


# Player attributes from getPlayerStatusEx JSON response
class PlayerAttribute(StrEnum):
    SPEAKER_TYPE = "type" # 0 for main, 1 for sub
    CHANNEL_TYPE = "ch" # 0 for stereo, 1 for L, 2 for R
    PLAYBACK_MODE = "mode" # Current PlayingMode (e.g. "40" for line-in)
    PLAYLIST_MODE = "loop" # Current LoopMode (e.g. "1" for repeat all)
    EQUALIZER_MODE = "eq" # Current EQ setting (e.g. "0" for none, or name for WiiM)
    PLAYING_STATUS = "status" # "play", "pause", "stop", "load"
    CURRENT_POSITION = "curpos" # Milliseconds
    OFFSET_POSITION = "offset_pts" # Keep if used
    TOTAL_LENGTH = "totlen" # Milliseconds
    TITLE = "Title" # Uppercase T
    ARTIST = "Artist" # Uppercase A
    ALBUM = "Album" # Uppercase A
    # ALARM_FLAG = "alarmflag" # Keep if used
    # PLAYLIST_COUNT = "plicount" # Keep if used
    # PLAYLIST_INDEX = "plicurr" # Keep if used
    VOLUME = "vol" # 0-100
    MUTED = "mute" # "0" or "1"
    # Add any other relevant fields from API 1.03 getPlayerStatusEx

# Device attributes from getStatusEx JSON response
class DeviceAttribute(StrEnum):
    UUID = "uuid" # Primary identifier
    DEVICE_NAME = "DeviceName"
    # GROUP_NAME = "GroupName" # Keep if used
    SSID = "ssid"
    LANGUAGE = "language"
    FIRMWARE = "firmware"
    HARDWARE = "hardware"
    BUILD = "build"
    PROJECT = "project" # Used for manufacturer/model mapping
    # PRIV_PRJ = "priv_prj"
    # PROJECT_BUILD_NAME = "project_build_name"
    RELEASE = "Release" # Often same as firmware
    # TEMP_UUID = "temp_uuid"
    # HIDE_SSID = "hideSSID"
    # SSID_STRATEGY = "SSIDStrategy"
    # BRANCH = "branch"
    # GROUP = "group" # Multiroom group ID?
    # WMRM_VERSION = "wmrm_version"
    INTERNET = "internet" # "1" if connected
    MAC_ADDRESS = "MAC" # Primary MAC
    STA_MAC_ADDRESS = "STA_MAC" # Wi-Fi client MAC
    # COUNTRY_CODE = "CountryCode"
    # COUNTRY_REGION = "CountryRegion"
    NET_STAT = "netstat" # Network status code
    # ESSID = "essid" # Connected Wi-Fi SSID
    APCLI0 = "apcli0" # IP address on Wi-Fi client interface
    ETH0 = "eth0" # IP address on Ethernet interface (if present)
    # ETH2 = "eth2" # Another ethernet interface?
    # RA0 = "ra0" # Wi-Fi AP interface IP?
    # ETH_DHCP = "eth_dhcp"
    # VERSION_UPDATE = "VersionUpdate" # Update status
    NEW_VER = "NewVer" # Available new firmware version
    # SET_DNS_ENABLE = "set_dns_enable"
    MCU_VER = "mcu_ver"
    # MCU_VER_NEW = "mcu_ver_new"
    # DSP_VER = "dsp_ver"
    # DSP_VER_NEW = "dsp_ver_new"
    # DATE = "date"
    # TIME = "time"
    # TIMEZONE = "tz"
    # DST_ENABLE = "dst_enable"
    # REGION = "region"
    # PROMPT_STATUS = "prompt_status"
    # IOT_VER = "iot_ver"
    UPNP_VERSION = "upnp_version" # UPnP stack version?
    # CAP1 = "cap1"
    # CAPABILITY = "capability"
    # LANGUAGES = "languages"
    # STREAMS_ALL = "streams_all"
    # STREAMS = "streams"
    # EXTERNAL = "external"
    PLAYMODE_SUPPORT = "plm_support" # Bitmask of supported InputModes
    PRESET_KEY = "preset_key" # Number of supported presets (e.g., "10")
    SPOTIFY_ACTIVE = "spotify_active" # "1" if Spotify Connect is active
    # LBC_SUPPORT = "lbc_support"
    # PRIVACY_MODE = "privacy_mode"
    # WIFI_CHANNEL = "WifiChannel"
    RSSI = "RSSI" # Wi-Fi signal strength
    # BSSID = "BSSID"
    BATTERY = "battery" # "1" if battery present/charging, "0" otherwise
    BATTERY_PERCENT = "battery_percent" # "0" to "100"
    # SECURE_MODE = "securemode"
    # AUTH = "auth"
    # ENCRYPTION = "encry"
    UPNP_UUID = "upnp_uuid" # Should match 'uuid'
    # UART_PASS_PORT = "uart_pass_port"
    # COMMUNICATION_PORT = "communication_port"
    # WEB_FIRMWARE_UPDATE_HIDE = "web_firmware_update_hide"
    # IGNORE_TALKSTART = "ignore_talkstart"
    # WEB_LOGIN_RESULT = "web_login_result"
    # SILENCE_OTA_TIME = "silenceOTATime"
    # IGNORE_SILENCE_OTA_TIME = "ignore_silenceOTATime"
    # NEW_TUNEIN_PRESET_AND_ALARM = "new_tunein_preset_and_alarm"
    # IHEARTRADIO_NEW = "iheartradio_new"
    # NEW_IHEART_PODCAST = "new_iheart_podcast"
    # TIDAL_VERSION = "tidal_version"
    # SERVICE_VERSION = "service_version"
    ETH_MAC_ADDRESS = "ETH_MAC" # Ethernet MAC
    # SECURITY = "security"
    # SECURITY_VERSION = "security_version"
    # FW_RELEASE_VERSION = "FW_Release_version" # Detailed firmware version
    # PCB_VERSION = "PCB_version"
    # EXPIRED = "expired" # License status?
    BT_MAC = "BT_MAC" # Bluetooth MAC
    # AP_MAC = "AP_MAC" # Wi-Fi AP MAC
    # UPDATE_CHECK_COUNT = "update_check_count"
    # BLE_REMOTE_UPDATE_CHECKED_COUNTER = "BleRemote_update_checked_counter"
    # ALEXA_VER = "alexa_ver"
    # ALEXA_BETA_ENABLE = "alexa_beta_enable"
    # ALEXA_FORCE_BETA_CFG = "alexa_force_beta_cfg"
    # VOLUME_CONTROL = "volume_control" # e.g. "hw" or "sw"
    # WLAN_SNR = "wlanSnr"
    # WLAN_NOISE = "wlanNoise"
    # WLAN_FREQ = "wlanFreq"
    # WLAN_DATA_RATE = "wlanDataRate"
    # OTA_INTERFACE_VER = "ota_interface_ver"
    EQ_SUPPORT = "EQ_support" # "1" if device supports EQ settings
    # AUDIO_CHANNEL_CONFIG = "audio_channel_config" # e.g. "L", "R", "S"
    # APP_TIMEZONE_ID = "app_timezone_id"
    # AVS_TIMEZONE_ID = "avs_timezone_id"
    # TZ_INFO_VER = "tz_info_ver"
    # POWER_MODE = "power_mode"
    # SECURITY_CAPABILITIES = "security_capabilities"


# Multiroom attributes from multiroom:getSlaveList JSON response
class MultiroomAttribute(StrEnum):
    NUM_FOLLOWERS = "slaves" # Number of followers as string
    FOLLOWER_LIST = "slave_list" # Array of follower dicts
    UUID = "uuid" # Follower's UUID (should be UDN)
    IP = "ip" # Follower's IP address
    # Add other fields if present in slave_info dict (e.g., name, status)

# MetaInfo for getMetaInfo command (WiiM specific for rich metadata)
class MetaInfo(StrEnum):
    METADATA = "metaData" # Top-level key in the response

class MetaInfoMetaData(StrEnum):
    # Fields within the 'metaData' object
    ALBUM_TITLE = "album"
    TRACK_TITLE = "title"
    TRACK_SUBTITLE = "subtitle"
    ALBUM_ART = "albumArtURI" # URL to album art
    SAMPLE_RATE = "sampleRate"
    BIT_DEPTH = "bitDepth"
    BIT_RATE = "bitRate"
    TRACK_ID = "trackId"
    # Add other fields like 'duration', 'artist' if present

# AudioOutputHwMode for setAudioOutputHardwareMode / getNewAudioOutputHardwareMode
class AudioOutputHwMode(StrEnum):
    OPTICAL = "1"
    LINE_OUT = "2"
    COAXIAL = "3"
    HEADPHONES = "4" # If supported

# Manufacturer constant (already in manufacturers.py, but good to have here too for SDK use)
MANUFACTURER_WIIM = "Linkplay" # Or "WiiM" if they changed it in device description
