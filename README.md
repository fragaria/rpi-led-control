# rpi-led-control

Dockerized REST API for LED control. Available on [Docker Hub](https://hub.docker.com/r/fragaria/rpi-led-control).

To make this work, attach a strip of two (or more) APA102 LEDs to Raspberry Pi GPIO pins:
- GND - GND
- VCC - 5V
- DI (data) - rpi pin 14
- CI (clock) - rpi pin 15

And then run

```sh
docker pull fragaria/rpi-led-control && docker run -d --device /dev/gpiomem:/dev/gpiomem -p 5000:5000 -e NUM_LED=2 -e START_COLOR=red fragaria/rpi-led-control
```

By sending the color values via POST, you can control what colors the LEDs are.

The LED positions are addressed from the start of the cable. 
Values are hexadecimal #rrggbb, #rgb or color name ([list of names](https://github.com/vaab/colour/blob/11f138eb7841d2045160b378a2eec0c2321144c0/colour.py#L52)).

```sh
curl -X POST -d '{"leds":["#ff0000", "blue"]}' -H "Content-Type: application/json" http://10.192.202.91:5000

curl -X GET http://10.192.202.12:5000
# -> {"leds": ["#ffffff", "#0000ff"]}
```
