import pygame
from block import Block


class TBlock(Block):
    def __init__(self, left, top, cell_size, speed):
        super().__init__(cell_size, speed)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[0, 1, 0],
                      [1, 1, 1]]


class SBlock(Block):
    def __init__(self, left, top, cell_size, speed):
        super().__init__(cell_size, speed)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[0, 1, 1],
                      [1, 1, 0]]


class OBlock(Block):
    def __init__(self, left, top, cell_size, speed):
        super().__init__(cell_size, speed)
        self.image = pygame.Surface((cell_size * 2, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[1, 1],
                      [1, 1]]


class IBlock(Block):
    def __init__(self, left, top, cell_size, speed):
        super().__init__(cell_size, speed)
        self.image = pygame.Surface((cell_size * 4, cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 3
        self.rect.y = top
        self.cords = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [1, 1, 1, 1],
                      [0, 0, 0, 0]]


class LBlock(Block):
    def __init__(self, left, top, cell_size, speed):
        super().__init__(cell_size, speed)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[0, 0, 1],
                      [1, 1, 1]]


class JBlock(Block):
    def __init__(self, left, top, cell_size, speed):
        super().__init__(cell_size, speed)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[1, 0, 0],
                      [1, 1, 1]]


class ZBlock(Block):
    def __init__(self, left, top, cell_size, speed):
        super().__init__(cell_size, speed)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[1, 1, 0],
                      [0, 1, 1]]
