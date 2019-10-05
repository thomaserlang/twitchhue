# Twitch Hue

Proof of concept. Sends an `alert` to all your Hue lights when somebody subs.

Create a config file called `twitchhue.yaml`. Place it next to the executable. 

Example config:

```yaml
channels:
    - erleperle
    - erletest
rooms:
    - Dining room
lights:
    - Bedroom ceiling
colors:
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
  -
    color: 2b59ff
    bri: 255
  -
    color: ff0303
    bri: 255
```
