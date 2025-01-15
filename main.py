import random

import pygame

from blocks import *
from board import Board
from Button import ColorButton

SIZE = WIDTH, HEIGHT = 800, 900
FPS = 60

BLOCKS = [ZBlock, SBlock, IBlock, LBlock, TBlock, JBlock, OBlock]


def main_menu():
    start_button.check_hover(pos)
    start_button.draw(screen)


def gameplay():
    board.render(screen)
    block.update(colliders)
    block.shadow(screen, colliders)
    block.draw(screen)


def show_defeat():
    board.render(screen)
    restart_button.check_hover(pos)
    restart_button.draw(screen)
    exit_to_main_menu.check_hover(pos)
    exit_to_main_menu.draw(screen)
    font = pygame.font.SysFont(None, 100)
    img = font.render('you lose!', 1, (255, 255, 255), '#34495e')
    screen.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height()))


def spawn_new_block(block=None):
    defeat = False
    index = random.randint(0, 6)
    # если у нас есть блок, то оставим его снизу
    if block:
        # переберём все ректы и поставим их в сетке
        color_index = block.color_index
        for rect in block.rects:
            x, y = rect.center
            cell = board.get_cell((x, y))
            board.create_block(cell, color_index)
            if cell[1] < 2:  # проверяем есть ли блок выше игрового поля
                defeat = True
                # если да, мы проиграли
        if defeat:
            return False
    block = BLOCKS[index](all_group, left, top, cell_size, speed)
    return block


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('tetris')

    clock = pygame.time.Clock()
    running = True

    defeat = False
    tetris_game_running = False
    start_menu = True

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

    width = 260
    height = 80
    start_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) - 150, width, height,
                               'start game', 'black', hover_color='gray', text_size=40)

    restart_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) + 120, width, height,
                                 'Restart game', '#34495e', hover_color='gray', text_size=40)
    exit_to_main_menu = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) + 220, width, height,
                                    'go to menu', '#34495e', hover_color='gray', text_size=40)

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
                    start_menu = False
                    tetris_game_running = True
                    board.clear()
                    block = spawn_new_block()
                elif event.button == restart_button:
                    start_menu = False
                    tetris_game_running = True
                    board.clear()
                    block = spawn_new_block()
                elif event.button == exit_to_main_menu:
                    start_menu = True
                    tetris_game_running = False

            if start_menu:
                start_button.handle_event(event)
            elif defeat:
                restart_button.handle_event(event)
                exit_to_main_menu.handle_event(event)

        if tetris_game_running and block.is_ground:
            block = spawn_new_block(block)
            if block:
                board.check_fill_line()
            else:
                defeat = True
                tetris_game_running = False

        if start_menu:
            # отрисовка начального меню
            main_menu()

        elif tetris_game_running:
            board.update(colliders)
            # отрисовка игры
            gameplay()

        elif defeat:
            # отрисовка поражения
            show_defeat()

        colliders.clear()
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
