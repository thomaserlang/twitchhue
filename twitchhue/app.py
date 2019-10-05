import requests, phue, time, asyncio, bottom, rgbxy
from config import config, load
from unpack import rfc2812_handler

def get_ip():
    print('Looking for the Hue Bridge')
    r = requests.get('https://discovery.meethue.com')
    if r.status_code == 200:
        data = r.json()
        if not data:
            return
        return data[0]['internalipaddress']
    else:
        return

def bridge_connect():
    b = None
    hue_ip = get_ip()
    if not hue_ip:
        print('Unable to locate a Hue Bridge. Make sure you are on the same network!')
        exit()

    press_message_displayed = False
    print(f'Connecting to Hue Bridge: {hue_ip}')
    while True:
        try:
            b = phue.Bridge(hue_ip)
            b.connect()
            b.get_api()
            break
        except phue.PhueRegistrationException:
            if not press_message_displayed:
                print('Press the button on the Hue Bridge to allow access')
                press_message_displayed = True
            time.sleep(1)
        except:
            raise
    print('Connected to the Hue Bridge')
    return b


bot = bottom.Client(
    host='irc.chat.twitch.tv', 
    port=6697, 
    ssl=True,
)
bot.raw_handlers = [rfc2812_handler(bot)]

@bot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    bot.send('PASS', password='BLANK')
    bot.send('NICK', nick='justinfan32429')

    done, pending = await asyncio.wait(
        [bot.wait("RPL_ENDOFMOTD"),
         bot.wait("ERR_NOMOTD")],
        loop=bot.loop,
        return_when=asyncio.FIRST_COMPLETED
    )

    bot.send_raw('CAP REQ :twitch.tv/tags')
    bot.send_raw('CAP REQ :twitch.tv/commands')
    bot.send_raw('CAP REQ :twitch.tv/membership')

    for c in config['channels']:
        print(f'Joining {c}')
        bot.send('JOIN', channel=f'#{c}')

    if not hasattr(bot, 'bridge'):
        bot.bridge = bridge_connect()

@bot.on('PING')
def keepalive(message, **kwargs):
    bot.send('PONG', message=message)

@bot.on('USERNOTICE')
async def usernotice(**kwargs):
    if kwargs['msg-id'] in ('sub', 'resub', 'subgift', 
        'anonsubgift', 'giftpaidupgrade', 'submysterygift',
        'anonsubmysterygift'):
        run_sub_light()

@bot.on('PRIVMSG')
async def message(message, **kwargs):
    if message in ['!testsub', '!subtest']: 
        if 'moderator' in kwargs['badges'] or 'broadcaster' in kwargs['badges']:
            run_sub_light()

def run_sub_light():
    print('Running sub light')

    light_names = []

    if config['rooms']:
        for r in config['rooms']:
            group = bot.bridge.get_group(r)
            if group:
                light_names.extend([int(i) for i in group['lights']])
            else:
                print(f'Unknown group {r}')

    if config['lights']:
        light_names.extend(config['lights'])

    lights = []    
    for l in light_names:
        lights.append(bot.bridge.get_light(l))

    light_names = [l['name'] for l in lights]


    try:
        converter = rgbxy.Converter()
        for c in config['colors']:        
            d = {
                'on': True, 
            }

            if c.get('color'):
                d['xy'] = converter.hex_to_xy(c['color'].strip('#'))
            if c.get('bri'):
                d['bri'] = int(c['bri'])
            if c.get('ct'):
                d['ct'] = int(c['ct'])

            bot.bridge.set_light(light_names, d)
            time.sleep(1)
    finally:
        # Reset the lights to their prev state
        for l in lights:
            for k in list(l['state'].keys()):
                if not k in ['on', 'bri', 'xy', 'ct']:
                    del l['state'][k]
            bot.bridge.set_light(l['name'], l['state'])


if __name__ == '__main__':
    load()
    bot.loop.create_task(bot.connect())
    bot.loop.run_forever()