import os
import random
import sys
import pygame

# variables
width_menu, height_menu = 686, 386  # size window menu
width_game, height_game = 600, 500
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
screensaver_group = pygame.sprite.Group()
sten_group = pygame.sprite.Group()
FPS = 100
clock = pygame.time.Clock()
camera = 0
pygame.init()
size_menu = (width_menu, height_menu)
size_game = (width_game, height_game)
screen = pygame.display.set_mode(size_menu)


##########################
# class
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
        self.dx = -(target.rect.x + target.rect.w // 2 - width_game // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height_game // 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)


class Screensaver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(screensaver_group)
        self.image = load_image(f'screensaver/screensaver_{random.randint(1, 2)}.jpg')
        self.rect = self.image.get_rect()


##########################
# func
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        try:
            image = image.convert_alpha()
        except Exception:
            pass
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def draw_game():
    pass


def draw_menu(mouse_x=-1, mouse_y=-1):
    screen.fill(pygame.Color('white'))
    screensaver_group.draw(screen)

    # draw button
    button = pygame.Surface((150, 75))  # the size rect
    button.set_alpha(150)  # alpha level
    button.fill((62, 50, 168))  # this fills the entire surface
    screen.blit(button, (size_menu[0] // 2 - 75, 10))

    text_game_go1 = pygame.font.Font(None, 34)
    text_game_go = text_game_go1.render('Продолжить', 1, 'black')

    screen.blit(text_game_go, (size_menu[0] // 2 - 75, 30))
    if mouse_x != -1 and mouse_y != -1:
        if size_menu[0] // 2 - 75 <= mouse_x <= size_menu[0] // 2 + 75 and 10 <= mouse_y <= 85:
            return 1
        return 0


def menu():
    runnig = True
    Screensaver()
    draw_menu()
    data = 0
    while runnig:  # boss while
        # события while
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnig = False
                exit(0)
            if pygame.mouse.get_pressed()[0]:
                data = draw_menu(mouse_x=pygame.mouse.get_pos()[0], mouse_y=pygame.mouse.get_pos()[1])
                if data == 1:
                    runnig = False
        clock.tick(FPS)
        pygame.display.flip()


def level_window():
    pass


def play_game():
    runnig = True
    while runnig:  # boss while
        # события while
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnig = False
                exit(0)
        clock.tick(FPS)
        pygame.display.flip()


def run():
    global screen
    menu()
    screen = pygame.display.set_mode(size_game)
    play_game()
    pygame.quit()
