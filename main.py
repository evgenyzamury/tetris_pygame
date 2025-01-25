import random
import os

import pygame

from blocks import *
from camera import Camera
from board import Board
from button import Button
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
        # падения игрового поля
        flag_shake_y -= 1
        dy = power_shake_y
    elif board.rect.y != top:
        # возвращение в исходное состояние поля
        dy = -power_shake_y

    # возьмем клавиши которые сейчас нажаты для управления блоком
    key = pygame.key.get_pressed()

    # ускорение падения блока
    if key[pygame.K_DOWN]:
        block.speed = 20
    # двигаем блок вправо
    if key[pygame.K_RIGHT]:
        # если мы касаемся игрового поля, сдвигаем его (для приятного эффекта столкновения с границей поля)
        dx = block.move_right(colliders, vertical_borders)
        if board.rect.x > left:  # ограничиваем отклонения поля вправо
            dx = 0
    elif key[pygame.K_LEFT]:
        # если мы касаемся игрового поля, сдвигаем его (для приятного эффекта столкновения с границей поля)
        dx = block.move_left(colliders, vertical_borders)
        if board.rect.x < left:  # ограничиваем отклонения поля влево
            dx = 0
    else:
        # возвращаем игровое поле в исходное состояние при боковых отклонениях
        if board.rect.x > left:
            dx = -5
        elif board.rect.x < left:
            dx += 5
        # если ничего не произошло ставим блок в готовность хода для моментального реагирования при нажатии клавиши < >
        block.move_tick = 1

    board.render(screen)  # рисуем игровое поле

    block.update(colliders)  # обновляем блок
    block.shadow(screen, colliders)  # рисуем тень блока (куда он падает)
    block.draw(screen)  # рисуем блок

    particles_group.update()  # обновляем все частицы
    particles_group.draw(screen)  # рисуем все частицы

    show_next_block()  # рисуем следующий блок

    pause_button.check_hover(pos)
    pause_button.draw(screen)  # рисуем паузу

    # изменение позиции камеры
    camera.update((dx, dy))
    for i, sprite in enumerate(all_group):
        camera.apply(sprite)
    return flag_shake_y


def main_menu():
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
    # левый верхний угол где показывается блок
    x, y = 670, 250
    font = pygame.font.SysFont(None, 30)
    # рисуем надпись по теме
    if theme:
        img_text = font.render('Next: ', 1, (255, 255, 255))
        screen.blit(img_text, (x, y))
    else:
        img_text = font.render('Next: ', 1, (0, 0, 0))
        screen.blit(img_text, (x, y))

    # выбираем 2 блок из списка тк это индексы будущего блока
    block_index = spawn_block_list[1][0]
    color_index = spawn_block_list[1][1]

    # вызываем класс блока и рисуем его на экране
    show_block = BLOCKS[block_index](all_group, x - 70, y + 50, 20, 0, color_index)
    show_block.draw(screen)


def button_set(theme):
    pause_button = Button(WIDTH - 770, 20, 80, 40, 'Pause', ((0, 0, 0) if theme else (255, 255, 255)),
                          hover_color='gray', text_size=30, theme=theme)

    continue_button = Button((WIDTH - 200) // 2, HEIGHT // 2 - 50 - 10, 200, 60, 'continue',
                             ((0, 0, 0) if theme else (255, 255, 255)), hover_color='gray', text_size=30, theme=theme)

    back_to_menu_button = Button((WIDTH - 200) // 2, HEIGHT // 2 + 50 + 10, 200, 60, 'back to menu',
                                 ((0, 0, 0) if theme else (255, 255, 255)), hover_color='gray', text_size=30,
                                 theme=theme)
    return pause_button, continue_button, back_to_menu_button


