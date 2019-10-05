import requests, phue, time, asyncio, bottom
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
    if kwargs['msg-id'] not in ('sub', 'resub', 'subgift', 
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
    for l in bot.bridge.lights:
        l.alert = 'select'

if __name__ == '__main__':
    load()
    bot.loop.create_task(bot.connect())
    bot.loop.run_forever()