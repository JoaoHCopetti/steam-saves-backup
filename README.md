# steam-saves-backup

A Python script that scrap https://store.steampowered.com/account/remotestorage to download all files locally, respecting the original folder structure.

## Summary
- [Motivation](#motivation)
- [How it works](#how-it-works)
- [How to use it](#how-to-use-it)
- [Directory structure](#directory-structure)
- [Known issues](#known-issues)
- [TODO](#todo)
- [Contributing](#contributing)

## Motivation<a name="motivation"></a>
Recently I've decided to download DRM-free versions of my Steam games (from GOG), but I wanted my old save files from my Steam games.
While Steam provides a dedicated page to download all of it, there's a few issues:
- Downloading from their webiste won't keep the original folder structure. The save file is named as `dir1_subdir1_subdir2_savefile` instead of `dir1/subdir1/subdir2/savefile` you'd need to rename and create every folder manually, prone to errors
- The save file root folder isn't provided. I used the table described on https://partner.steamgames.com/doc/features/cloud#setup, plus some undocumented folders from https://steamdb.info
- Some games may have more than 100 save files, downloading them individually and sorting all of it would be a chore

## How it works<a name="how-it-works"></a>
- Scraps https://store.steampowered.com/account/remotestorage for the main page of each game
- Scraps each game page, parsing the folder structure correctly (supports pagination)
- Makes a new directory in the current directory called `save-files`, where all the save files will be stored
- Store all save files respecting the original structure
- Real paths are named as reference only. Ex.: `C:\Users\User Name` is `windows/_user_profile_`
- You should consult https://www.pcgamingwiki.com/ game page, for example, if you're migrating from Steam to GOG, you might need to move your save files to the GOG related directory
  - Take [Rise of the Tomb Rider (pcgamewiki)](https://www.pcgamingwiki.com/wiki/Rise_of_the_Tomb_Raider#Save_game_data_location) for example, you'd need to copy the content of:
    - `<Steam-folder>\userdata\<user-id>\391220\remote\` (which this script generates in `anyplatform/_steam_install_/userdata/<user-id>/391220/remote`)
    - to:
    - `%LOCALAPPDATA%\GOG.com\Galaxy\Applications\58668848197088414\Storage\Shared\Files\`

## How to use it<a name="#how-to-use-it"></a>
It only requires Python 3 and two modules: [requests](https://pypi.org/project/requests/) and [beautifulsoup](https://pypi.org/project/BeautifulSoup/). For Windows, you should use PowerShell to execute the following commands.

- Clone the repo (or download the .zip directly from this page, then extract):
```bash
git clone https://github.com/JoaoHCopetti/steam-saves-backup.git
```

- Enter into the directory
```bash
cd steam-saves-backup
```
- Create a Python virtual environment
```bash
python -m venv .venv
```

- Install the required dependencies
```bash
# Linux
./.venv/bin/pip install -r requirements.txt

# Windows
.\.venv\Scripts\pip.exe install -r .\requirements.txt
```

- Now we'll use your auth session cookie, you need to login in your account and copy your session cookies, don't worry, your cookies will only be used to authenticate in the remote storage pages. You can check the script by yourself (it's short)

<details>
  <summary>
    INSTRUCTIONS FOR FIREFOX
  </summary>
  
  - Access https://store.steampowered.com
  - Login in your account (skip if you're logged already)
  - Open the DevTools (F12)
  - Go to Network tab, make sure "All" is selected
  <img width="1288" height="484" alt="image" src="https://github.com/user-attachments/assets/4a28af35-3408-4ee8-ac1f-c1912d244ecf" />
  
  - Refresh the page with DevTools open
  - Click on the very first item of this list (you might need to scroll up)
  - It'll open a new panel in the right called `Headers`
  - Scroll down a little until you see `Cookie:`
  - Right click in the value and `Copy Value`
  <img width="1079" height="532" alt="image" src="https://github.com/user-attachments/assets/d6827642-be50-4934-b08c-4fc899562cb8" />
</details>

<details>
  <summary>
    INSTRUCTIONS FOR CHROME
  </summary>
  
  - Access https://store.steampowered.com
  - Login in your account (skip if you're logged already)
  - Open the DevTools (F12)
  - Go to Network tab, make sure "All" is selected
<img width="1293" height="431" alt="image" src="https://github.com/user-attachments/assets/ff038ad8-5004-4743-8a28-ee6cc2141d4f" />

   - Refresh the page with DevTools open
   - Click on the very first item of this list (you might need to scroll up)
   - It'll open a new panel in the right called `Headers`
   - Scroll down a little until you see `Cookie:`
   - Double click the cookie value, then right click and copy it
<img width="1392" height="721" alt="image" src="https://github.com/user-attachments/assets/d39f381d-7174-49db-89dd-3b35961342db" />

</details>

- Paste the cookie value in the project file `_paste_your_cookie_here.txt` and save it
- Run the script:
```
# Linux
./.venv/bin/python main.py

# Windows
.\.venv\Scripts\python.exe .\main.py
```

It'll start download all your remote save files to `save-files` folder in the project directory

## Directory structure<a name="#directory-structure"></a>
The script might create 4 main directories:
- `anyplatform`: It's for save-files independent of platform (Windows, Linux or Mac)
  - `_steam_install_`: The Steam Client installation directory (not your games library)
  - `_steam_library_`: This is the Steam games library
- `linux`: For native Linux games (not using Proton)
  - `_home_`: This is your home folder (`echo $HOME`)
  - `_xdg_data_home_`: Defaults to `$HOME/.local/share` (according to Arch wiki: https://wiki.archlinux.org/title/XDG_Base_Directory)
- `windows`: For save games exclusive to Windows (or Proton/Wine)
   - `_user_profile_`: This is your Windows user profile, usually in `C:\Users\User Name\`
- `mac`: For save games exclusive to Mac

Note that the folder names are just a reference, not the real path, you should copy and paste to the real path of your OS accordingly, for example, in Windows, you'd copy the contents of `anyplatform/_steam_install_/` to `C:\Program Files (x86)\Steam`

## Known issues<a name="known-issues"></a>
- For any save game under `save-files/anyplatform/_steam_library_/steamapps/common/` you might need to rename it to the correct install dir name, you can find the correct name in the https://steamdb.info page of your game, in "Configuration" side tab. This is needed because I can't figure out where to pull the official install dir of each game, and steamdb doesn't allow scrapping, so I just named it same as the game name.
<details>
  <summary>See here</summary>
  https://steamdb.info/app/70/config/
  <img width="924" height="570" alt="image" src="https://github.com/user-attachments/assets/7c2a73c3-c112-4e95-b153-f04a673da3b7" />
</details>

- I don't know if the Steam remote storage page has pagination, if it does, it will just scrap the first page, you can change the variable `STEAM_REMOTE_STORAGE_URL` of `constants.py` to a different URL to scrap other pages, I didn't handle this because my account doesn't seems to have enough save files for pagination, so I can't test it.

## TODO<a name="todo"></a>
- [ ] Fix installdir path
- [ ] Provide CLI to choose specific games
- [ ] Implement Steam OAuth and remove cookie based auth
- [ ] Automated tests

## Contributing<a name="#contributing"></a>
If you wish to fork this or anything, don't forget to mark the file `_paste_your_cookie_here.txt` as `assume-unchaged` after cloning, so you don't push your auth cookie to some remote repo by mistake:
```
git update-index --assume-unchanged _paste_your_cookie_here.txt
```
This will make changes to this file not be detected by git.







