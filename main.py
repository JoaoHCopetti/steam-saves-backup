import sys
import os
import requests
from bs4 import BeautifulSoup
import constants

with open("_paste_your_cookie_here.txt", encoding="utf-8") as cookie_file:
    COOKIE = cookie_file.read()

SAVE_FILES_FOLDER = "save-files/"
HEADERS = {"Cookie": COOKIE}


def main():
    storage_request = requests.get(
        constants.STEAM_REMOTE_STORAGE_URL, headers=HEADERS, timeout=10
    )

    urls = parse_urls(storage_request.content)
    valid_urls = remove_invalid_urls(urls)
    steam_3_account_id = get_steam_3_account_id(storage_request.text)

    for url in valid_urls:
        bs_saves_page = BeautifulSoup(
            requests.get(url, headers=HEADERS, timeout=10).text,
            "html.parser",
        )
        app_id = get_url_param(url, "appid")
        game_name = bs_saves_page.select_one("#main_content > h2").get_text().strip()

        save_files = fetch_all_saves_files(bs_saves_page)

        store_save_files(save_files, app_id, steam_3_account_id, game_name)


def parse_urls(request_content):
    game_urls = []
    sp_remote = BeautifulSoup(request_content, "html.parser")

    for anchor_el in sp_remote.select("table.accountTable a"):
        game_url = anchor_el.get("href")
        game_urls.append(game_url)

    return game_urls


def remove_invalid_urls(remote_urls):
    valid_urls = remote_urls.copy()

    for remote_url in valid_urls:
        url_appid = get_url_param(remote_url, "appid")

        if url_appid in constants.IGNORE_APP_IDS:
            valid_urls.remove(remote_url)

    return valid_urls


def get_steam_3_account_id(content):
    """
    The Steam 3 Account ID is shown in the page source code,
    just after "accountid&quot;:" and before ",&quot;account_name",
    but it's unsafe and might change.
    We can ask user input to type its own ID if this stop working.
    """
    return content.split("accountid&quot;:")[1].split(",&quot;account_name")[0]


def get_root_folder(folder):
    valid_folders = constants.SAVE_GAMES_PATHS.keys()

    if folder not in valid_folders:
        print("Not supported root folder: " + folder)
        return None

    return constants.SAVE_GAMES_PATHS[folder]


def format_saves_data(bs_saves_page):
    items = []

    for table_row in bs_saves_page.select("tbody tr"):
        items.append(
            {
                "folder": table_row.select_one(":nth-child(1)").get_text().strip(),
                "filepath": table_row.select_one(":nth-child(2)").get_text().strip(),
                "download_url": table_row.select_one(":nth-child(5) a").get("href"),
                "size": table_row.select_one(":nth-child(3)").get_text().strip(),
            }
        )

    return items


def next_page_url(bs_saves_page):
    next_div = bs_saves_page.select_one(
        '#main_content a[href*="index"]:-soup-contains("next")'
    )

    if next_div is None:
        return False

    return next_div.get("href")


def get_url_param(url, param):
    query_params = url.split("?")[1].split("&")
    params = {}

    for query_param in query_params:
        key, value = query_param.split("=")
        params[key] = value

    return params[param]


def fetch_all_saves_files(bs_saves_page):
    fetch_more = True
    formatted_saves_data = []
    bs_page = bs_saves_page

    while fetch_more:
        formatted_saves_data.append(format_saves_data(bs_page))

        next_page = next_page_url(bs_page)

        if next_page:
            bs_page = BeautifulSoup(
                requests.get(next_page, headers=HEADERS, timeout=10).text,
                "html.parser",
            )
        else:
            fetch_more = False

    return [item for sublist in formatted_saves_data for item in sublist]


def store_save_files(save_files, app_id, steam_3_account_id, game_name):
    os.makedirs(SAVE_FILES_FOLDER, exist_ok=True)

    for index, file in enumerate(save_files):
        root_folder = get_root_folder(file["folder"])

        if root_folder is None:
            print("Skipping " + file["filepath"] + "\n")
            continue

        filepath = format_filepath(
            root_folder,
            file,
            {
                ":steam_3_account_id": steam_3_account_id,
                ":app_id": app_id,
                ":install_dir": game_name_for_windows(game_name),
            },
        )

        print(f"[FILEPATH] {filepath}")

        if os.path.isfile(filepath):
            print("[ALREADY EXISTS, SKIPPING]\n")
        else:
            print(f"[FETCHING {index + 1}/{len(save_files)}] {file["size"]}")
            fetch_and_store_file(file["download_url"], filepath)


def game_name_for_windows(game_name):
    """
    Some game names contains invalid characters for Windows folder structure.
    I'm guessing the "InstallDir" of the game based on the name showed in the
    Steam page, but the correct way is to fetch the "installdir" value,
    as showed in steamdb.info: https://steamdb.info/app/70/config/.
    Even tho, I can't figure out where to find this value and steamdb doesn't
    allow scrapping.
    """
    return (
        game_name.replace("<", "")
        .replace(">", "")
        .replace(":", "")
        .replace('"', "")
        .replace("/", "")
        .replace("\\", "")
        .replace("|", "")
        .replace("?", "")
        .replace("*", "")
    )


def format_filepath(root_folder, file, replacements):
    filepath = SAVE_FILES_FOLDER + root_folder + file["filepath"]

    for key, value in replacements.items():
        filepath = filepath.replace(key, value)

    path = os.path.dirname(filepath)
    filename = os.path.basename(filepath)

    # Windows filesystem is case insensitive
    # This will avoid duplicated folders if ran in Unix-like: My Games, my Games, My games
    # While on Windows it'll accept fine if you paste it, independent of folder case
    if "Windows" in path:
        return path.lower() + filename

    return path + filename


def fetch_and_store_file(url, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    file_response = requests.get(url, headers=HEADERS, timeout=10)

    with open(filepath, "wb") as file:
        file.write(file_response.content)

    print("[SUCCESS]\n")


if __name__ == "__main__":
    main()
