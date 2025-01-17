import random
import sqlite3

import pygame

from blocks import ZBlock, SBlock, IBlock, LBlock, TBlock, JBlock, OBlock
from board import Board
from Button import ColorButton
from menu_show import main_menu, show_statistics
from gameplay_show import gameplay
from defeat_show import show_defeat
from variables import *

FPS = 60
BLOCKS = [ZBlock, SBlock, IBlock, LBlock, TBlock, JBlock, OBlock]


def spawn_new_block(block=None, spawn_block_list=None):
    defeat = False
    # если у нас есть блок, то оставим его снизу
    if block:
        # переберём все ректы и поставим их в сетке
        color_index = spawn_block_list[0][1] + 1
        spawn_block_list = spawn_block_list[1::]
        spawn_block_list.append((random.randint(0, 6), random.randint(0, 6)))
        for rect in block.rects:
            x, y = rect.center
            cell = board.get_cell((x, y))
            board.create_block(cell, color_index)
            if cell[1] < 2:  # проверяем есть ли блок выше игрового поля
                defeat = True
                # если да, мы проиграли
        if defeat:
            return False, spawn_block_list
    block_index = spawn_block_list[0][0]  # определяем какой блок заспавниться
    color_index = spawn_block_list[0][1]  # определяем цвет блока
    block = BLOCKS[block_index](left, top, cell_size, speed, color_index)
    return block, spawn_block_list


def save_result_in_db(score, time):
    con = sqlite3.connect('data/tetris.db')
    cur = con.cursor()
    query = """SELECT * FROM stats INNER JOIN players on players.id = stats.player_id
                    WHERE player = (SELECT player FROM players WHERE active_player = 1)"""
    result = cur.execute(query).fetchone()
    best_score = result[1]
    all_score = result[2] + score
    all_time = result[3] + time
    if score > best_score:
        best_score = score
    query = """UPDATE
            stats
        SET
            best_score = ?,
            all_score = ?,
            play_time = ?
        WHERE player_id = (SELECT id FROM players WHERE active_player = 1)"""
    cur.execute(query, (best_score, all_score, all_time))
    con.commit()
    con.close()
    print('данные в бд сохранены', best_score, all_score, all_time)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('tetris')

    clock = pygame.time.Clock()
    running = True

    start_menu = True
    statistics_menu = False
    tetris_game_running = False
    defeat = False
    statistical_data_received = False

    board = Board(10, 21)
    cell_size = 40
    cell_height = 21
    cell_width = 10
    colliders = []
    all_group = pygame.sprite.Group()
    left = (WIDTH - (cell_width * cell_size)) // 2
    top = (HEIGHT - (cell_height * cell_size)) // 2 - 30
    board.set_view(left, top, cell_size, colliders)

    speed = 2
    spawn_block_list = [(random.randint(0, 6), random.randint(0, 6)), (random.randint(0, 6), random.randint(0, 6))]

    width = 260
    height = 80
    start_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) - 150, width, height,
                               'start game', 'black', hover_color='gray', text_size=40)
    stats_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) - 50, width, height,
                               'stats', 'black', hover_color='gray', text_size=40)
    #
    # back_button_in_statistic = ColorButton(WIDTH * 0.05, HEIGHT * 0.05, width, height,
    #                                        'Back', 'black', hover_color='gray', text_size=40)

    restart_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) + 120, width, height,
                                 'Restart game', '#34495e', hover_color='gray', text_size=40)
    exit_to_main_menu = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) + 220, width, height,
                                    'exit to menu', '#34495e', hover_color='gray', text_size=40)

    pos = 0, 0

    while running:
        board.update(colliders)  # заполняем коллайдеры, без этого не будут работать столкновения
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif tetris_game_running and event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_DOWN]:
                    block.speed = 20
                if event.key == pygame.K_RIGHT:
                    block.move_right(colliders)
                if event.key == pygame.K_LEFT:
                    block.move_left(colliders)
                if event.key == pygame.K_UP:
                    block.rotation(colliders)
                if event.key == pygame.K_SPACE:
                    block.instant_fall(colliders)
            elif tetris_game_running and event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    block.speed = speed

            elif event.type == pygame.MOUSEMOTION:
                pos = event.pos
                print(print(pos))

            elif event.type == pygame.USEREVENT:
                if event.button == start_button:
                    defeat = False
                    start_menu = False
                    tetris_game_running = True
                    board.clear()
                    block, spawn_block_list = spawn_new_block(spawn_block_list=spawn_block_list)
                    start_time = pygame.time.get_ticks()

                elif event.button == stats_button:
                    statistics_menu = True

                elif event.button == restart_button:
                    defeat = False
                    start_menu = False
                    tetris_game_running = True
                    board.clear()
                    block, spawn_block_list = spawn_new_block(spawn_block_list=spawn_block_list)
                    start_time = pygame.time.get_ticks()

                elif event.button == exit_to_main_menu:
                    defeat = False
                    start_menu = True
                    tetris_game_running = False
                    statistics_menu = False

            if start_menu:
                if statistics_menu:  # если мы в статистике
                    exit_to_main_menu.handle_event(event)
                else:
                    stats_button.handle_event(event)
                    start_button.handle_event(event)

            elif defeat:
                restart_button.handle_event(event)
                exit_to_main_menu.handle_event(event)

        if tetris_game_running and block.is_ground:
            block, spawn_block_list = spawn_new_block(block, spawn_block_list)
            if block:
                board.check_fill_line()  # проверяем линии на заполненность
            else:
                # если мы проиграли
                defeat = True
                tetris_game_running = False
                end_time = pygame.time.get_ticks()
                save_result_in_db(board.score, (end_time - start_time) // 1000)

        if start_menu:
            # меню игры
            if statistics_menu:
                # рисуем статистику
                show_statistics(screen, exit_to_main_menu, pos)
            else:
                # отрисовка начального меню
                main_menu(screen, start_button, stats_button, pos)

        elif tetris_game_running:
            # отрисовка игры
            gameplay(screen, board, block, colliders, spawn_block_list, start_time, BLOCKS)

        elif defeat:
            # отрисовка поражения
            show_defeat(screen, board, restart_button, exit_to_main_menu, start_time, end_time, pos)

        colliders.clear()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
