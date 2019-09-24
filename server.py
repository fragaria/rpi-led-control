#!/usr/bin/env python3
import falcon
from driver import apa102
from wsgiref.simple_server import make_server
import time
import json

strip = apa102.APA102(num_led=2, global_brightness=20, mosi=14, sclk=15, order='rbg')

class Leds(object):
    def __init__(self):
        print("led control started")
        strip.clear_strip()
        strip.set_pixel_rgb(0, 20000)

    def on_post(self, req, res):
        data = req.media
        for i in range(0, len(data["leds"])):
            strip.set_pixel_rgb(i, data["leds"][i])
            strip.show()

        print(data)
        return data

app = falcon.API()
leds = Leds()
app.add_route('/', leds)

