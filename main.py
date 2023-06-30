from settings import *
from level import Level
import pygame, sys
from overworld import Overworld
from level import Level
from ui import UI

class Game:
    def __init__(self):
        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        # overworld creation
        self.overworld = Overworld(0, self.max_level, window, self.create_level)    # no brackets because method is being passed around, not called
        self.status = 'overworld'

        # user interface
        self.ui = UI(window)

    # method created in Game class but called in Overworld
    def create_level(self, current_level):
        self.level = Level(current_level, window, self.create_overworld, self.change_coins)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:  # only when player wins
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, window, self.create_level)
        self.status = 'overworld'

    def change_coins(self, amount):
        self.coins += amount

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health, self.max_health)
            self.ui.show_coins(self.coins)

# Pygame setup
pygame.init()

pygame.display.set_caption("Platformer Game")

window = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
# level = Level(level_0, window)  # previous
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
# run = True
# while run:
#     clock.tick(FPS)
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#             break
#
#     #     if event.type == pygame.KEYDOWN:
#     #         if event.key == pygame.K_SPACE and player.jump_count < 2:
#     #             player.jump()
#     # window.fill('grey')
#     # level.run() # previous
#     game.run()
#
#     pygame.display.update()
#
# pygame.quit()
# quit()
