import pygame
from block import Block


class IBlock(Block):
    def __init__(self, group, left, top, cell_size):
        super().__init__(cell_size)
        self.image = pygame.Surface((cell_size, cell_size * 4))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[1],
                      [1],
                      [1],
                      [1]]
