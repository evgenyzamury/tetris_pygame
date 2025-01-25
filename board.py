import copy
import random

import pygame
from pprint import pprint
from variables import COLOR, WIDTH, HEIGHT

screen_rect = (0, 0, WIDTH, HEIGHT)


class Board(pygame.sprite.Sprite):
    # создание поля
    def __init__(self, all_group, width, height):
        super().__init__(all_group)
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 20
        self.top = 20
        self.cell_size = 40
        self.step = 0
        self.first_step = True
        self.color_step = None
        self.surface = pygame.Surface((width * self.cell_size, height * self.cell_size))
        self.rect = self.surface.get_rect(topleft=(self.left, self.top))

    def set_view(self, left, top, cell_size, colliders, vertical_borders):  # настройка внешнего вида
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.create_borders(colliders, vertical_borders)
        self.surface = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))
        self.rect = self.surface.get_rect(topleft=(self.left, self.top))

    def create_borders(self, colliders, vertical_borders):
        # делаем стенки нашего поля, левое - правое - нижнее
        x1, y1 = self.rect.x, self.rect.y
        x2, y2 = x1 + (self.width * self.cell_size), y1 + (self.height * self.cell_size)
        # создание боковых границ
        left_rect = pygame.Rect(x1 - 50, y1 - 100, 50, self.cell_size * self.height + 100)
        right_rect = pygame.Rect(x2, y1 - 100, 50, self.cell_size * self.height + 100)
        # создадим rect для нижней границы
        horizontal_rect = pygame.Rect(x1, y2, self.width * self.cell_size, 40)
        colliders.append(left_rect)
        colliders.append(right_rect)
        colliders.append(horizontal_rect)
        vertical_borders.append(left_rect)
        vertical_borders.append(right_rect)

    def render(self, screen):
        # отрисовка нашего игрового поля
        w = h = self.cell_size
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                x = self.rect.x + self.cell_size * j
                y = self.rect.y + self.cell_size * i

                if i > 1:
                    pygame.draw.rect(screen, '#808080',
                                     (x, y, self.cell_size, self.cell_size), 1)

                if elem:
                    color_index = elem - 1
                    pygame.draw.rect(screen, COLOR[color_index][0], (x, y, w, h), 0)
                    pygame.draw.rect(screen, COLOR[color_index][1], (x + 10, y + 10, w - 20, h - 20), 2)
                    pygame.draw.line(screen, COLOR[color_index][2], (x, y + h - 1), (x + w, y + h - 1), 2)
                    pygame.draw.line(screen, COLOR[color_index][2], (x + w - 1, y), (x + w - 1, y + h), 2)
                    pygame.draw.line(screen, COLOR[color_index][3], (x, y + 1), (x + w, y + 1), 2)
                    pygame.draw.line(screen, COLOR[color_index][3], (x + 1, y), (x + 1, y + h), 2)

    def update(self, colliders, vertical_borders):
        # функция для обновления списка коллайдеров
        self.create_borders(colliders, vertical_borders)
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                # если элемент не пустой создаём коллайдер
                if bool(elem):
                    x = self.cell_size * j + self.rect.x
                    y = self.cell_size * i + self.rect.y
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    colliders.append(rect)

    def get_cell(self, pos):
        # узнаем клетку поля по координатам окна
        x, y = pos
        x -= self.rect.x
        y -= self.rect.y
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

    def check_fill_line(self, particles_group):
        count_lines = 0
        # создаём список координат оси y, чтобы отследить где заполнились линии
        need_y = []
        for y, line in enumerate(self.board):
            if all(line):
                count_lines += 1
                self.effect_fill_line(y, particles_group)
                self.board[y] = [0 for _ in range(self.width)]  # убираем блоки с заполненной линии
                need_y.append(y)
        else:
            # если есть хоть 1 заполненная линия роняем блоки
            if count_lines:
                self.fall_block_after_fill_lines(need_y, count_lines)
            return count_lines

    def effect_fill_line(self, y, particles_group):
        for x in range(len(self.board[y])):
            self.broken_block(x, y, particles_group)

    def broken_block(self, x, y, particles_group):
        amount_particles = 7
        left, top = self.rect.x, self.rect.y
        xx = left + self.cell_size * x
        yy = top + self.cell_size * y
        for i in range(amount_particles):
            for j in range(amount_particles):
                Particle(particles_group, xx + self.cell_size // amount_particles * i,
                         yy + self.cell_size // amount_particles * j, 5,
                         COLOR[self.board[y][x] - 1][0])

    def fall_block_after_fill_lines(self, y, count):
        # роняем блоки при заполнении линий
        for index in range(count):
            board = copy.deepcopy(self.board)
            for i in range(y[index], 0, -1):
                self.board[i] = board[i - 1]

    def clear(self):
        self.board = [[0] * self.width for _ in range(self.height)]

    def clear_destroy(self, particles_group):
        for y in range(self.height):
            for x in range(self.width):
                print(x, y)
                if self.board[y][x]:
                    self.broken_block(x, y, particles_group)
                    self.board[y][x] = 0


class Particle(pygame.sprite.Sprite):
    def __init__(self, particles_group, x, y, size, color):
        super().__init__(particles_group)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = [random.randint(-3, 3), random.randint(-3, 4)]
        self.gravity = 0.15
        self.tick = 0

    def update(self, fps):
        self.tick += 60 / fps
        if self.tick >= 1:
            # применяем гравитационный эффект:
            # движение с ускорением под действием гравитации
            self.velocity[1] += self.gravity
            # перемещаем частицу
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            # убиваем, если частица ушла за экран
            if not self.rect.colliderect(screen_rect):
                self.kill()
            self.tick = 0
