import random
import os

import pygame

from blocks import *
from camera import Camera
from board import Board
from Button import ColorButton
from ui_in_game import InGameUI
from ui_menu import MenuUI
from settings_ui import SettingsUI
from UI_statistik import ui_show_statistic
from database import *

SIZE = WIDTH, HEIGHT = 800, 900
FPS = 60

BLOCKS = [ZBlock, SBlock, IBlock, LBlock, TBlock, JBlock, OBlock]

story_line = []
index_story = -1

score = 0
level = 1

is_paused = False
result_show = False

music_volume, block_volume, difficulty, language, theme = get_player_settings()
music_volume = music_volume / 100


def gameplay(flag_shake_y):
    dx = dy = 0
    # логика тряски экрана при приземлении
    if flag_shake_y:
        flag_shake_y -= 1
        dy = power_shake_y
    elif board.rect.y != top:
        dy = -power_shake_y

    key = pygame.key.get_pressed()
    if key[pygame.K_DOWN]:
        block.speed = 20
    if key[pygame.K_RIGHT]:
        dx = block.move_right(colliders, vertical_borders)
        if board.rect.x > left:
            dx = 0
    elif key[pygame.K_LEFT]:
        dx = block.move_left(colliders, vertical_borders)
        if board.rect.x < left:
            dx = 0
    else:
        if board.rect.x > left:
            dx = -5
        elif board.rect.x < left:
            dx += 5
        block.move_tick = 1

    board.render(screen)
    block.update(colliders)
    block.shadow(screen, colliders)
    block.draw(screen)
    particles_group.update()
    particles_group.draw(screen)
    in_game_ui.render(screen)

    show_next_block()

    # изменение позиции камеры
    camera.update((dx, dy))
    for i, sprite in enumerate(all_group):
        camera.apply(sprite)
    pause_button.draw(screen)
    return flag_shake_y


def main_menu():
    start_button.check_hover(pos)
    start_button.draw(screen)
    menu_ui.render(screen)


def spawn_new_block(flag_shake_y, block=None, spawn_block_list=None):
    defeat = False
    # если у нас есть блок, то оставим его снизу
    if block:
        # переберём все ректы и поставим их в сетке
        color_index = spawn_block_list[0][1] + 1
        spawn_block_list = spawn_block_list[1::]
        spawn_block_list.append((random.randint(0, 6), random.randint(0, 6)))
        block.kill()  # убираем активный блок из группы
        flag_shake_y += 3
        for rect in block.rects:
            x, y = rect.center
            cell = board.get_cell((x, y))
            board.create_block(cell, color_index)
            if cell[1] < 2:  # проверяем есть ли блок выше игрового поля
                defeat = True
                # если да, мы проиграли
        if defeat:
            return False, spawn_block_list, flag_shake_y
    block_index = spawn_block_list[0][0]  # определяем какой блок заспавниться
    color_index = spawn_block_list[0][1]  # определяем цвет блока
    block = BLOCKS[block_index](all_group, board.rect.x, board.rect.y, cell_size, speed, color_index)
    return block, spawn_block_list, flag_shake_y


def show_next_block():  # показывает следующий блок который заспавнится
    x, y = 670, 250
    font = pygame.font.SysFont(None, 30)
    if settings_ui.bg_color == (255, 255, 255):
        img_text = font.render('Next: ', 1, (0, 0, 0))
        screen.blit(img_text, (x, y))
    else:
        img_text = font.render('Next: ', 1, (255, 255, 255))
        screen.blit(img_text, (x, y))
    block_index = spawn_block_list[1][0]
    color_index = spawn_block_list[1][1]

    show_block = BLOCKS[block_index](all_group, x - 70, y + 50, 20, 0, color_index)
    show_block.draw(screen)


