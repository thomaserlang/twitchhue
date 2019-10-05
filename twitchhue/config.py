import os, yaml

config = {
    'channels': [],
    'rooms': [],
    'lights': [],
    'interval': 1,
    'colors': [
        {
            'color': '2b59ff',
            'bri': 255,
        },
        {
            'color': 'ff0303',
            'bri': 255,
        },
        {
            'color': '2b59ff',
            'bri': 255,
        },
        {
            'color': 'ff0303',
            'bri': 255,
        },        
        {
            'color': '2b59ff',
            'bri': 255,
        },
        {
            'color': 'ff0303',
            'bri': 255,
        },
        {
            'color': '2b59ff',
            'bri': 255,
        },
        {
            'color': 'ff0303',
            'bri': 255,
        },
        {
            'color': '2b59ff',
            'bri': 255,
        },
        {
            'color': 'ff0303',
            'bri': 255,
        },
    ]
}

def load(path=None):
    default_paths = [
        '~/twitchhue.yaml',
        './twitchhue.yaml',
        '../twitchhue.yaml',
        '/etc/twitchhue/twitchhue.yaml',
        '/etc/twitchhue.yaml',
    ]
    if not path:
        path = os.environ.get('TWITCHHUE_CONFIG', None)
        if not path:
            for p in default_paths:
                p = os.path.expanduser(p)
                if os.path.isfile(p):
                    path = p
                    break
    if not path:
        raise Exception('No config file specified.')
    if not os.path.isfile(path):
        raise Exception('Config: "{}" could not be found.'.format(path))
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.BaseLoader)
    for key in data:
        if key in config:
            if isinstance(config[key], dict):
                config[key].update(data[key])
            else:
                config[key] = data[key]