import pygame
from block import Block


class OBlock(Block):
    def __init__(self, group, left, top, cell_size):
        super().__init__(cell_size)
        self.image = pygame.Surface((cell_size * 2, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.fill_rects()
        self.cords = [[1, 1],
                      [1, 1]]
