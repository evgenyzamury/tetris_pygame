import pygame
from block import Block


class ZBlock(Block):
    def __init__(self, group, left, top, cell_size):
        super().__init__(cell_size)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
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
