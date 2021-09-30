import json
import random
import time

import console
import location
import ui

from objc_util import on_main_thread
from pathlib import Path


COLORS = ["red", "blue", "green"]
CWD = Path(__file__).parent
DATA_DIR = Path(CWD, "data")

logging = False


class MainView(ui.View):

    def update(self):
        self.background_color = random.choice(COLORS)


def disable_logging(sender):
    global logging
    logging = False
    sender.superview.close()


def enable_logging():
    global logging
    logging = True
    gps_logger()


def save_location_data(data):
    """Get or create data file and append new data"""
    location_data = Path(DATA_DIR, "pending_location_data.json")
    if location_data.exists():
        with open(location_data) as of:
            existing_data = json.load(of)
    else:
        existing_data = []
    existing_data.append(data)

    with open(location_data, "w") as of:
        json.dump(existing_data, of)

    # once file has 600 entries, rename it to be sent to API
    if len(existing_data) == 600:
        archived = list(DATA_DIR.glob("location_data_*.json"))
        location_data.rename(
            Path(DATA_DIR, f"location_data_{len(archived)+1}.json")
        )


@ui.in_background
def gps_logger():
    while logging:
        location.start_updates()

        # giving time allows for more accuracy?
        time.sleep(1)

        loc = location.get_location()
        location.stop_updates()
        save_location_data(loc)


if __name__ == "__main__":
    console.clear()
    console.alert("GPS Logging", "Start GPS Logging?", "Okay")
    console.hud_alert("Starting...")
    on_main_thread(console.set_idle_timer_disabled)(True)

    # enable background tasks
    enable_logging()

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
