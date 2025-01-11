import pygame
from block import Block


class IBlock(Block):
    def __init__(self, group, left, top, cell_size):
        super().__init__(cell_size)
        self.image = pygame.Surface((cell_size, cell_size * 4))
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top

    def fill_rects(self):
        self.rects = []
        x, y = self.rect.topleft
        x, y = x + 5, y + 5
        self.rects.append(pygame.Rect(x, y, 30, 30))
        self.rects.append(pygame.Rect(x, y + 40, 30, 30))
        self.rects.append(pygame.Rect(x, y + 80, 30, 30))
        self.rects.append(pygame.Rect(x, y + 120, 30, 30))
