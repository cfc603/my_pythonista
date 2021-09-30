import time

import console
import location
import ui


logging = False


def enable_logging(sender):
    global logging
    logging = sender.value
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


if __name__ == "__main__":
    console.clear()
    console.alert("GPS Logging", "Start GPS Logging?", "Okay")
    console.hud_alert("Starting...")

    # Create view changing color display and button to cancel
    view = ui.View()
    view.name = "GPS Logging"
    view.background_color = "white"

    button = ui.Button(title="Stop GPS Logging")
    button.center = (view.width * 0.5, view.height * 0.5)
    button.flex = 'LRTB'
    button.action = enable_logging

    view.add_subview(button)
    view.present('sheet')
