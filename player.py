import pygame
from os.path import join
from support import import_folder
from settings import FPS
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles, change_health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0        # animation frame
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)    # actual sprite rect (follows self.collision_rect)/used for coins/enemies

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (50, self.rect.height)) # for rect around character only (without sword)

        # player status
        self.status = 'idle'   # default
        # self.jump_count = 0
        # self.fall_count = 0
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # health management
        self.change_health = change_health
        self.invincible = False     # needed to set timer for decrease in player health
        self.invincibility_duration = 500
        self.hurt_time = 0

    # def jump(self):
    #     self.direction.y = self.jump_speed
    #     self.jump_count += 1
    #     # # self.moving = False
    #     # if self.jump_count == 1:  # for first jump
    #     #     self.fall_count = 0  # accumulated gravity eliminated
    #     # print(self.jump_count)
    #
    # # new (try for jump)
    # def landed(self):
    #     self.fall_count = 0
    #     self.jump_count = 0

    # # imports animation states (old)
    # def import_character_assets(self):
    #     character_path = 'assets/MainCharacters/MaskDude/'
    #     self.animations = {'double_jump': [], 'fall': [], 'hit': [], 'idle': [],
    #                        'jump': [], 'run': [], 'wall_jump': []}
    #
    #     for animation in self.animations.keys():
    #         full_path = character_path + animation + '.png'
    #         self.animations[animation] = load_sprite_sheets(full_path)

    def import_character_assets(self):
        character_path = 'Treasure Hunters/Treasure Hunters/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_particles = import_folder('Treasure Hunters/Treasure Hunters/dust_particles/run')

    # animate based on player movement
    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):  # loops over range of animation
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft   # rect follows collision_rect
        else:
            flipped_image = pygame.transform.flip(image, True, False)       # image, x-axis, y-axis
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()   # 0 or 255
            self.image.set_alpha(alpha)     # setting transparency
        else:
            self.image.set_alpha(255)   # full transparency

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]     # getting frames of dust particles

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)    # dust particles spawned on bottom left of player
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)   # True horizontal flip
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    # # movement based on input keys (old)
    # def get_input(self):
    #     keys = pygame.key.get_pressed()
    #
    #     if keys[pygame.K_RIGHT]:
    #         self.direction.x = 1
    #         self.facing_right = True
    #     elif keys[pygame.K_LEFT]:
    #         self.direction.x = -1
    #         self.facing_right = False
    #     else:
    #         self.direction.x = 0
    #
    #     if keys[pygame.K_SPACE] and self.jump_count <= 18:
    #         self.jump()
        # moving = False
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE and self.jump_count <= 2:
        #             self.jump()
        # if not self.moving:
        #     if keys[pygame.K_SPACE] and self.jump_count <= 3:
        #         self.moving = True
        #         self.jump()
        #     self.jump_count += 1
        #     print(self.jump_count)
        #     # self.moving = False

        # if self.moving:
        #     self.jump_count += 1
        #     self.moving = False
        #     print(self.jump_count)

    # # get status of player (jump, run, idle etc.)
    # def get_status(self):
    #     if self.direction.y < 0:   # player going upwards (jump)
    #         if self.jump_count == 1:
    #             self.status = 'jump'
    #         elif self.jump_count == 2:
    #             self.status = 'double_jump'
    #     elif self.direction.y > 1:      # player going downwards
    #         self.status = 'fall'
    #     else:
    #         if self.direction.x != 0:     # player moving left/right
    #             self.status = 'run'
    #         else:
    #             self.status = 'idle'

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    # # old jump
    # def get_status(self):
    #     if self.direction.y < 0:   # player going upwards (jump)
    #         if self.jump_count < 9:
    #             self.status = 'jump'
    #         elif self.jump_count >= 9:
    #             self.status = 'double_jump'
    #     elif self.direction.y > 1:      # player going downwards
    #         self.status = 'fall'
    #     else:
    #         if self.direction.x != 0:     # player moving left/right
    #             self.status = 'run'
    #         else:
    #             self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_damage(self):
        if not self.invincible:
            self.change_health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:        # measures timer
                self.invincible = False

    def wave_value(self):   # used for flickering of character when hurt
        value = sin(pygame.time.get_ticks())    # between -1 and 1 (transparency between 0 and 255)
        if value >= 0: return 255
        else: return 0

    def update(self):
        self.animate()
        self.get_status()
        self.get_input()
        self.run_dust_animation()
        self.invincibility_timer()
        self.wave_value()
