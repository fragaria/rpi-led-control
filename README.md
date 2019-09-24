# rpi-led-control

Dockerized REST API for LED control

By sending the decimal color values via POST, you can control what colors the LEDs are.
For color conversion, you can use [this tool](https://convertingcolors.com/).

The LEDs positions are addressed from the start of the cable

```sh
curl -X POST -d '{"leds":[20000, 255]}' -H "Content-Type: application/json" http://10.192.202.91:5000
```
