import pygame
from block import Block


class LBlock(Block):
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

    # def update(self, h):
    #     self.tick += self.speed / 60
    #     if self.tick >= 1:
    #         if not self.is_ground:
    #             self.rect.y += 1
    #             if self.rect.collidelist(h) != -1:
    #                 self.rect.y -= 0
    #                 self.is_ground = True
    #             else:
    #                 self.rect.y += self.cell_size
    #             self.rect.y -= 1
    #         else:
    #             self.kill()
    #         self.tick = 0
    #
    # def move_right(self):
    #     self.rect.x += self.cell_size
    #
    # def move_left(self):
    #     self.rect.x -= self.cell_size
    #
    # def draw(self, screen):
    #     x, y = self.rect.topleft
    #     x, y = x + 5, y + 5
    #     pygame.draw.rect(screen, (255, 255, 255), (x, y, 30, 30), 5)
    #     pygame.draw.rect(screen, (255, 255, 255), (x, y + 40, 30, 30), 5)
    #     pygame.draw.rect(screen, (255, 255, 255), (x, y + 80, 30, 30), 5)
    #     pygame.draw.rect(screen, (255, 255, 255), (x, y + 120, 30, 30), 5)
