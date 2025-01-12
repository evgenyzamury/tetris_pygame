import copy
import pygame
from pprint import pprint


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
        self.score = 0

    def set_view(self, left, top, cell_size, vertical_borders, horizontal_borders):  # настройка внешнего вида
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.create_borders(vertical_borders, horizontal_borders)

    def create_borders(self, vertical_borders, horizontal_borders):
        # делаем стенки нашего поля, левое - правое - нижнее
        x1, y1 = self.left, self.top
        x2, y2 = self.left + (self.width * self.cell_size), self.top + (self.height * self.cell_size)
        # создание боковых границ
        left_rect = pygame.Rect(x1 - 50, y1, 50, self.cell_size * self.height)
        right_rect = pygame.Rect(x2, y1, 50, self.cell_size * self.height)
        # создадим rect для нижней границы
        horizontal_rect = pygame.Rect(x1, y2, self.width * self.cell_size, 40)
        vertical_borders.append(left_rect)
        vertical_borders.append(right_rect)
        horizontal_borders.append(horizontal_rect)

    def render(self, screen):
        # отрисовка нашего игрового поля
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
                # 660 80
        font = pygame.font.SysFont(None, 32)
        img = font.render('SCORE:', 1, (255, 255, 255))
        img_score = font.render(f'{self.score}', 1, (255, 255, 255))
        screen.blit(img, (660, 80))
        screen.blit(img_score, (660, 110))

    def update(self, vertical_borders, horizontal_borders):
        # функция для обновления списка коллайдеров
        self.create_borders(vertical_borders, horizontal_borders)
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                # если элемент не пустой создаём коллайдер
                if bool(elem):
                    x = self.cell_size * j + self.left
                    y = self.cell_size * i + self.top
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    vertical_borders.append(rect)
                    horizontal_borders.append(rect)

    def get_cell(self, pos):
        # узнаем клетку поля по координатам окна
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
        # создаем блок на поле
        x = cell[0]
        y = cell[1]
        self.board[y][x] = 1

    def check_fill_line(self):
        count_lines = 0
        # создаём список координат оси y, чтобы отследить где заполнились линии
        need_y = []
        for y, line in enumerate(self.board):
            if all(line):
                count_lines += 1
                self.board[y] = [0 for _ in range(self.width)]  # убираем блоки с заполненной линии
                need_y.append(y)
        else:
            # если есть хоть 1 заполненная линия роняем блоки
            if count_lines:
                self.fall_block_after_fill_lines(need_y, count_lines)
                self.add_points(count_lines)

    def fall_block_after_fill_lines(self, y, count):
        # роняем блоки при заполнении линий
        for index in range(count):
            for i in range(y[index], 0, -1):
                self.board[i] = self.board[i - 1]

    def add_points(self, count_lines):
        self.score += 1000 * count_lines
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
