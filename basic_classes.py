import pygame
from os import path


# self.mobs = [Mob(x=self.path[0][0], y=self.path[0][1],
#                  image=pygame.transform.scale(load_image('yes.jpg'), (self.cell_size, self.cell_size)),
#                  speed=self.cell_size * 2, xp=10, path=self.path)]

class Mob(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, image='', speed=0, xp=10, path=pygame.image):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.xp = xp
        self.path = path[1:]
        self.direction = path[0][-1]

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_xp(self):
        return self.xp

    def get_x_y(self):
        return [self.x, self.y]

    def update(self, FPS):
        if self.direction == 0:
            return 0
        if self.direction == 1:
            self.x += self.speed / FPS
            if self.x >= self.path[0][0]:
                self.x = self.path[0][0]
                self.direction = self.path[0][-1]
                self.path.pop(0)
        elif self.direction == 2:
            self.y -= self.speed / FPS
            if self.y <= self.path[0][1]:
                self.y = self.path[0][1]
                self.direction = self.path[0][-1]
                self.path.pop(0)
        elif self.direction == 3:
            self.x -= self.speed / FPS
            if self.x <= self.path[0][0]:
                self.x = self.path[0][0]
                self.direction = self.path[0][-1]
                self.path.pop(0)
        elif self.direction == 4:
            self.y += self.speed / FPS
            if self.y >= self.path[0][1]:
                self.y = self.path[0][1]
                self.direction = self.path[0][-1]
                self.path.pop(0)


class Tower_fire(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, image_all=[]):
        super().__init__()
        self.image_all = image_all.copy()
        self.image = self.image_all[0]
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.name = 'tower_fire'
        self.corner = 0
        self.view = 0
        self.radius = 100
        self.damage = 10

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def set_corner(self, corner):
        self.corner = corner
        loc = self.image.get_rect().center  # rot_image is not defined
        self.image = pygame.transform.rotate(self.image, corner)
        self.image.get_rect().center = loc

    def set_view(self, view):
        self.view = view
        self.image = self.image_all[view]


class Button:
    def __init__(self, screen: pygame.Surface, x: float, y: float, width: float, height: float, text: str = "",
                 color: tuple[int, int, int] = (62, 50, 168), text_color: tuple[int, int, int] = (0, 0, 0),
                 border_radius: int = 10) -> None:

        self.screen = screen
        self.is_pressed = False

        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(x - width * 0.5, y - height * 0.5, width, height)

        hsva_color = pygame.Color(*color, a=255).hsva

        self.inactive_color = pygame.Color(0, 0, 0)
        self.unpressed_color = pygame.Color(0, 0, 0)
        self.pressed_color = pygame.Color(0, 0, 0)

        self.inactive_color.hsva = hsva_color[0], 60, hsva_color[2]
        self.unpressed_color.hsva = hsva_color[0], 75, hsva_color[2]
        self.pressed_color.hsva = hsva_color[0], 100, hsva_color[2]

        self.text = text
        self.text_color = text_color
        self.border_radius = border_radius

    def update(self) -> bool:
        self.is_pressed = False
        mouse_position = pygame.mouse.get_pos()
        rendered_text = COMIC_SANS_MS.render(self.text, False, self.text_color)

        if (self.x - self.width * 0.5 <= mouse_position[0] <= self.x + self.width * 0.5 and
                self.y - self.height * 0.5 <= mouse_position[1] <= self.y + self.height * 0.5):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, self.pressed_color, self.rect, border_radius=self.border_radius)
                self.is_pressed = True
            else:
                pygame.draw.rect(self.screen, self.unpressed_color, self.rect, border_radius=self.border_radius)
        else:
            pygame.draw.rect(self.screen, self.inactive_color, self.rect, border_radius=self.border_radius)

        self.screen.blit(rendered_text, rendered_text.get_rect(center=(self.x, self.y)))


