#!/usr/bin/env python3
import falcon
from driver import apa102


strip = apa102.APA102(num_led=2, global_brightness=20, mosi=14, sclk=15, order="rbg")
strip.clear_strip()


class Leds(object):
    def on_post(self, req, res):
        data = req.media
        for i in range(0, len(data["leds"])):
            strip.set_pixel_rgb(i, data["leds"][i])
            strip.show()
        return data


app = falcon.API()
app.add_route("/", Leds())
