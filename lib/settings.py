import configparser


Config = configparser.ConfigParser()


def load_settings():
    Config.read("saved/settings.ini")
    Config.set('Settings','JSON', get_JSON())
    Config.set('Settings','Local', get_Local())

def save_settings():
    with open('saved/settings.ini', 'w') as configfile:
        Config.write(configfile)

def get_JSON():
    return Config.get('Settings', 'JSON')

def set_JSON(inp):
    Config.set('Settings','JSON', str(inp))
    save_settings()

def get_Local():
    return Config.get('Settings', 'Local')

def set_Local(inp):
    Config.set('Settings','Local', str(inp))
    save_settings()