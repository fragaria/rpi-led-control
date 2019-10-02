# rpi-led-control

Dockerized REST API for LED control

```sh
docker pull fragaria/rpi-led-control && docker run -d --device /dev/gpiomem:/dev/gpiomem -p 5000:5000 -e NUM_LED=2 -e START_COLOR=16711680 fragaria/rpi-led-control
```

By sending the decimal color values via POST, you can control what colors the LEDs are.
For color conversion, you can use [this tool](https://convertingcolors.com/).

The LEDs positions are addressed from the start of the cable. Values are decimal color representation (0-16777215).

```sh
curl -X POST -d '{"leds":[20000, 255]}' -H "Content-Type: application/json" http://10.192.202.91:5000
```

Attach strip of two APA102 leds rpi GPIO pins:
- GND - GND
- VCC - 5V
- DI (data) - rpi pin 14
- CI (clock) - rpi pin 15
