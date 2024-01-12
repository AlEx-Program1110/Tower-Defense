from itertools import product
from os import path
import pygame


class GameOver:
    def __init__(self, screen_width: int, screen_height: int, name: str = "game over.png") -> None:
        self.image = pygame.transform.scale(load_image(name), (screen_width, screen_height))
        self.rect = self.image.get_rect()
        self.x = -self.rect.width
        self.rect.x = -self.rect.width
        self.status = 1

    def update(self, move: int, fps: int, screen_width: int) -> None:
        if self.status:
            self.x += move / fps
        if self.x + self.rect.width >= screen_width:
            self.status = 0
        self.rect.x = self.x

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.rect.y))


class Mob(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image: str | pygame.Surface, speed: int, xp: int, way: list, money: int) -> None:
        super().__init__()
        self.image = image
        self.x, self.y = x, y
        self.speed = speed
        self.xp = xp
        self.path = way[1:]
        self.direction = way[0][-1]
        self.money = money

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.y))

    def get_xp(self) -> int | float:
        return self.xp

    def get_x_y(self) -> list[int | float, int | float]:
        return [self.x, self.y]

    def set_money(self, money):
        self.money = money

    def set_xp(self, xp):
        self.xp = xp

    def get_money(self):
        return self.money

    def update(self, fps: int) -> int | None:
        if self.direction == 0:
            return 0
        if self.direction == 1:
            self.x += self.speed / fps
            if self.x >= self.path[0][0]:
                self.x = self.path[0][0]
                self.direction = self.path[0][-1]
                self.path.pop(0)
        elif self.direction == 2:
            self.y -= self.speed / fps
            if self.y <= self.path[0][1]:
                self.y = self.path[0][1]
                self.direction = self.path[0][-1]
                self.path.pop(0)
        elif self.direction == 3:
            self.x -= self.speed / fps
            if self.x <= self.path[0][0]:
                self.x = self.path[0][0]
                self.direction = self.path[0][-1]
                self.path.pop(0)
        elif self.direction == 4:
            self.y += self.speed / fps
            if self.y >= self.path[0][1]:
                self.y = self.path[0][1]
                self.direction = self.path[0][-1]
                self.path.pop(0)

    def set_speed(self, speed: int | float) -> None:
        self.speed = speed


