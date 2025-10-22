STEAM_REMOTE_STORAGE_URL = "https://store.steampowered.com/account/remotestorage"

IGNORE_APP_IDS = [
    "7",  # Steam Client
    "764",  #  Steam Cloud - User Logs
    "744350",  # Steam Chat Images
    "241100",  #  Steam Input Configs
    "2371090",  #  Steam Game Notes
]

# https://partner.steamgames.com/doc/features/cloud#setup
""" 
    The folders "", "GameInstall" and "WindowsHome" 
    aren't officially documented. I'm using steamdb.info as reference.
"""
SAVE_GAMES_PATHS = {
    "": "AnyPlatform/_STEAM_INSTALL_/userdata/:steam_3_account_id/:app_id/",
    "GameInstall": "AnyPlatform/_STEAM_LIBRARY_/steamapps/common/:install_dir/",
    "WinMyDocuments": "Windows/_USER_PROFILE_/My Documents/",
    "WinAppDataLocal": "Windows/_USER_PROFILE_/AppData/Local/",
    "WinAppDataLocalLow": "Windows/_USER_PROFILE_/AppData/LocalLow/",
    "WinAppDataRoaming": "Windows/_USER_PROFILE_/AppData/Roaming/",
    "WinSavedGames": "Windows/_USER_PROFILE_/Saved Games/",
    "WindowsHome": "Windows/_USER_PROFILE_/",
    "MacHome": "Mac/_HOME_/",
    "MacAppSupport": "Mac/_HOME_/Library/Application Support",
    "MacDocuments": "Mac/_HOME_/Documents/",
    "LinuxHome": "Linux/_HOME_/",
    "LinuxXdgDataHome": "Linux/_XDG_DATA_HOME_/",
}
