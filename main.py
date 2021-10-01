import json
import os
import random
import requests
import tarfile
import time

import console
import keychain
import location
import ui

from objc_util import on_main_thread
from pathlib import Path


API_URL = ""
API_TOKEN = keychain.get_password("gps_logging", "api")
COLORS = ["red", "blue", "green"]
CWD = Path(__file__).parent
DATA_DIR = Path(CWD, "data")
LOCATION_DATA_FILE = Path(DATA_DIR, "pending_location_data.json")

logging = False


class MainView(ui.View):

    def update(self):
        self.background_color = random.choice(COLORS)

    def will_close(self):
        location_data_archive()
        archive_submit()
        on_main_thread(console.set_idle_timer_disabled)(False)


@ui.in_background
def archive_runner():
    while logging:
        time.sleep(10)
        archive_submit()


def archive_submit():
    for archive in DATA_DIR.glob("location_data_*.tar.gz"):
        with open(archive, "rb") as open_file:
            response = requests.post(
                API_URL,
                files={archive.name: open_file},
                headers={"Authorization": f"Token {API_TOKEN}"}
            )
            print(response)


def disable_logging(sender):
    global logging
    logging = False
    sender.superview.close()


def enable_logging():
    global logging
    logging = True
    gps_logger()


def location_data_archive():
    archived = list(DATA_DIR.glob("location_data_*.tar.gz"))
    archive_file = Path(DATA_DIR, f"location_data_{len(archived) + 1}.tar.gz")
    with tarfile.open(archive_file, "w:gz") as open_tarfile:
        open_tarfile.add(LOCATION_DATA_FILE)

    os.remove(LOCATION_DATA_FILE)


def location_data_save(data):
    """Get or create data file and append new data"""
    if LOCATION_DATA_FILE.exists():
        with open(LOCATION_DATA_FILE) as of:
            existing_data = json.load(of)
    else:
        existing_data = []
    existing_data.append(data)

    with open(LOCATION_DATA_FILE, "w") as of:
        json.dump(existing_data, of)

    # once file has 600 entries, rename it to be sent to API
    if len(existing_data) == 600:
        location_data_archive()


@ui.in_background
def gps_logger():
    while logging:
        location.start_updates()

        # giving time allows for more accuracy?
        time.sleep(1)

        loc = location.get_location()
        location.stop_updates()
        location_data_save(loc)


if __name__ == "__main__":
    console.clear()
    console.alert("GPS Logging", "Start GPS Logging?", "Okay")
    console.hud_alert("Starting...")
    on_main_thread(console.set_idle_timer_disabled)(True)

    # enable background tasks
    enable_logging()
    archive_runner()

    # Create view changing color display and button to cancel
    view = MainView()
    view.name = "GPS Logging"
    view.background_color = "white"
    view.update_interval = 5

    button = ui.Button(title="Stop GPS Logging")
    button.center = (view.width * 0.5, view.height * 0.5)
    button.flex = 'LRTB'
    button.action = disable_logging

    view.add_subview(button)
    view.present('full_screen')
