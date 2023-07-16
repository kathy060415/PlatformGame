'''
relies on Tiles to place objects on screen
stores game logic
'''

import pygame
from tiles import Tile, StaticTile, Crate, Coin, Palm
from settings import tile_size, screen_width, screen_height
from player import Player
from support import import_csv_layout, import_cut_graphics
from enemy import Enemy
from decoration import Sky, Water, Clouds
from game_data import levels
from particles import ParticleEffect

class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        # level setup
        self.display_surface = surface
        self.world_shift = 0
        # self.current_x = None      # x position of where collision has occurred

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        # level_content = level_data['content']
        self.new_max_level = level_data['unlock']  # level to be unlocked

        # level display (new)
        # self.font = pygame.font.Font(None, 40)
        # self.text_surf = self.font.render(level_content, True, 'White')
        # self.text_rect = self.text_surf.get_rect(center=(screen_width / 2, screen_height / 2))

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)     # when player is created health is changed

        # user interface
        self.change_coins = change_coins    # method from main used inside level

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates setup
        crates_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crates_layout, 'crates')

        # coins
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraints
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # decoration
        self.sky = Sky(6)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 25, level_width)
        self.clouds = Clouds(400, level_width, 20)

    # new
    # def input(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_RETURN]:   # wins level
    #         self.create_overworld(self.current_level, self.new_max_level)
    #     if keys[pygame.K_ESCAPE]:   # loses level
    #         self.create_overworld(self.current_level, 0)    # level not updated

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False      # player in the air

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    sprite = None

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('Treasure Hunters/Treasure Hunters/Palm Tree Island/Sprites/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        # sprite_group.add(sprite)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('Treasure Hunters/Treasure Hunters/Palm Tree Island/Sprites/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    if type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, 'Treasure Hunters/Treasure Hunters/Pirate Treasure/Sprites/Gold Coin', 5)
                        if val == '1':
                            sprite = Coin(tile_size, x, y, 'Treasure Hunters/Treasure Hunters/Pirate Treasure/Sprites/Silver Coin', 1)

                    if type == 'fg palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y, 'Treasure Hunters/Treasure Hunters/Palm Tree Island/Sprites/palm_small', 40)
                        if val == '1':
                            sprite = Palm(tile_size, x, y, 'Treasure Hunters/Treasure Hunters/Palm Tree Island/Sprites/palm_large', 64)

                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, 'Treasure Hunters/Treasure Hunters/Palm Tree Island/Sprites/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    if sprite is not None:
                        sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':  # player
                    # self.player = pygame.sprite.GroupSingle()
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if val == '1':  # goal
                    hat_surface = pygame.image.load('assets/Items/Checkpoints/End/End (Idle).png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():  # checking all enemy sprites (cycle through all enemies)
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):  # if sprites collide with constraints, False = don't kill
                enemy.reverse()

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # if player gets near to end of screen, screen speed is set to
        # player speed and player speed is set to 0 to look like as if the player
        # is moving
        if player_x < screen_width / 4 and direction_x < 0:      # direction_x < 0 means moving to the left
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_movement_collision(self):
        player = self.player.sprite
        # displaying horizontal movement
        player.collision_rect.x += player.direction.x * player.speed  # num used to increase speed of player
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        # checking for rect collision in all sprites
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:  # player moving left
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    # self.current_x = player.rect.left
                elif player.direction.x > 0:    # player moving right
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    # self.current_x = player.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()  # gravity continually increases; needs to be cancelled out
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        # checking for rect collision in all sprites
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:  # player moving downwards/on floor
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0  # cancels out gravity
                    player.on_ground = True
                    # player.fall_count = 0
                    # player.jump_count = 0
                elif player.direction.y < 0:  # player moving upwards/on ceiling
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height: # player leaves screen
            self.create_overworld(self.current_level, 0)


    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)   # True = do kill
        if collided_coins:      # if anything in list
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)   # False = don't kill

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:    # player going downwards (on top of enemy)
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()    # destroys enemy when jump on top
                else:
                    self.player.sprite.get_damage()

    def run(self):
        # new
        # self.display_surface.blit(self.text_surf, self.text_rect)
        # self.input()

        # sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)    # not displayed (constraints only)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # water
        self.water.draw(self.display_surface, self.world_shift)


