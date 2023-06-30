import pygame
from support import import_folder


# needed for jump and land because animations are not looped for these
# the animateion will be terminated once shown (unlike run)
class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5

        if type == 'jump':
            self.frames = import_folder('Treasure Hunters/Treasure Hunters/dust_particles/jump')
        if type == 'land':
            self.frames = import_folder('Treasure Hunters/Treasure Hunters/dust_particles/land')

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):    # only runs for number of frames
            self.kill()     # destroy sprite after animation has been shown
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):      # x_shift responsible for when scrolling through screen
        self.animate()
        self.rect.x += x_shift