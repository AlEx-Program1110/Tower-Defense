import pygame
from os import path
from basic_classes import Board

PASSWORD = 'program.08'


def load_image(name, colorkey=None):
    fullname = path.join('data', name)

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


def read_map(name, size):
    with open(f'data/levels/{name}', 'r', encoding='utf8') as level_map:
        data = level_map.read().split('\n')
    try:
        if data[0].split(':')[0] != 'PASSWORD' and data[0].split(':')[1] == PASSWORD:
            raise Exception('Файл поврежден!!!')
        data.pop(0)
        if data[0].split(':')[0] != 'WIDTH' and data[1].split(':')[0] != 'HEIGHT':
            raise Exception('Файл поврежден1!!!')
        width = int(data[0].split(':')[1])
        data.pop(0)
        height = int(data[0].split(':')[1])
        data.pop(0)
        if data[0].split(':')[0] != 'POLE':
            raise Exception('Файл поврежден!!!')
        data.pop(0)
        pole = list()
        for y in range(height):
            pole.append(list(data[0]))
            data.pop(0)
        if data[0].split(':')[0] != 'PATH':
            raise Exception('Файл поврежден!!!')
        data.pop(0)
        path = data[0].split(';')
        data.pop(0)
        if data[0].split()[0] != 'COUNT' or data[0].split()[1] != 'WAVE':
            raise Exception('Файл поврежден!!!')
        count_wave = int(data[0].split()[-1])
        data.pop(0)
        data_wave = {}
        for i in range(len(data)):
            if data[0] != f'{i + 1} WAVE:':
                raise Exception('Файл поврежден!!!')
            data.pop(0)
            data_wave[i + 1] = data[0]
            data.pop(0)
    except Exception as text:
        print(text)
        return 0
    size_cell = min(size) // min(width, height)
    left = (size[0] - (width * size_cell)) // 2
    top = (size[1] - (height * size_cell)) // 2
    return Board(width, height, left, top, size_cell, pole, path, count_wave, data_wave)
