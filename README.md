# Twitch Hue

Change the color of your lights when somebody subs.

Create a config file called `twitchhue.yaml`. Place it next to the executable.  
Download it from [here](https://github.com/thomaserlang/twitchhue/releases).

Example config:

```yaml
channels:
    - somechannel
rooms:
    - Dining room
lights:
    - Bedroom ceiling
interval: 0.5 # number of seconds between each color change
colors:
  -
    color: 2b59ff # RGB
    bri: 255      # Brightness
  -
    color: ff0303
    bri: 255
  -
    color: 2b59ff
    bri: 255
  -
    color: ff0303
    bri: 255
  -
    color: 2b59ff
    bri: 255
  -
    color: ff0303
    bri: 255
  -
    color: 2b59ff
    bri: 255
  -
    color: ff0303
    bri: 255
  -
    color: 2b59ff
    bri: 255
  -
    color: ff0303
    bri: 255
```
