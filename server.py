#!/usr/bin/env python3
import os
import json
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


def get_strip_color(strip, index):
    start_index = 4 * index
    red = strip.leds[start_index + strip.rgb[0]]
    green = strip.leds[start_index + strip.rgb[1]]
    blue = strip.leds[start_index + strip.rgb[2]]
    return (red, green, blue)


def strip_as_rgb(strip):
    res = [0] * NUM_LED
    for c in range(0, NUM_LED):
        red, green, blue = get_strip_color(strip, c)
        print(red, green, blue)
        res[c] = red * 256 * 256 + green * 256 + blue
    return res


class Leds(object):
    def on_post(self, req, res):
        data = req.media
        for i in range(0, len(data["leds"])):
            if i > NUM_LED:
                break
            strip.set_pixel_rgb(i, data["leds"][i])
        strip.show()
        return data

    def on_get(self, req, res):
        res.body = json.dumps({"leds": strip_as_rgb(strip)})

app = falcon.API()
app.add_route("/", Leds())
