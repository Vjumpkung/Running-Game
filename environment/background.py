import pygame
from utils.settings import Settings

settings = Settings()

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT


class Background:

    '''
        Create some beautiful background here.
    '''

    def __init__(self):

        # drawing sky
        self.sky_surface = pygame.Surface((WIDTH, HEIGHT))

        # drawing ground
        self.ground_surface = pygame.Surface((WIDTH, 180))

    # Set sky color
    def SetSkyColor(self, color):
        self.sky_surface.fill(color)

    # Set ground color
    def SetGroundColor(self, color):
        self.ground_surface.fill(color)
