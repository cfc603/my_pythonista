import random
import time

import console
import location
import ui


COLORS = ["red", "blue", "green"]

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


@ui.in_background
def gps_logger():
    while logging:
        location.start_updates()

        # giving time allows for more accuracy?
        time.sleep(1)

        loc = location.get_location()
        console.hud_alert("Logging...", duration=0.5)
        location.stop_updates()
        print(loc)


if __name__ == "__main__":
    console.clear()
    console.alert("GPS Logging", "Start GPS Logging?", "Okay")
    console.hud_alert("Starting...")

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