class Tower(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, image_all: list, name: str) -> None:
        super().__init__()
        self.image_all = image_all.copy()
        self.image = self.image_all[0]
        self.rect = self.image.get_rect()
        self.name = name
        self.x, self.y = x, y
        self.corner = 0
        self.view = 0
        self.radius = 100
        self.damage = 10

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))

    def set_corner(self, corner) -> None:
        print(corner)
        self.corner = corner
        loc = self.image.get_rect().center  # rot_image is not defined
        self.image = pygame.transform.rotate(self.image, corner)
        self.image.get_rect().center = loc

    def set_view(self, view) -> None:
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

    def update(self) -> None:
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
    def __init__(self, width: int, height: int, left_indent: int, top_indent: int, cell_size: int, board,
                 way: list[str], count_wave: int, data_wave: dict[int: str], data_tower) -> None:

        self.width = width
        self.height = height
        self.board = board
        self.left = left_indent
        self.top = top_indent
        self.cell_size = cell_size

        self.grass = load_image('grass.jpg')
        self.grass = pygame.transform.scale(self.grass, (self.cell_size, self.cell_size))
        self.plate = pygame.transform.scale(load_image('plate.jpg'), (self.cell_size, self.cell_size))
        self.box_texture = pygame.transform.scale(load_image('box.jpg'), (self.cell_size, self.cell_size))
        self.tower_finish = pygame.transform.scale(load_image('tower_finish.jpg'), (self.cell_size, self.cell_size))
        self.data_tower = data_tower
        # pygame.transform.scale(load_image('data_tower.bmp'), (self.cell_size * self.width, self.top))
        self.towers_texture = {
            'fire': [
                pygame.transform.scale(load_image('tower_fire_1.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_fire_2.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_fire_3.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5))
            ],
            'bomb': [
                pygame.transform.scale(load_image('tower_bomb_1.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_bomb_2.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_bomb_3.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5))
            ],
            'gun': [
                pygame.transform.scale(load_image('tower_gun_1.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_gun_2.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_gun_3.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5))
            ],
            'laser': [
                pygame.transform.scale(load_image('tower_laser_1.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_laser_2.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5)),
                pygame.transform.scale(load_image('tower_laser_3.jpg'), (self.cell_size // 1.5, self.cell_size // 1.5))
            ]
        }

        self.trails = [
            pygame.transform.scale(load_image(f'trail_{i + 1}.jpg'), (self.cell_size,) * 2) for i in range(6)
        ]

        self.texture_mobs = {
            'regular': pygame.transform.scale(load_image('regular.png'), (self.cell_size, self.cell_size)),
            'fast': pygame.transform.scale(load_image('fast.png'), (self.cell_size, self.cell_size)),
            'fat': pygame.transform.scale(load_image('fat.png'), (self.cell_size, self.cell_size))
        }

        self.path = []
        for index, element in enumerate(way[:]):
            elem = list(map(int, [
                element.split(' : ')[0].split(',')[0],
                element.split(' : ')[0].split(',')[1],
                element.split(' : ')[-1]
            ]))

            elem[0] = elem[0] * self.cell_size + self.left
            elem[1] = elem[1] * self.cell_size + self.top

            self.path.append(elem)

        self.mobs = []
        self.now_wave = 1
        self.count_wave = count_wave
        self.command_all = {
            '1': load_image('tower_fire_1.jpg'),
            '2': load_image('tower_bomb_1.jpg'),
            '3': load_image('tower_gun_1.jpg'),
            '4': load_image('tower_laser_1.jpg'),
            'del': load_image('del.jpg'),
            'level up': load_image('level up.jpg')
        }

        for picture_name in self.command_all:
            if not self.command_all[picture_name]:
                continue

            picture = self.command_all[picture_name]
            self.command_all[picture_name] = pygame.transform.scale(picture, (self.cell_size // 2,) * 2)
            self.command_all[picture_name].set_colorkey((255, 255, 255))

        self.command = '1'
        self.money = 20
        self.choice = 0
        self.pos_choice = []
        self.tick = 0
        self.count_mobs = 0
        self.data_wave = data_wave

        self.total_heart_count = self.heart_count = 5
        self.alive_heart = pygame.transform.scale(load_image('alive_heart.png'), (self.cell_size // 2,) * 2)
        self.death_heart = pygame.transform.scale(load_image('death_heart.png'), (self.cell_size // 2,) * 2)
        self.alive_heart.set_colorkey((255, 255, 255))
        self.death_heart.set_colorkey((255, 255, 255))

    def get_click(self, mouse_pos: tuple[int, int]) -> None:
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse: tuple[int, int]) -> tuple | None:
        mouse = [(mouse[0] - self.left) // self.cell_size, (mouse[1] - self.top) // self.cell_size]
        if mouse[0] < 0 or mouse[0] >= self.width or mouse[1] < 0 or mouse[1] >= self.height:
            return None
        return tuple(mouse)

    def on_click(self, x_y_data: tuple) -> int | None:
        if x_y_data is None:
            return 0
        print(x_y_data)
        command = self.command
        if command == 'del':
            try:
                if isinstance(self.board[x_y_data[1]][x_y_data[0]], Tower):
                    self.board[x_y_data[1]][x_y_data[0]] = 'P'
            except AssertionError:
                pass
        elif command == 'level up':
            try:
                assert self.board[x_y_data[1]][x_y_data[0]].name
                assert self.board[x_y_data[1]][x_y_data[0]].view + 1 <= 2
                if self.board[x_y_data[1]][x_y_data[0]].name == 'fire' and self.money - (
                        (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 20) >= 0:
                    self.money -= (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 20
                    self.board[x_y_data[1]][x_y_data[0]].set_view(self.board[x_y_data[1]][x_y_data[0]].view + 1)
                elif self.board[x_y_data[1]][x_y_data[0]].name == 'bomb' and self.money - (
                        (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 30) >= 0:
                    self.money -= (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 30
                    self.board[x_y_data[1]][x_y_data[0]].set_view(self.board[x_y_data[1]][x_y_data[0]].view + 1)
                elif self.board[x_y_data[1]][x_y_data[0]].name == 'gun' and self.money - (
                        (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 40) >= 0:
                    self.money -= (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 40
                    self.board[x_y_data[1]][x_y_data[0]].set_view(self.board[x_y_data[1]][x_y_data[0]].view + 1)
                elif self.board[x_y_data[1]][x_y_data[0]].name == 'laser' and self.money - (
                        (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 45) >= 0:
                    self.money -= (self.board[x_y_data[1]][x_y_data[0]].view + 1) * 45
                    self.board[x_y_data[1]][x_y_data[0]].set_view(self.board[x_y_data[1]][x_y_data[0]].view + 1)
            except Exception:
                pass
        else:
            if self.board[x_y_data[1]][x_y_data[0]] == 'P':
                if command == '1':
                    if self.money - 20 >= 0:
                        self.board[x_y_data[1]][x_y_data[0]] = Tower(
                            x=x_y_data[0] * self.cell_size + self.left + self.cell_size // 6,
                            y=x_y_data[1] * self.cell_size + self.top + self.cell_size // 6,
                            image_all=self.towers_texture['fire'],
                            name='fire'
                        )
                        self.money -= 20
                elif command == '2':
                    if self.money - 50 >= 0:
                        self.board[x_y_data[1]][x_y_data[0]] = Tower(
                            x=x_y_data[0] * self.cell_size + self.left + self.cell_size // 6,
                            y=x_y_data[1] * self.cell_size + self.top + self.cell_size // 6,
                            image_all=self.towers_texture['bomb'],
                            name='bomb'
                        )
                        self.money -= 50
                elif command == '3':
                    if self.money - 75 >= 0:
                        self.money -= 75
                        self.board[x_y_data[1]][x_y_data[0]] = Tower(
                            x=x_y_data[0] * self.cell_size + self.left + self.cell_size // 6,
                            y=x_y_data[1] * self.cell_size + self.top + self.cell_size // 6,
                            image_all=self.towers_texture['gun'],
                            name='gun'
                        )
                elif command == '4':
                    if self.money - 150 >= 0:
                        self.money -= 150
                        self.board[x_y_data[1]][x_y_data[0]] = Tower(
                            x=x_y_data[0] * self.cell_size + self.left + self.cell_size // 6,
                            y=x_y_data[1] * self.cell_size + self.top + self.cell_size // 6,
                            image_all=self.towers_texture['laser'],
                            name='laser'
                        )

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def set_command(self, command):
        self.command = command

    def render(self, screen):
        for x, y in product(range(self.width), range(self.height)):
            coordinates = (x * self.cell_size + self.left, y * self.cell_size + self.top)
            try:
                assert not isinstance(self.board[y][x], Tower)
                if self.board[y][x] == 'G':
                    screen.blit(self.grass, coordinates)
                elif self.board[y][x].isdigit():
                    screen.blit(self.trails[int(self.board[y][x]) - 1], coordinates)
                elif self.board[y][x] == 'P':
                    screen.blit(self.plate, coordinates)
                elif self.board[y][x] == 'B':
                    screen.blit(self.box_texture, coordinates)
                elif self.board[y][x] == 'F':
                    screen.blit(self.tower_finish, coordinates)

            except AssertionError:
                screen.blit(self.plate, coordinates)
                self.board[y][x].draw(screen)

        rendered_text = COMIC_SANS_MS.render(str(self.money) + '$', False, 'red')
        screen.blit(rendered_text, (self.left + (self.cell_size * (self.width - 2)), self.top))
        screen.blit(self.command_all[self.command], (self.left + (self.cell_size * (self.width - 2.5)), self.top))
        # screen.blit(self.data_tower, (self.cell_size * self.width, self.top))

        for i in range(self.total_heart_count):
            picture = self.alive_heart if i < self.heart_count else self.death_heart
            coordinates = self.cell_size * 0.1 + self.left + (self.cell_size * 0.6 * i), self.cell_size * 0.1 + self.top
            screen.blit(picture, coordinates)

        for elem in self.mobs:
            elem.draw(screen)

    def update(self, fps: int):
        self.tick += 1
        if self.tick == fps * float(self.data_wave[self.now_wave].split(': ')[-1]):
            self.tick = 0
            self.money += 5
            if int(self.data_wave[self.now_wave].split(': ')[1].split(';')[0]) != self.count_mobs:
                self.mobs.append(
                    Mob(
                        x=self.path[0][0],
                        y=self.path[0][1],
                        image=self.texture_mobs[self.data_wave[self.now_wave].split(': ')[0]],
                        speed=self.cell_size,
                        xp=10,
                        way=self.path,
                        money=50
                    )
                )

                self.count_mobs += 1

                if self.data_wave[self.now_wave].split(': ')[0] == 'regular':
                    self.mobs[-1].set_speed(self.cell_size * 1.5)
                    self.mobs[-1].set_money(20)
                    self.mobs[-1].set_xp(30)
                elif self.data_wave[self.now_wave].split(': ')[0] == 'fast':
                    self.mobs[-1].set_speed(self.cell_size * 5)
                    self.mobs[-1].set_money(45)
                    self.mobs[-1].set_xp(20)
                elif self.data_wave[self.now_wave].split(': ')[0] == 'fat':
                    self.mobs[-1].set_speed(self.cell_size)
                    self.mobs[-1].set_money(75)
                    self.mobs[-1].set_xp(100)

            elif int(self.data_wave[self.now_wave].split(': ')[1].split(';')[0]) == self.count_mobs:
                if self.mobs == list():
                    self.now_wave += 1
                    if self.now_wave <= self.count_wave:
                        self.count_mobs = 0

        for i, mob in enumerate(self.mobs):
            try:
                mob.update(fps)
                x_y = mob.get_x_y()
                if self.board[int((x_y[1] - self.top) // self.cell_size)][
                    int((x_y[0] - self.left) // self.cell_size)] != '1' and \
                        self.board[int((x_y[1] - self.top) // self.cell_size)][
                            int((x_y[0] - self.left) // self.cell_size)] != '2':
                    print(int((x_y[1] - self.top) // self.cell_size),
                          int((x_y[0] - self.left) // self.cell_size))
                if mob.get_xp() <= 0:
                    self.money += self.mobs[i].get_money()
                    self.mobs[i] = None
                elif mob.get_x_y() == [self.path[-1][0], self.path[-1][1]]:
                    self.money += self.mobs[i].get_money()
                    self.mobs[i] = None
                    self.heart_count -= 1
            except IndexError:
                pass

        self.mobs = list(filter(lambda enemy: enemy is not None, self.mobs))
        if self.heart_count == 0 or self.now_wave > self.count_wave:
            return 1


def load_image(name: str, color_key: str = None):
    fullname = path.join('data\\texture', name)

    if not path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        raise SystemExit

    image = pygame.image.load(fullname)
    if color_key is None:
        try:
            image = image.convert_alpha()
        except pygame.error:
            pass
    else:
        image = image.convert()
        if color_key == -1:
            image.set_colorkey(image.get_at((0, 0)))
        image.set_colorkey(color_key)

    return image


pygame.init()
pygame.font.init()
COMIC_SANS_MS = pygame.font.SysFont('Comic Sans MS', 30)
