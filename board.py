import copy
import pygame
from block import load_image


class Board(pygame.sprite.Sprite):
    block = load_image('block.png')
    block = pygame.transform.scale(block, (40, 40))

    # создание поля
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 20
        self.top = 20
        self.cell_size = 60
        self.step = 0
        self.first_step = True
        self.color_step = None

    # настройка внешнего вида
    def set_view(self, left, top, cell_size, vertical_borders, horizontal_borders):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.create_borders(vertical_borders, horizontal_borders)

    def create_borders(self, vertical_borders, horizontal_borders):
        x1, y1 = self.left, self.top
        x2, y2 = self.left + (self.width * self.cell_size), self.top + (self.height * self.cell_size)
        rect = pygame.Rect(x1 - 1, y1, 1, self.cell_size * self.height)
        rect2 = pygame.Rect(x2, y1, 1, self.cell_size * self.height)
        rect3 = pygame.Rect(x1, y2, self.width * self.cell_size, 10)
        vertical_borders.append(rect)
        vertical_borders.append(rect2)
        horizontal_borders.append(rect3)

    def render(self, screen):
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                x = self.left + self.cell_size * j
                y = self.top + self.cell_size * i
                if elem == 0:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                elif elem == 1:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (x + 5, y + 5,
                                      30, 30), 5)

                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def update(self, vertical_borders, horizontal_borders):
        self.create_borders(vertical_borders, horizontal_borders)
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                if bool(elem):
                    x = self.cell_size * j + self.left
                    y = self.cell_size * i + self.top
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    vertical_borders.append(rect)
                    horizontal_borders.append(rect)

    def get_cell(self, pos):
        x, y = pos
        x -= self.left
        y -= self.top
        x //= self.cell_size
        y //= self.cell_size
        if (x >= 0 and y >= 0) and (
                x < self.width and y < self.height):
            return x, y
        return None

    def create_block(self, cell):
        x = cell[0]
        y = cell[1]
        self.board[y][x] = 1
#
#
# if __name__ == '__main__':
#     a = 30
#     size = width, height = 700, 700
#     pygame.init()
#     screen = pygame.display.set_mode(size)
#     line = Lines(10, 10)
#     running = True
#     clock = pygame.time.Clock()
#     speed = 5
#     start_game = False
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN and not start_game:
#                 line.get_click(event.pos)
#         screen.fill((0, 0, 0))
#         line.go()
#         line.render(screen)
#         clock.tick(speed)
#         pygame.display.flip()
