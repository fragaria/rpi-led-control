#!/usr/bin/env python3
import os
import json
import falcon
from driver import apa102
from colour import Color

NUM_LED = int(os.environ.get("NUM_LED", 2))
DATA_PIN = int(os.environ.get("DATA_PIN", 14))
CLK_PIN = int(os.environ.get("CLK_PIN", 15))
START_COLOR = int(os.environ.get("START_COLOR", 16711680))
BRIGHTNESS = int(os.environ.get("BRIGHTNESS", 31))


class Apa102(apa102.APA102):
    @staticmethod
    def _fd(c):
        return int(c * 256)

    @staticmethod
    def _df(c):
        return c/256

    def set_pixel_f(self, index, r, g, b):
        return super().set_pixel(index, self._fd(r), self._fd(g), self._fd(b))

    def set_pixel_color(self, index, color):
        return self.set_pixel_f(index, color.r, color.g, color.b)

    def get_strip_color(self, index):
        start_index = 4 * index
        red = strip.leds[start_index + strip.rgb[0]]
        green = strip.leds[start_index + strip.rgb[1]]
        blue = strip.leds[start_index + strip.rgb[2]]
        return Color(rgb=(self._df(red), self._df(green), self._df(blue)))

    def as_hex(self):
        res = [0] * NUM_LED
        for i in range(0, NUM_LED):
            color = self.get_strip_color(i)
            res[i] = color.hex_l
        return res


strip = Apa102(
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
            c = Color(data["leds"][i])
            strip.set_pixel_color(i, c)
        strip.show()
        return data

    def on_get(self, req, res):
        res.body = json.dumps({"leds": strip.as_hex()})


app = falcon.API()
app.add_route("/", Leds())
