import copy
import pygame


class Board(pygame.sprite.Sprite):
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
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size, self.cell_size), 0)

                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x -= self.left
        y -= self.top
        x //= self.cell_size
        y //= self.cell_size
        if (x >= 0 and y >= 0) and (
                x < self.width and y < self.height):
            return x, y
        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell):
        if cell:
            x, y = cell
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
