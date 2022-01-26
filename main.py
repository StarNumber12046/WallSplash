import os
import time
import threading
import requests
import ctypes
import sys
import os
from pyunsplash import PyUnsplash
import random
import win10toast
import json

notifications = win10toast.ToastNotifier()


def everything_exists():
    if not "config.json" in os.listdir("."):
        print("config.json not found!\n")
        return False
    if not "grinning.ico" in os.listdir("icons"):
        print("icons folder not found!\n")
        return False
    return True


if not everything_exists():
    json_config = requests.get(
        "https://raw.githubusercontent.com/StarNumber12046/WallSplash/main/config.standard.json"
    )
    f = open("config.json", "wb")
    f.write(json_config.content)
    f.close()
    try:

        os.mkdir("icons")
    except:
        pass
    grinning = requests.get(
        "https://github.com/StarNumber12046/WallSplash/blob/main/icons/grinning.ico?raw=true"
    )
    f = open("icons/grinning.ico", "wb")
    f.write(grinning.content)
    f.close()
    growing = requests.get(
        "https://github.com/StarNumber12046/WallSplash/blob/main/icons/growing.ico?raw=true"
    )
    f = open("icons/growing.ico", "wb")
    f.write(grinning.content)
    f.close()
    exit(
        "Insert your API key from Unsplash in the config.json and restart the program!"
    )


f = open("config.json", "r")
config = json.load(f)
f.close()


SPI_SETDESKWALLPAPER = 20
UNSPLASH_ACCESS_KEY = config["api_key"]


try:
    pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)

except:
    notifications.show_toast(
        "Error!",
        "The API key is not valid",
        icon_path="icons/growing.ico",
        duration=5,
        threaded=True,
    )
    exit()
WAIT_SECONDS = int(config["change_time"]) * 60


def is_64bit():
    return sys.maxsize > 2 ** 32


def change_background():
    print(f"Wallpaper change started at {time.ctime()}")
    query = random.choice(config["categories"])
    print(f"Query for wallpaper: {query}")
    photos = pu.photos(type_="random", count=1, featured=True, query=query)

    [photo] = photos.entries

    print(photo.get_attribution())
    with open("wallpaper.png", "wb") as f:
        response = requests.get(photo.link_download, allow_redirects=True)
        f.write(response.content)
    path_to_file = os.path.join(os.getcwd(), "wallpaper.png")
    SPI_SETDESKWALLPAPER = 20
    try:
        notifications.show_toast(
            "Wallpaper changed!",
            f"{photo.get_attribution()}",
            icon_path="icons/grinning.ico",
            duration=5,
            threaded=True,
        )
        if is_64bit():
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, path_to_file, 0
            )
        else:
            ctypes.windll.user32.SystemParametersInfoA(
                SPI_SETDESKWALLPAPER, 0, path_to_file, 0
            )

    except:
        notifications.show_toast(
            "Wallpaper not changed!",
            f"{photo.get_attribution()}",
            icon_path="icons/growing.ico",
            duration=5,
            threaded=True,
        )
    time.sleep(WAIT_SECONDS)


if __name__ == "__main__":
    while True:
        change_background()
