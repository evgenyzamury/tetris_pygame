import pygame
import random
from board import Board
from zblock import ZBlock
from iblock import IBlock
from lblock import LBlock
from tblock import TBlock

SIZE = WIDTH, HEIGHT = 800, 800
FPS = 60

BLOCKS = [ZBlock, IBlock, LBlock, TBlock]


def colliders_clear(vertical_borders, horizontal_borders):
    vertical_borders.clear()
    horizontal_borders.clear()


def spawn_new_block(block=None):
    index = random.randint(0, 3)
    # если у нас есть блок, то оставим его снизу
    if block:
        # переберём все ректы и поставим их в сетке
        for rect in block.rects:
            x, y = rect.center
            cell = board.get_cell((x, y))
            board.create_block(cell)
    block = BLOCKS[index](all_group, left, top, cell_size)
    return block


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('shablon')

    clock = pygame.time.Clock()
    running = True

    board = Board(10, 19)
    cell_size = 40

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
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_DOWN]:
                    block.speed = 20
                if event.key == pygame.K_RIGHT:
                    block.move_right()
                if event.key == pygame.K_LEFT:
                    block.move_left()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    block.speed = 4

        if block.is_ground:
            block = spawn_new_block(block)

        board.render(screen)

        block.draw(screen)
        block.update(horizontal_borders)

        all_group.draw(screen)
        all_group.update(vertical_borders, horizontal_borders)
        colliders_clear(vertical_borders, horizontal_borders)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