if __name__ == '__main__':
    pygame.init()

    # проверяем на наличие базы данных, если нету создаём пустую
    if not os.path.isfile(database_path):
        if not os.path.isdir('data'):
            os.mkdir('data')
        create_table()

    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('tetris')
    settings_ui = SettingsUI()

    all_group = pygame.sprite.Group()
    particles_group = pygame.sprite.Group()  # группа для частиц после поломки блоков

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

    power_shake_y = 1  # сила тряски блока при приземлении
    speed = 1  # столько блоков в секунду падает блок

    # список индексов блоков которые будут появляться
    spawn_block_list = [(random.randint(0, 6), random.randint(0, 6)), (random.randint(0, 6), random.randint(0, 6))]
    # спавним блок
    block, spawn_block_list, flag_shake_y = spawn_new_block(flag_shake_y, spawn_block_list=spawn_block_list)

    pos = 0, 0

    # создадим кнопку паузу по теме
    pause_button, continue_button, back_to_menu_button = button_set(theme)

    menu_ui = MenuUI(WIDTH, HEIGHT, theme)

    # музыка на фон
    play_music = pygame.mixer.Sound('data/sounds/base_music_fon.mp3')
    # звук музыку на фон
    play_music.set_volume(music_volume)
    # музыка в бесконечном цикле
    play_music.play(-1)

    while running:
        # показ фпс
        pygame.display.set_caption(f'fps - {int(clock.get_fps())}')
        board.update(colliders, vertical_borders)
        # заливаем фон цветом темы
        screen.fill(settings_ui.bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из приложения нажатие на крестик
                running = False

            if event.type == pygame.MOUSEMOTION:
                pos = event.pos

            if tetris_game_running and event.type == pygame.KEYDOWN:  # отслеживаем нажатие клавиш в игровом процессе
                if event.key == pygame.K_UP:  # нажали на стрелочку вверх - переворачиваем блок на 90 градусов
                    block.rotation(colliders)
                if event.key == pygame.K_SPACE:  # нажали на пробел - моментальный моментальное падение блока
                    block.instant_fall(colliders)
                if event.key == pygame.K_ESCAPE:
                    print('ok')
                    is_paused = True

            elif tetris_game_running and event.type == pygame.KEYUP:  # отслеживаем отпускание клавиш в игровом процессе
                if event.key == pygame.K_DOWN:  # перестаём ускорять блок если отпустили клавишу
                    block.speed = speed

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.rect.collidepoint(event.pos):
                    is_paused = True

                # Логика для главного меню
                if start_menu:
                    action = menu_ui.get_button_action(event)  # ловим действие происходящее в меню

                    if action == 'Continue' and start_menu:  # нажата клавиша continue
                        start_menu = False
                        tetris_game_running = True

                    elif action == 'Settings':  # нажата клавиша settings
                        settings_open = True

                        # Открытые настройки в главном меню
                        while settings_open:
                            settings_ui.render(screen)
                            play_music.set_volume(music_volume)
                            pygame.display.flip()
                            for settings_event in pygame.event.get():

                                # передаём event в обработку в настройки
                                settings_action = settings_ui.handle_event(settings_event)

                                if settings_event.type == pygame.QUIT:
                                    running = False
                                    settings_open = False

                                # выход из настроек с помощью escape
                                if settings_event.type == pygame.KEYDOWN and settings_event.key == pygame.K_ESCAPE:
                                    settings_open = False

                                # выход если была нажата кнопка back
                                if settings_action == "back":
                                    settings_open = False

                                # если был изменен ползунок звука
                                elif settings_action == "music volume":
                                    music_volume = settings_ui.options['music_volume'] / 100

                                # смена цветовой темы приложения
                                elif settings_action == "theme":
                                    menu_ui.change_theme()
                                    theme = int(not theme)
                                    pause_button, continue_button, back_to_menu_button = button_set(theme)

                                # последняя сточка настроек

                    # нажали на кнопку Results
                    elif action == 'Results':
                        show_statistic = True

                    # нажали на кнопку Quit
                    elif action == 'Quit' and start_menu:
                        running = False

                    # нажали на кнопку Exit
                    elif action == "Save and Exit":
                        running = False

        # Логика паузы
        if is_paused:
            while is_paused:
                font = pygame.font.Font(None, 64)
                font_score = pygame.font.SysFont(None, 30)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_paused = False
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        is_paused = False
                    if event.type == pygame.MOUSEMOTION:
                        pos = event.pos
                    if event.type == pygame.USEREVENT:
                        if event.button == back_to_menu_button:  # нажали на клавишу back to menu возвращаемся в лобби
                            is_paused = False
                            tetris_game_running = False
                            start_menu = True
                        if event.button == continue_button:  # нажали на продолжить, продолжаем игру
                            is_paused = False

                    #  ловим нажатие кнопки
                    back_to_menu_button.handle_event(event)
                    continue_button.handle_event(event)

                board.render(screen)  # рисуем игровое поле
                block.draw(screen)  # рисуем активный блок

                # надпись PAUSED
                img_font = font.render('PAUSED', 1, ((255, 255, 255) if theme else (0, 0, 0)))
                # надпись кол-во очков
                score_text = font_score.render(f"Score: {score}", True, ((255, 255, 255) if theme else (0, 0, 0)))

                # выводим надписи на экран
                screen.blit(score_text, (620, 70))
                screen.blit(img_font, ((WIDTH - img_font.get_width()) // 2, img_font.get_height() - 10))

                # рисуем следующий блок
                show_next_block()

                continue_button.check_hover(pos)
                continue_button.draw(screen)
                back_to_menu_button.check_hover(pos)
                back_to_menu_button.draw(screen)
                pause_button.check_hover(pos)
                pause_button.draw(screen)  # рисуем паузу

                pygame.display.flip()

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

            # рисуем очки
            font = pygame.font.SysFont(None, 30)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255) if theme else (0, 0, 0))
            screen.blit(score_text, (620, 70))

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
            else:
                defeat = True
                tetris_game_running = False

        play_music.set_volume(music_volume)
        vertical_borders.clear()
        colliders.clear()
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
