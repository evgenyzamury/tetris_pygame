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
from log_in import show_log_in
from database import *
from variables import translations

SIZE = WIDTH, HEIGHT = 800, 900
FPS = 1650

BLOCKS = [ZBlock, SBlock, IBlock, LBlock, TBlock, JBlock, OBlock]


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
    if key[pygame.K_DOWN] or key[pygame.K_s]:
        block.speed = 20
    # двигаем блок вправо
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        # если мы касаемся игрового поля, сдвигаем его (для приятного эффекта столкновения с границей поля)
        dx = block.move_right(board, fps)
        if board.rect.x > left:  # ограничиваем отклонения поля вправо
            dx = 0
    elif key[pygame.K_LEFT] or key[pygame.K_a]:
        # если мы касаемся игрового поля, сдвигаем его (для приятного эффекта столкновения с границей поля)
        dx = block.move_left(board, fps)
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

    # обновляем блок, передаём туда поле и координаты блока для проверки на столкновение
    block.update(board, fps)
    block.shadow(screen, board)  # рисуем тень блока (куда он падает)
    block.draw(screen)  # рисуем блок

    particles_group.update(fps)  # обновляем все частицы
    particles_group.draw(screen)  # рисуем все частицы

    show_next_block()  # рисуем следующий блок
    show_time(pygame.time.get_ticks())  # отображаем время проведенное в матче
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
    block = BLOCKS[block_index](all_group, board.rect.x, board.rect.y, cell_size, speed, color_index, sfx_volume)
    return block, spawn_block_list, flag_shake_y


def show_next_block():  # показывает следующий блок который заспавнится
    # левый верхний угол где показывается блок
    x, y = 670, 250
    if language == 'ru':  # если ру будет СЛЕДУЮЩИЙ длинное слово, надо поставить его левее
        x -= 30
    font = pygame.font.SysFont(None, 30)
    # рисуем надпись по теме
    img_text = font.render(f'{translations[language]['Next']}: ', 1, (255, 255, 255) if theme else (0, 0, 0))
    screen.blit(img_text, (x, y))

    # выбираем 2 блок из списка тк это индексы будущего блока
    block_index = spawn_block_list[1][0]
    color_index = spawn_block_list[1][1]

    # вызываем класс блока и рисуем его на экране
    show_block = BLOCKS[block_index](all_group, x - 70, y + 50, 20, 0, color_index, sfx_volume)
    show_block.kill()  # убиваем его из группы он там не нужен
    show_block.draw(screen)


def show_time(ticks):
    font = pygame.font.SysFont(None, 30)
    time = (ticks - start_time) // 1000
    time = f'{time // 60:02d}:' + f'{time % 60:02d}'
    img_time = font.render(time, 1, (255, 255, 255) if theme else (0, 0, 0))
    img_time_text = font.render(translations[language]['Time'], 1, (255, 255, 255) if theme else (0, 0, 0))

    screen.blit(img_time_text, (660, 140))
    screen.blit(img_time, (670 + img_time_text.get_width(), 140))


def button_set():
    pause_button = Button(WIDTH - 770, 20, 80, 40, translations[language]['Pause'],
                          ((0, 0, 0) if theme else (255, 255, 255)),
                          hover_color='gray', text_size=30, theme=theme)

    continue_button = Button((WIDTH - 200) // 2, HEIGHT // 2 - 50 - 10, 200, 60, translations[language]['Continue'],
                             ((0, 0, 0) if theme else (255, 255, 255)), hover_color='gray', text_size=30, theme=theme)

    back_to_menu_button = Button((WIDTH - 200) // 2, HEIGHT // 2 + 50 + 10, 200, 60,
                                 translations[language]['Back to menu'],
                                 ((0, 0, 0) if theme else (255, 255, 255)), hover_color='gray', text_size=30,
                                 theme=theme)

    restart_button = Button((WIDTH - 200) // 2, HEIGHT // 2 + 100 + 30, 200, 60, translations[language]['Restart'],
                            ((0, 0, 0) if theme else (255, 255, 255)), hover_color='gray', text_size=30, theme=theme)

    return pause_button, continue_button, back_to_menu_button, restart_button


