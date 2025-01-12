import random

import pygame

from blocks import *
from board import Board

SIZE = WIDTH, HEIGHT = 800, 800
FPS = 60

BLOCKS = [ZBlock, SBlock, IBlock, LBlock, TBlock, JBlock, OBlock]


def colliders_clear(vertical_borders, horizontal_borders):
    vertical_borders.clear()
    horizontal_borders.clear()


def spawn_new_block(block=None):
    index = random.randint(0, 6)
    # если у нас есть блок, то оставим его снизу
    if block:
        # переберём все ректы и поставим их в сетке
        for rect in block.rects:
            x, y = rect.center
            cell = board.get_cell((x, y))
            if cell:
                board.create_block(cell)
            else:
                return False
    block = BLOCKS[index](left, top - 120, cell_size)
    return block


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('shablon')

    clock = pygame.time.Clock()
    running = True

    board = Board(10, 19)
    cell_size = 40

    defeat = False
    tetris_game_running = True
    start_menu = False

    cell_height = 19
    cell_width = 10
    vertical_borders = []
    horizontal_borders = []
    all_group = pygame.sprite.Group()

    left = (WIDTH - (cell_width * cell_size)) // 2
    top = (HEIGHT - (cell_height * cell_size)) // 2

    board.set_view(left, top, cell_size, vertical_borders, horizontal_borders)
    block = spawn_new_block()

    while running:
        board.update(vertical_borders, horizontal_borders)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif tetris_game_running and event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_DOWN]:
                    block.speed = 20
                if event.key == pygame.K_RIGHT:
                    block.move_right(vertical_borders)
                if event.key == pygame.K_LEFT:
                    block.move_left(vertical_borders)
                if event.key == pygame.K_UP:
                    block.rotation(vertical_borders)
                if event.key == pygame.K_SPACE:
                    block.instant_fall(horizontal_borders)
            elif tetris_game_running and event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    block.speed = 4

            elif event.type == pygame.MOUSEMOTION:
                print(event.pos)

        if tetris_game_running and block.is_ground:
            block = spawn_new_block(block)
            if block:
                board.check_fill_line()
            else:
                defeat = True
                tetris_game_running = False

        board.render(screen)

        if start_menu:
            print('start_menu')
            # отрисовка начального меню
            pass

        elif tetris_game_running:
            print('gaming')

            block.draw(screen)
            block.update(horizontal_borders)

            all_group.draw(screen)
            all_group.update(vertical_borders, horizontal_borders)
        elif defeat:
            print('defeats')
            # отрисовка поражения
            pass

        colliders_clear(vertical_borders, horizontal_borders)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
