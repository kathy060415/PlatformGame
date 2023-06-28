import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'available':
            self.image.fill('red')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center=pos)


# icon on overworld (Tracks progess of player)
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((15, 15))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos

# start_level: player starting level
# max_level: total num of levels
class Overworld:
    def __init__(self, start_level, max_level, surface):
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level    # initialized to start level

        # movement logic
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.moving = False

        # sprites
        self.setup_nodes()
        self.setup_icon()

    # setting up position of nodes
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()      # making node group

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:     # to only see levels that are open
                node_sprite = Node(node_data['node_pos'], 'available')       # making a node class for each level
            else:
                node_sprite = Node(node_data['node_pos'], 'locked')
            self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface, 'red', False, points, 4)     # pygame that draws lines

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)    # gives list of all node sprites
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)

        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()    # to get length (direction) of vector

    def update_icon_pos(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]

    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)

