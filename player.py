import pygame
from os.path import join
from support import import_folder
from settings import FPS

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0        # animation frame
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'   # default
        # self.jump_count = 0
        # self.fall_count = 0
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

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
        else:
            flipped_image = pygame.transform.flip(image, True, False)       # image, x-axis, y-axis
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

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
            # self.create_jump_particles(self.rect.midbottom)

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
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.animate()
        self.get_status()
        self.get_input()