class Board:
    # создание поля
    def __init__(self, width: int, height: int, left_indent: int, top_indent: int, cell_size: int, board, path,
                 count_wave: int, data_wave):
        self.width = width
        self.height = height
        self.board = board
        self.left = left_indent
        self.top = top_indent
        self.cell_size = cell_size

        self.grass = load_image('grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (self.cell_size, self.cell_size))
        self.plate = pygame.transform.scale(load_image('plate.jpg'), (self.cell_size, self.cell_size))
        self.towers_texture = {
            'fire': [
                pygame.transform.scale(load_image('tower_fire_1.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_fire_2.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_fire_3.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5))]}
        self.trails = list()
        for i in range(6):
            self.trails.append(load_image(f'trail_{i + 1}.jpg'))
            self.trails[i] = pygame.transform.scale(self.trails[i], (self.cell_size, self.cell_size))
        self.texture_mobs = {'regular': pygame.transform.scale(load_image('yes.jpg'),
                                                               (self.cell_size, self.cell_size))}
        self.path = path
        self.mobs = []
        self.data_mob = {'regular': Mob(self.path[0][0], self.path[0][1],
                                        self.texture_mobs['regular'],
                                        self.cell_size * 2, 10, self.path)}
        self.now_wave = 1
        self.count_wave = count_wave
        self.command_all = {
            '1': pygame.transform.scale(load_image('tower_fire_1.jpg'), (self.cell_size // 2, self.cell_size // 2)),
            '2': '', '3': '', '4': '', '5': '', '6': '', '7': '', '8': '', '9': '',
            '0': pygame.transform.scale(load_image('plate.jpg'), (self.cell_size // 2, self.cell_size // 2)),
            'del': pygame.transform.scale(load_image('del.jpg'), (self.cell_size // 2, self.cell_size // 2)),
            'uplevel': pygame.transform.scale(load_image('uplevel.jpg'), (self.cell_size // 2, self.cell_size // 2))}
        self.command = '0'
        self.money = 100
        self.choice = 0
        self.pos_choice = []
        for i in range(len(self.path)):
            elem = [int(path[i].split(' : ')[0].split(',')[0]), int(path[i].split(' : ')[0].split(',')[1]),
                    int(path[i].split(' : ')[-1])]
            elem[0] = elem[0] * self.cell_size + self.left
            elem[1] = elem[1] * self.cell_size + self.top
            self.path[i] = elem

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse):
        mouse = list(mouse)
        mouse[0] = (mouse[0] - self.left) // self.cell_size
        mouse[1] = (mouse[1] - self.top) // self.cell_size
        if mouse[0] < 0 or mouse[0] >= self.width or mouse[1] < 0 or mouse[1] >= self.height:
            return None
        return tuple(mouse)

    def on_click(self, x_y_data: tuple):
        if x_y_data is None:
            return 0
        print(x_y_data)
        # self.board[x_y_data[1]][x_y_data[0]] = Tower_fire(
        #     x=x_y_data[0] * self.cell_size + self.left + self.cell_size // 6,
        #     y=x_y_data[1] * self.cell_size + self.top + self.cell_size // 6,
        #     image_all=self.towers_texture['fire'])
        # настройка внешнего вида
        # self.board[x_y_data[1]][x_y_data[0]] = 'P'
        command = self.command
        if command == 'del':
            try:
                if not self.board[x_y_data[1]][x_y_data[0]].isdigit():
                    self.board[x_y_data[1]][x_y_data[0]] = 'G'
            except Exception:
                self.board[x_y_data[1]][x_y_data[0]] = 'G'
        elif command == 'uplevel':
            try:
                if self.board[x_y_data[1]][x_y_data[0]].name:
                    pass
                if self.board[x_y_data[1]][x_y_data[0]].view + 1 > 2:
                    raise Exception
                self.board[x_y_data[1]][x_y_data[0]].set_view(self.board[x_y_data[1]][x_y_data[0]].view + 1)
            except Exception:
                pass
        else:
            if command == '0' and self.board[x_y_data[1]][x_y_data[0]] == 'G':
                self.board[x_y_data[1]][x_y_data[0]] = 'P'
            elif self.board[x_y_data[1]][x_y_data[0]] == 'P':
                if command == '1':
                    self.board[x_y_data[1]][x_y_data[0]] = Tower_fire(
                        x=x_y_data[0] * self.cell_size + self.left + self.cell_size // 6,
                        y=x_y_data[1] * self.cell_size + self.top + self.cell_size // 6,
                        image_all=self.towers_texture['fire'])

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_command(self, command):
        self.command = command

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                try:
                    if self.board[y][x] == 'G':
                        screen.blit(self.grass, (x * self.cell_size + self.left,
                                                 y * self.cell_size + self.top))
                    elif self.board[y][x].isdigit():
                        screen.blit(self.trails[int(self.board[y][x]) - 1], (x * self.cell_size + self.left,
                                                                             y * self.cell_size + self.top))
                    elif self.board[y][x] == 'P':
                        screen.blit(self.plate, (x * self.cell_size + self.left,
                                                 y * self.cell_size + self.top))
                except Exception:
                    screen.blit(self.plate, (x * self.cell_size + self.left,
                                             y * self.cell_size + self.top))
                    self.board[y][x].draw(screen)
        rendered_text = COMIC_SANS_MS.render(str(self.money) + '$', False, 'red')
        screen.blit(rendered_text, (self.left + (self.cell_size * (self.width - 2)), self.top))

        screen.blit(self.command_all[self.command], (self.left + (self.cell_size * (self.width - 2.5)), self.top))

        for elem in self.mobs:
            elem.draw(screen)

    def update(self, FPS):
        for i in range(len(self.mobs)):
            self.mobs[i].update(FPS)
            print(self.mobs[i].get_x_y())
            print((self.path[-1][0], self.path[-1][1]))
            if self.mobs[i].get_xp() <= 0:
                self.mobs.pop(i)
            elif self.mobs[i].get_x_y() == [self.path[-1][0], self.path[-1][1]]:
                self.mobs.pop(i)


def load_image(name, colorkey=None):
    fullname = path.join('data\\texture', name)

    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        raise SystemExit

    image = pygame.image.load(fullname)

    if colorkey is None:
        try:
            image = image.convert_alpha()
        except Exception:
            pass
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


pygame.init()
pygame.font.init()
COMIC_SANS_MS = pygame.font.SysFont('Comic Sans MS', 30)
