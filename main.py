import os
import sys
import pygame

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("Не найдено:/")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = os.path.join("data", filename)
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))  # самая длинная строка

    return list(map(lambda x: x.ljust(max_width, "."), level_map))  # ljust дополняем каждую строку до нужной длины


tile_images = {

    'empty': load_image("grass.png"),  # элементы игрового поля
    'wall': load_image("box.png")

}

player_image = load_image("mar.png")

tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()

player, level_x, level_y = None, None, None
tile_width = tile_height = 50

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * tile_width, pos_y * tile_height)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = 0
        self.y = 0

    def update(self, action):
        x, y = 0, 0
        if action[pygame.K_UP]:
            y = -25
        elif action[pygame.K_DOWN]:
            y = 25
        elif action[pygame.K_RIGHT]:
            x = 25
        elif action[pygame.K_LEFT]:
            x = -25
        self.rect = self.rect.move(x, y)
        self.rect.x += x
        self.rect.y += y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def generate_level(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == ".":
                Tile('empty', x, y)
            elif level[y][x] == "#":
                Tile('wall', x, y)
            elif level[y][x] == "@":
                Tile('empty', x, y)
                player = Player(x, y)
    return player, x, y


player, level_x, level_y = generate_level(load_level("level.txt"))
camera = Camera()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.key.get_pressed():
            all_sprites.update(pygame.key.get_pressed())
    tile_group.draw(screen)
    player_group.draw(screen)
    # изменяем ракурс камеры
    #camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    pygame.display.flip()
pygame.quit()