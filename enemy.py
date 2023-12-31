import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'Treasure Hunters/Treasure Hunters/enemy/run') # flipped in the future
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 6)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0: # right
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1    # speed reversed

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()