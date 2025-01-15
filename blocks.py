import pygame
from block import Block


class TBlock(Block):
    def __init__(self, all_group, left, top, cell_size, speed, color_index):
        super().__init__(all_group, cell_size, speed, color_index)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[0, 1, 0],
                      [1, 1, 1]]
        self.fill_rects(self.rects)


class SBlock(Block):
    def __init__(self, all_group, left, top, cell_size, speed, color_index):
        super().__init__(all_group, cell_size, speed, color_index)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[0, 1, 1],
                      [1, 1, 0]]
        self.fill_rects(self.rects)


class OBlock(Block):
    def __init__(self, all_group, left, top, cell_size, speed, color_index):
        super().__init__(all_group, cell_size, speed, color_index)
        self.image = pygame.Surface((cell_size * 2, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[1, 1],
                      [1, 1]]
        self.fill_rects(self.rects)


class IBlock(Block):
    def __init__(self, all_group, left, top, cell_size, speed, color_index):
        super().__init__(all_group, cell_size, speed, color_index)
        self.image = pygame.Surface((cell_size * 4, cell_size))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 3
        self.rect.y = top
        self.cords = [[0, 0, 0, 0],
                      [1, 1, 1, 1],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.fill_rects(self.rects)


class LBlock(Block):
    def __init__(self, all_group, left, top, cell_size, speed, color_index):
        super().__init__(all_group, cell_size, speed, color_index)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[0, 0, 1],
                      [1, 1, 1]]
        self.fill_rects(self.rects)


class JBlock(Block):
    def __init__(self, all_group, left, top, cell_size, speed, color_index):
        super().__init__(all_group, cell_size, speed, color_index)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[1, 0, 0],
                      [1, 1, 1]]
        self.fill_rects(self.rects)


class ZBlock(Block):
    def __init__(self, all_group, left, top, cell_size, speed, color_index):
        super().__init__(all_group, cell_size, speed, color_index)
        self.image = pygame.Surface((cell_size * 3, cell_size * 2))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.cords = [[1, 1, 0],
                      [0, 1, 1]]
        self.fill_rects(self.rects)
