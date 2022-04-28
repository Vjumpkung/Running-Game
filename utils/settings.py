import json
from utils.savegenerator import SaveGenerator

sg = SaveGenerator()

# read config
with open("settings.json") as f:
    r = json.load(f)

# you can customize title
class Settings:
    def __init__(self):
        # default game size
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.URL = r['URL']
        self.NAME = "Running Game"
        self.USERNAME = r['USERNAME']
        self.PASSWORD = r['PASSWORD']
                
# get framerate in game
def get_fps(fpsfont, clock):
    return fpsfont.render(f'{clock.get_fps():.0f}', False, 'Black')