if __name__ == '__main__':
    pygame.init()
    pygame_icon = pygame.image.load('data/tetris_logo.png')
    pygame.display.set_icon(pygame_icon)
    screen = pygame.display.set_mode(SIZE)
    screen.fill((255, 255, 255))
    pygame.display.flip()
    # проверяем на наличие базы данных, если нету создаём пустую
    if not os.path.isfile(database_path):
        if not os.path.isdir('data'):
            os.mkdir('data')
        create_table()

    # получаем настройки пользователя из бд
    music_volume, sfx_volume, difficulty, language, theme = get_player_settings()
    settings_ui = SettingsUI(music_volume, sfx_volume, difficulty, language, theme)  # инициализируем настройки
    music_volume = music_volume / 100
    sfx_volume = sfx_volume / 100

    pygame.display.set_caption('tetris')
    settings_ui.options['difficulty'] = difficulty  # загружаем сложность
    settings_ui.change_speed_block()

    all_group = pygame.sprite.Group()
    particles_group = pygame.sprite.Group()  # группа для частиц после поломки блоков

    clock = pygame.time.Clock()
    running = True

    defeat = False
    tetris_game_running = False
    start_menu = True
    show_statistic = False
    is_paused = False
    result_show = False
    log_in_menu_show = False
    new_record = False
    flag_shake_y = 0
    score = 0
    level = 1

    camera = Camera()

    board = Board(all_group, 10, 21)
    cell_size = 40
    cell_height = 21
    cell_width = 10
    left = (WIDTH - (cell_width * cell_size)) // 2
    top = (HEIGHT - (cell_height * cell_size)) // 2 - 30
    board.set_view(left, top, cell_size)

    power_shake_y = 1  # сила тряски блока при приземлении
    speed = settings_ui.options.get('block_speed', 1)  # столько блоков в секунду падает блок

    pos = 0, 0

    # создадим кнопку паузу по теме
    pause_button, continue_button, back_to_menu_button, restart_button = button_set()

    menu_ui = MenuUI(WIDTH, HEIGHT, theme, language=language)

    # музыка на фон
    play_music = pygame.mixer.Sound('data/sounds/base_music_fon.mp3')
    # звук музыку на фон
    play_music.set_volume(music_volume)
    # музыка в бесконечном цикле
    play_music.play(-1)

    new_record_sound = pygame.mixer.Sound('data/sounds/new_record.mp3')
    new_record_sound.set_volume(sfx_volume)

    while running:
        # показ фпс
        fps = int(clock.get_fps())
        if fps < 60:
            fps = 60
        pygame.display.set_caption(f'fps - {fps}')
        # заливаем фон цветом темы
        screen.fill(settings_ui.bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # выход из приложения нажатие на крестик
                running = False

            if event.type == pygame.MOUSEMOTION:
                pos = event.pos

            if tetris_game_running and event.type == pygame.KEYDOWN:  # отслеживаем нажатие клавиш в игровом процессе
                if event.key == pygame.K_UP or event.key == pygame.K_w:  # нажали на стрелочку вверх - переворачиваем блок на 90 градусов
                    block.rotation(board)
                if event.key == pygame.K_SPACE:  # нажали на пробел - моментальный моментальное падение блока
                    block.instant_fall(board)
                if event.key == pygame.K_ESCAPE:
                    is_paused = True

            elif tetris_game_running and event.type == pygame.KEYUP:  # отслеживаем отпускание клавиш в игровом процессе
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # перестаём ускорять блок если отпустили клавишу
                    block.speed = speed

            elif event.type == pygame.USEREVENT:
                if event.button == pause_button:
                    is_paused = True
                elif event.button == back_to_menu_button:  # возвращаемся в меню после поражения
                    board.clear()
                    defeat = False
                    tetris_game_running = False
                    start_menu = True
                elif event.button == restart_button:  # перезапуск игры после поражения
                    board.clear_destroy(particles_group)
                    spawn_block_list = [(random.randint(0, 6), random.randint(0, 6)),
                                        (random.randint(0, 6), random.randint(0, 6))]
                    # спавним блок
                    block, spawn_block_list, flag_shake_y = spawn_new_block(flag_shake_y,
                                                                            spawn_block_list=spawn_block_list)
                    score = 0
                    start_time = pygame.time.get_ticks()
                    defeat = False
                    start_menu = False
                    tetris_game_running = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pause_button.handle_event(event)
                if defeat:  # ловим кнопки при поражении
                    back_to_menu_button.handle_event(event)
                    restart_button.handle_event(event)

                # Логика для главного меню
                if start_menu:
                    action = menu_ui.get_button_action(event)  # ловим действие происходящее в меню

                    if action == menu_ui.continue_button and start_menu:  # нажата клавиша continue
                        # список индексов блоков которые будут появляться
                        spawn_block_list = [(random.randint(0, 6), random.randint(0, 6)),
                                            (random.randint(0, 6), random.randint(0, 6))]
                        # спавним блок
                        block, spawn_block_list, flag_shake_y = spawn_new_block(flag_shake_y,
                                                                                spawn_block_list=spawn_block_list)
                        start_time = pygame.time.get_ticks()
                        start_menu = False
                        tetris_game_running = True

                    elif action == menu_ui.settings_button:  # нажата клавиша settings
                        settings_open = True

                        # Открытые настройки в главном меню
                        while settings_open:
                            settings_ui.render(screen)
                            play_music.set_volume(music_volume)
                            pygame.display.flip()
                            for settings_event in pygame.event.get():

                                # передаём event в обработку в настройки
                                settings_action = settings_ui.handle_event(settings_event)
                                menu_ui.render(screen)

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

                                elif settings_action == "sfx volume":
                                    sfx_volume = settings_ui.options["sfx_volume"] / 100
                                    new_record_sound.set_volume(sfx_volume)

                                elif settings_action == "difficulty":
                                    speed = settings_ui.options.get('block_speed')

                                # смена цветовой темы приложения
                                elif settings_action == "theme":
                                    menu_ui.change_theme()
                                    theme = int(not theme)  # так как 2 темы, меняем её на противоположную
                                    pause_button, continue_button, back_to_menu_button, restart_button = button_set()

                                # меняем язык
                                elif settings_action == 'language':
                                    # передаём язык в меню
                                    language = settings_ui.options['language']
                                    menu_ui.change_language(language)
                                    pause_button, continue_button, back_to_menu_button, restart_button = button_set()
                            # последняя сточка настроек

                    # нажали на кнопку Results
                    elif action == menu_ui.results_button:
                        show_statistic = True

                    # нажали на кнопку Exit
                    elif action == menu_ui.save_exit_button:
                        running = False

                    # нажали на кнопку Log in
                    elif action == menu_ui.log_in_button:
                        log_in_menu_show = True

        # Логика паузы
        if is_paused:
            pause_time = pygame.time.get_ticks()
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
                img_font = font.render(translations[language]['PAUSED'], 1, ((255, 255, 255) if theme else (0, 0, 0)))
                # надпись кол-во очков
                score_text = font_score.render(f"{translations[language]['Score']}: {score}", True,
                                               ((255, 255, 255) if theme else (0, 0, 0)))

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

                show_time(pause_time)
                pygame.display.flip()

            start_time += pygame.time.get_ticks() - pause_time

        # ЛОГИКА ОТОБРАЖЕНИЕ ЭКРАНОВ
        if start_menu:
            if show_statistic:
                ui_show_statistic(screen, theme, language)
                show_statistic = False
            elif log_in_menu_show:
                play_music.stop()
                signal = show_log_in(screen, theme, language)
                if signal == 'change':
                    # получаем настройки пользователя из бд
                    music_volume, sfx_volume, difficulty, language, theme = get_player_settings()
                    settings_ui = SettingsUI(music_volume, sfx_volume, difficulty, language, theme)
                    # инициализируем настройки
                    music_volume = music_volume / 100
                    sfx_volume = sfx_volume / 100
                    menu_ui = MenuUI(WIDTH, HEIGHT, theme, language=language)
                    pause_button, continue_button, back_to_menu_button, restart_button = button_set()
                log_in_menu_show = False
                play_music.set_volume(music_volume)
                play_music.play()
            else:
                screen.fill(settings_ui.bg_color)
                font = pygame.font.Font(None, 50)
                player = get_player_name()
                active_player_text_surface = font.render(player, True, (255, 255, 255) if theme else (0, 0, 0))
                screen.blit(active_player_text_surface, (WIDTH // 2 - active_player_text_surface.get_width() // 2, 100))
                main_menu()
                menu_ui.handle_event(event)

        if tetris_game_running:
            # ход игры
            # логика тряски экрана при приземлении
            flag_shake_y = gameplay(flag_shake_y)

            # рисуем очки
            font = pygame.font.SysFont(None, 30)
            score_text = font.render(f"{translations[language]['Score']}: {score}", True,
                                     (255, 255, 255) if theme else (0, 0, 0))
            screen.blit(score_text, (640, 70))

        elif defeat:
            show_time(end_time)  # показываем сколько длилась игра
            font = pygame.font.SysFont(None, 30)
            # показываем очки
            score_text = font.render(f"{translations[language]['Score']}: {score}", True,
                                     (255, 255, 255) if theme else (0, 0, 0))
            screen.blit(score_text, (640, 70))
            board.render(screen)
            font = pygame.font.SysFont(None, 100)
            # показываем надпись поражения
            img = font.render(translations[language]["YOU LOSE!"], 1, (255, 255, 255) if theme else (0, 0, 0))
            screen.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height()))

            if new_record:
                font = pygame.font.SysFont(None, 90)
                img_new_record = font.render(translations[language]["NEW RECORD"], 1,
                                             (255, 255, 255) if theme else (0, 0, 0))
                screen.blit(img_new_record,
                            (WIDTH // 2 - img_new_record.get_width() // 2, 10))

            # показываем кнопки
            restart_button.check_hover(pos)
            restart_button.draw(screen)
            back_to_menu_button.check_hover(pos)
            back_to_menu_button.draw(screen)

        # Проверка игры и логика спавна нового блока
        if tetris_game_running and block.is_ground:
            block, spawn_block_list, flag_shake_y = spawn_new_block(flag_shake_y, block,
                                                                    spawn_block_list=spawn_block_list)
            if block:  # проверка на блок иначе на поражение
                lines_filled = board.check_fill_line(particles_group)
                # если при падении блока заполнилась линия, увеличить силу тряски
                if lines_filled > 0:
                    score += 100
                    lines_filled -= 1
                    score += lines_filled * 150
                    if lines_filled == 3:
                        score += 50
                    power_shake_y = 4
                else:  # иначе поставить её обычную
                    power_shake_y = 1
            else:
                # Момент поражения в игре
                end_time = pygame.time.get_ticks()
                new_record = save_result_in_db(score, (end_time - start_time) // 1000)
                if new_record:
                    new_record_sound.play()
                defeat = True
                tetris_game_running = False

        play_music.set_volume(music_volume)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
