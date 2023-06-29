import pygame

class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('Treasure Hunters/Treasure Hunters/ui/health_bar.png')

        # coins