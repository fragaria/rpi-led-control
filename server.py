#!/usr/bin/env python3
import os
import falcon
from driver import apa102

NUM_LED = int(os.environ.get("NUM_LED", 2))
DATA_PIN = int(os.environ.get("DATA_PIN", 14))
CLK_PIN = int(os.environ.get("CLK_PIN", 15))
START_COLOR = int(os.environ.get("START_COLOR", 16711680))
BRIGHTNESS = int(os.environ.get("BRIGHTNESS", 31))

strip = apa102.APA102(
    num_led=NUM_LED,
    global_brightness=BRIGHTNESS,
    mosi=DATA_PIN,
    sclk=CLK_PIN,
    order="rbg",
)
strip.clear_strip()
for i in range(0, NUM_LED):
    strip.set_pixel_rgb(i, START_COLOR)
strip.show()


class Leds(object):
    def on_post(self, req, res):
        data = req.media
        for i in range(0, len(data["leds"])):
            if i > NUM_LED:
                break
            strip.set_pixel_rgb(i, data["leds"][i])
        strip.show()
        return data


app = falcon.API()
app.add_route("/", Leds())