def get_button_action(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                return button.text
    return None


if __name__ == '__main__':
    pygame.init()

    # проверяем на наличие базы данных, если нету создаём пустую
    if not os.path.isfile("data/tetris.db"):
        if not os.path.isdir('data'):
            os.mkdir('data')
        create_table()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('tetris')
    settings_ui = SettingsUI()

    all_group = pygame.sprite.Group()
    particles_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True

    defeat = False
    tetris_game_running = False
    start_menu = True
    show_statistic = False
    flag_shake_y = 0

    camera = Camera()

    board = Board(all_group, 10, 21)
    cell_size = 40
    cell_height = 21
    cell_width = 10
    colliders = []
    vertical_borders = []
    left = (WIDTH - (cell_width * cell_size)) // 2
    top = (HEIGHT - (cell_height * cell_size)) // 2 - 30
    board.set_view(left, top, cell_size, colliders, vertical_borders)

    power_shake_y = 1
    speed = 1
    spawn_block_list = [(random.randint(0, 6), random.randint(0, 6)), (random.randint(0, 6), random.randint(0, 6))]
    block, spawn_block_list, flag_shake_y = spawn_new_block(flag_shake_y, spawn_block_list=spawn_block_list)

    width = 260
    height = 80

    pos = 0, 0

    if settings_ui.bg_color == (0, 0, 0):
        start_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) - 200, width, height,
                                   'TETRIS GAME', 'black', hover_color='gray', text_size=40)

        pause_button = ColorButton(WIDTH - 770, 20, 80, 40, 'Pause', 'black', hover_color='gray', text_size=30)

        back_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 - 95, 200, 50, 'Back to Menu', 'black',
                                  hover_color='gray',
                                  text_size=30)
        continue_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, 'Continue', 'black',
                                      hover_color='gray',
                                      text_size=30)
        settings_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, 'Settings', 'black', hover_color='gray',
                                      text_size=30)
        results_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 + 45, 200, 50, 'Results', 'black',
                                     hover_color='gray',
                                     text_size=30)
        quit_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, 'Quit', 'black', hover_color='gray',
                                  text_size=30)
    else:
        start_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) - 200, width, height,
                                   'TETRIS GAME', 'white', hover_color='gray', text_size=40)

        pause_button = ColorButton(WIDTH - 770, 20, 80, 40, 'Pause', 'white', hover_color='gray', text_size=30)

        back_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 - 95, 200, 50, 'Back to Menu', 'white',
                                  hover_color='gray',
                                  text_size=30)
        continue_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, 'Continue', 'white',
                                      hover_color='gray',
                                      text_size=30)
        settings_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, 'Setting', 'white', hover_color='gray',
                                      text_size=30)
        results_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 + 45, 200, 50, 'Results', 'white',
                                     hover_color='gray',
                                     text_size=30)
        quit_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, 'Quit', 'white', hover_color='gray',
                                  text_size=30)

    menu_ui = MenuUI(WIDTH, HEIGHT)
    in_game_ui = InGameUI(WIDTH, HEIGHT)

    play_music = pygame.mixer.Sound('data/sounds/base_music_fon.mp3')
    play_music.set_volume(music_volume)

    play_music.play(-1)

    while running:
        pygame.display.set_caption(f'fps - {int(clock.get_fps())}')
        board.update(colliders, vertical_borders)
        screen.fill(settings_ui.bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if tetris_game_running:
                    if event.key == pygame.K_UP:
                        block.rotation(colliders)
                    if event.key == pygame.K_SPACE:
                        block.instant_fall(colliders)

                if not start_menu and event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused
                    tetris_game_running = not tetris_game_running

            elif tetris_game_running and event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    block.speed = speed

            if event.type == pygame.MOUSEMOTION:
                pause_button.handle_event(event)
                continue_button.handle_event(event)
                settings_button.handle_event(event)
                quit_button.handle_event(event)
                pos = event.pos
                results_button.check_hover(pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.rect.collidepoint(event.pos):
                    is_paused = not is_paused
                    tetris_game_running = False

                # Логика для главного меню
                if start_menu:
                    action = menu_ui.get_button_action(event)
                    if action == 'Continue' and start_menu:
                        start_menu = False
                        tetris_game_running = True
                    elif action == 'Settings':
                        settings_open = True
                        while settings_open:
                            settings_ui.render(screen)
                            play_music.set_volume(music_volume)
                            pygame.display.flip()
                            for settings_event in pygame.event.get():
                                if settings_event.type == pygame.QUIT:
                                    running = False
                                    exit()
                                if settings_event.type == pygame.KEYDOWN and settings_event.key == pygame.K_ESCAPE:
                                    settings_open = False
                                settings_action, music_volume = settings_ui.handle_event(settings_event)
                                if settings_action == "back":
                                    settings_open = False
                    elif action == 'Results':
                        print('ok')
                        show_statistic = True
                    elif action == 'Quit' and start_menu:
                        running = False

                    elif action == "Save and Exit":
                        running = False

                # Логика паузы
                if is_paused:
                    if continue_button.rect.collidepoint(event.pos):
                        is_paused = False
                        tetris_game_running = True
                    elif back_button.rect.collidepoint(event.pos):
                        tetris_game_running = False
                        is_paused = False
                        start_menu = True
                    elif settings_button.rect.collidepoint(event.pos):
                        settings_open = True
                        while settings_open:
                            play_music.set_volume(music_volume)
                            settings_ui.render(screen)
                            pygame.display.flip()
                            for settings_event in pygame.event.get():
                                if settings_event.type == pygame.QUIT:
                                    running = False
                                    exit()
                                if settings_event.type == pygame.KEYDOWN and settings_event.key == pygame.K_ESCAPE:
                                    settings_open = False
                                settings_action, music_volume = settings_ui.handle_event(settings_event)
                                if settings_action == "back":
                                    settings_open = False

                    elif quit_button.rect.collidepoint(event.pos):
                        running = False

                # Проверка кнопки старта в главном меню
                elif event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(event.pos):
                    start_menu = False
                    tetris_game_running = True

                elif event.type == pygame.USEREVENT:
                    print('event_type')
                    if event.button == results_button:
                        show_statistic = True
                        print('ok')

            results_button.handle_event(event)

        # ЛОГИКА ОТОБРАЖЕНИЕ ЭКРАНОВ
        if start_menu:
            if show_statistic:
                ui_show_statistic(screen)
            else:
                screen.fill(settings_ui.bg_color)
                main_menu()
                menu_ui.handle_event(event)

        if tetris_game_running:
            # ход игры
            # логика тряски экрана при приземлении
            flag_shake_y = gameplay(flag_shake_y)

            font = pygame.font.SysFont(None, 30)
            if settings_ui.bg_color == (255, 255, 255):
                score_text = font.render(f"Score: {score}", True, (0, 0, 0))
                level_text = font.render(f"Level: {level}", True, (0, 0, 0))
                screen.blit(level_text, (620, 20))
                screen.blit(score_text, (620, 70))
            else:
                score_text = font.render(f"Score: {score}", True, (255, 255, 255))
                level_text = font.render(f"Level: {level}", True, (255, 255, 255))
                screen.blit(level_text, (620, 20))
                screen.blit(score_text, (620, 70))

        elif is_paused:
            board.render(screen)
            block.draw(screen)
            back_button.draw(screen)
            continue_button.draw(screen)
            quit_button.draw(screen)

        elif defeat:
            board.render(screen)
            font = pygame.font.SysFont(None, 100)
            img = font.render("YOU LOSE!", 1, (255, 255, 255), (0, 0, 0))
            screen.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height()))

        # Проверка игры и логика спавна нового блока
        if tetris_game_running and block.is_ground:
            block, spawn_block_list, flag_shake_y = spawn_new_block(flag_shake_y, block,
                                                                    spawn_block_list=spawn_block_list)
            if block:  # проверка на блок иначе на поражение
                lines_filled = board.check_fill_line(particles_group)
                # если при падении блока заполнилась линия, увеличить силу тряски
                if lines_filled > 0:
                    score += lines_filled * 100
                    power_shake_y = 4
                else:  # иначе поставить её обычную
                    power_shake_y = 1
                if score >= level * 1000:
                    level += 1
            else:
                defeat = True
                tetris_game_running = False

        play_music.set_volume(music_volume)
        vertical_borders.clear()
        colliders.clear()
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
