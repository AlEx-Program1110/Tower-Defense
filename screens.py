import pygame
from random import randint
from mechanics import load_image, read_map
from basic_classes import Button, Board, GameOver, GameOverWin


def main_screen_function():
    while True:
        if name_of_function.startswith("level_number_"):
            level_number = int(name_of_function.split("_")[-1])
            play_level(level_number)
        else:
            current_screen[name_of_function]()


def menu_screen() -> None:
    global name_of_function

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                exit_function()

        screen.blit(main_menu_back_ground, (0, 0))

        for button in main_menu_buttons:
            button.update()
            if button.is_pressed:
                name_of_function = main_menu_buttons[button]
                return

        pygame.display.flip()


def survival_screen() -> None:
    while True:
        classic_event_loop()
        if name_of_function == "main_menu":
            return

        screen.fill((0, 0, 0))
        pygame.display.flip()


def levels_menu_screen() -> None:
    global name_of_function
    pygame.time.delay(250)

    while True:
        classic_event_loop()
        if name_of_function == "main_menu":
            return

        screen.fill((0, 0, 0))

        for button in levels_menu_buttons:
            button.update()
            if button.is_pressed:
                name_of_function = levels_menu_buttons[button]
                return

        pygame.display.flip()


def play_level(level_number: int) -> None:
    global name_of_function

    pole = read_map(f'level_{level_number}.txt', (width, height))
    game_over = GameOver(width, height)
    game_over_win = GameOverWin(width, height)
    status = 0
    wait = 1

    while True:
        if name_of_function == "main_menu":
            return
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                name_of_function = "levels_menu_screen"
                return
            if event.type == pygame.QUIT:
                exit_function()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pole.get_click(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pole.set_command('1')
                if event.key == pygame.K_2:
                    pole.set_command('2')
                if event.key == pygame.K_3:
                    pole.set_command('3')
                if event.key == pygame.K_4:
                    pole.set_command('4')
                if event.key == pygame.K_DELETE:
                    pole.set_command('del')
                if event.key == pygame.K_UP:
                    pole.set_command('level up')
        screen.fill((0, 0, 0))
        if status != 1 and status != 2:
            if wait:
                status = pole.update(FPS)
            pole.render(screen, width, height)
            clock.tick(FPS)
            pygame.display.flip()
        elif status == 1:
            screen.fill((0, 0, 0))
            pole.render(screen, width, height)
            game_over.update(300, FPS, width)
            game_over.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()
        else:
            screen.fill((0, 0, 0))
            pole.render(screen, width, height)
            game_over_win.update(300, FPS, width)
            game_over_win.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()


def rules_screen() -> None:
    global name_of_function

    while True:
        classic_event_loop()
        if name_of_function == "main_menu":
            return

        with open('data\\files_for_game\\rules.txt', mode='r', encoding='utf-8') as file:
            intro_text = file.read().split('\n')

        fon = pygame.transform.scale(load_image('files_for_game\\fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.SysFont('Comic Sans MS', 22)
        text_coord = 0

        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()


def classic_event_loop():
    global name_of_function

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_function()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            name_of_function = "main_menu"
            return


def exit_function() -> None:
    pygame.quit()
    raise SystemExit


pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 100

main_menu_back_ground = load_image(f"screensaver\\screensaver_{randint(1, 2)}.jpg")
main_menu_back_ground = pygame.transform.scale(main_menu_back_ground, (width, height))
main_menu_buttons = {
    Button(screen, width * 0.5, height * 0.3, width * 0.3, height * 0.15, "Уровни"): "levels_menu_screen",
    Button(screen, width * 0.5, height * 0.5, width * 0.3, height * 0.15, "Правила"): "rule_screen",
    Button(screen, width * 0.5, height * 0.7, width * 0.3, height * 0.15, "Выход"): "exit"
}
# Button(screen, width * 0.5, height * 0.2, width * 0.3, height * 0.15, "Выживание"): "survivle_menu_screen",

levels_menu_buttons = {
    Button(screen, width * (0.1 + n % 5 * 0.2), height * (0.3 + n // 5 * 0.4), width * 0.15, height * 0.2,
           f"{n + 1}"): f"level_number_{n + 1}" for n in range(10)
}

name_of_function = "main_menu"
current_screen = {
    "main_menu": menu_screen,
    "survivle_menu_screen": survival_screen,
    "levels_menu_screen": levels_menu_screen,
    "rule_screen": rules_screen,
    "exit": exit_function
}
