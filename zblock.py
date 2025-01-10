import pygame
import os
import sys
from block import Block

CELL_SIZE = 40


def load_image(name):
    fullname = os.path.join('image', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class ZBlock(Block):
    block_image = load_image('1.png')
    block_image = pygame.transform.scale(block_image, (CELL_SIZE * 3, CELL_SIZE * 2))

    def __init__(self, group, left, top, cell_size):
        super().__init__(cell_size)
        self.image = pygame.Surface((CELL_SIZE * 3, CELL_SIZE * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.fill_rects()

    def fill_rects(self):
        self.rects = []
        x, y = self.rect.topleft
        x, y = x + 5, y + 5
        self.rects.append(pygame.Rect(x + 40, y, 30, 30))
        self.rects.append(pygame.Rect(x + 80, y, 30, 30))
        self.rects.append(pygame.Rect(x, y + 40, 30, 30))
        self.rects.append(pygame.Rect(x + 40, y + 40, 30, 30))
