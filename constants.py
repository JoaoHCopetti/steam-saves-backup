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
    "": "anyplatform/_steam_install_/userdata/:steam_3_account_id/:app_id/",
    "GameInstall": "anyplatform/_steam_library_/steamapps/common/:install_dir/",
    "WinMyDocuments": "windows/_user_profile_/my documents/",
    "WinAppDataLocal": "windows/_user_profile_/appdata/local/",
    "WinAppDataLocalLow": "windows/_user_profile_/appdata/locallow/",
    "WinAppDataRoaming": "windows/_user_profile_/appdata/roaming/",
    "WinSavedGames": "windows/_user_profile_/saved games/",
    "WindowsHome": "windows/_user_profile_/",
    "MacHome": "mac/_home_/",
    "MacAppSupport": "mac/_home_/library/application support/",
    "MacDocuments": "mac/_home_/documents/",
    "LinuxHome": "linux/_home_/",
    "LinuxXdgDataHome": "linux/_xdg_data_home_/",
}
