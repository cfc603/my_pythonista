import random
import time

import console
import location
import ui


logging = False


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
        location.stop_updates()
        print(loc)


@ui.in_background
def update_view_color():
    while logging:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        view.background_color = (r, g, b, 1.0)
        time.sleep(5)


if __name__ == "__main__":
    console.clear()
    console.alert("GPS Logging", "Start GPS Logging?", "Okay")
    console.hud_alert("Starting...")

    # enable background tasks
    enable_logging()
    update_view_color()

    # Create view changing color display and button to cancel
    view = ui.View()
    view.name = "GPS Logging"
    view.background_color = "white"

    button = ui.Button(title="Stop GPS Logging")
    button.center = (view.width * 0.5, view.height * 0.5)
    button.flex = 'LRTB'
    button.action = disable_logging

    view.add_subview(button)
    view.present('sheet')
