import copy
import pygame
from pprint import pprint
from variables import COLOR, WIDTH, HEIGHT


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

    def set_view(self, left, top, cell_size, colliders):  # настройка внешнего вида
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.create_borders(colliders)

    def create_borders(self, colliders):
        # делаем стенки нашего поля, левое - правое - нижнее
        x1, y1 = self.left, self.top
        x2, y2 = self.left + (self.width * self.cell_size), self.top + (self.height * self.cell_size)
        # создание боковых границ
        left_rect = pygame.Rect(x1 - 50, y1 - 100, 50, self.cell_size * self.height + 100)
        right_rect = pygame.Rect(x2, y1 - 100, 50, self.cell_size * self.height + 100)
        # создадим rect для нижней границы
        horizontal_rect = pygame.Rect(x1, y2, self.width * self.cell_size, 40)
        colliders.append(left_rect)
        colliders.append(right_rect)
        colliders.append(horizontal_rect)

    def render(self, screen):
        # отрисовка нашего игрового поля
        w = h = self.cell_size
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                x = self.left + self.cell_size * j
                y = self.top + self.cell_size * i

                if i > 1:
                    pygame.draw.rect(screen, '#808080',
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size, self.cell_size), 1)

                if elem:
                    color_index = elem - 1
                    pygame.draw.rect(screen, COLOR[color_index][0], (x, y, w, h), 0)
                    pygame.draw.rect(screen, COLOR[color_index][1], (x + 10, y + 10, w - 20, h - 20), 2)
                    pygame.draw.line(screen, COLOR[color_index][2], (x, y + h - 1), (x + w, y + h - 1), 2)
                    pygame.draw.line(screen, COLOR[color_index][2], (x + w - 1, y), (x + w - 1, y + h), 2)
                    pygame.draw.line(screen, COLOR[color_index][3], (x, y + 1), (x + w, y + 1), 2)
                    pygame.draw.line(screen, COLOR[color_index][3], (x + 1, y), (x + 1, y + h), 2)

                # 660 80
        font = pygame.font.SysFont(None, 32)
        img = font.render('SCORE:', 1, (255, 255, 255))
        img_score = font.render(f'{self.score}', 1, (255, 255, 255))

        screen.blit(img, (660, 80))
        screen.blit(img_score, (660, 110))

    def update(self, colliders):
        # функция для обновления списка коллайдеров
        self.create_borders(colliders)
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                # если элемент не пустой создаём коллайдер
                if bool(elem):
                    x = self.cell_size * j + self.left
                    y = self.cell_size * i + self.top
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    colliders.append(rect)

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

    def create_block(self, cell, color_index):
        # создаем блок на поле
        x = cell[0]
        y = cell[1]
        self.board[y][x] = color_index

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
            board = copy.deepcopy(self.board)
            for i in range(y[index], 0, -1):
                self.board[i] = board[i - 1]

    def add_points(self, count_lines):
        self.score += 1000 * count_lines

    def clear(self):
        self.board = [[0] * self.width for _ in range(self.height)]
