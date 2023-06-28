from settings import *
from level import Level
from game_data import level_0
import pygame
from overworld import Overworld

class Game:
    def __init__(self):
        self.max_level = 2
        self.overworld = Overworld(1, self.max_level, window)

    def run(self):
        self.overworld.run()

# Pygame setup
pygame.init()

pygame.display.set_caption("Platformer Game")

window = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
# level = Level(level_0, window)  # previous
game = Game()

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_SPACE and player.jump_count < 2:
    #             player.jump()
    # window.fill('grey')
    # level.run() # previous
    game.run()

    pygame.display.update()

pygame.quit()
quit()
