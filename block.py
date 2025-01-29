import copy

import pygame
import random
import numpy
from variables import COLOR, SHADOW_COLOR


class Block(pygame.sprite.Sprite):

    def __init__(self, all_group, cell_size, speed, color_index, sfx_volume):
        super().__init__(all_group)
        self.speed = speed
        self.tick = 0
        self.move_tick = 0
        self.is_ground = False
        self.ground_more_time = False  # переменная для увелечения времени на земле
        self.rects = []
        self.cords = []

        self.color_index = color_index
        self.main_color = COLOR[self.color_index][0]
        self.inside_color = COLOR[self.color_index][1]
        self.bottom_color = COLOR[self.color_index][2]
        self.top_color = COLOR[self.color_index][3]
        self.color_index += 1

        self.rect = pygame.Rect((100, 100, 100, 100))
        self.cell_size = cell_size
        self.sound_fall = pygame.mixer.Sound('data/sounds/fall_sound.mp3')
        self.sound_rotate = pygame.mixer.Sound('data/sounds/block_rotate.mp3')
        self.sfx_volume = sfx_volume

    def __repr__(self):
        return f'Block({self.cell_size} {self.speed} {self.color_index})'

    def update(self, board, fps, insta_fall=False):  # функция падения блока
        self.tick += self.speed / fps  # для не моментального падения считаем тики, speed падений блока в секунду
        if self.tick >= 1:
            if not self.is_ground:  # если блок ешё не упал
                self.rect.y += 40
                self.fill_rects(self.rects)
                block_cords = [board.get_cell(rect.center) for rect in self.rects]
                if not insta_fall:  # проверка что это не мгновенное падание звука (иначе звук накладывается)
                    self.sound_fall.set_volume(self.sfx_volume)
                    self.sound_fall.play()
                if check_collide(board.board, block_cords):
                    self.rect.y -= 40
                    self.fill_rects(self.rects)
                    self.is_ground = True
            self.tick = 0
        self.fill_rects(self.rects)

    def move_right(self, board, fps):  # движение блока вправо
        dx = 0
        self.move_tick += 10 / fps
        if self.move_tick > 1:
            self.move_tick = 0
            self.rect.x += self.cell_size
            self.fill_rects(self.rects)
            block_cords = [board.get_cell(rect.center) for rect in self.rects]
            if check_collide(board.board, block_cords) or self.is_ground:
                dx = 5
                self.rect.x -= self.cell_size
                self.fill_rects(self.rects)
        return dx

    def move_left(self, board, fps):  # движение блока влево
        dx = 0
        self.move_tick += 10 / fps
        if self.move_tick > 1:
            self.move_tick = 0
            self.rect.x -= self.cell_size
            self.fill_rects(self.rects)
            block_cords = [board.get_cell(rect.center) for rect in self.rects]
            if check_collide(board.board, block_cords) or self.is_ground:
                dx = -5
                self.rect.x += self.cell_size
                self.fill_rects(self.rects)
        return dx

    def instant_fall(self, board):  # мгновенное падение блока
        self.sound_fall.set_volume(0.3)  # ставим громкость звуку
        self.sound_fall.play()  # проигрываем звук
        speed = self.speed  # сохраняем скорость, чтобы потом вернуть
        self.speed = 100  # для мгновенного смены тика
        while not self.is_ground:  # бесконечный цикл пока мы не столкнёмся
            self.update(board, 1, insta_fall=True)
        self.speed = speed  # возвращаем скорость

    def rotation(self, board):  # поворачивает блок на 90 градусов
        if not self.is_ground:
            cords = numpy.array(self.cords)
            rotate_matrix = numpy.rot90(cords)
            self.cords = rotate_matrix
            self.fill_rects(self.rects)
            block_cords = [board.get_cell(rect.center) for rect in self.rects]
            if check_collide(board.board, block_cords):
                self.cords = cords
                self.fill_rects(self.rects)
            else:
                self.sound_fall.set_volume(self.sfx_volume)
                self.sound_fall.play()

    def draw(self, screen):  # рисует блок
        for rect in self.rects:
            x, y = rect.x, rect.y
            w, h = self.cell_size, self.cell_size
            pygame.draw.rect(screen, self.main_color, (x, y, w, h), 0)
            pygame.draw.rect(screen, self.inside_color, (x + 10, y + 10, w - 20, h - 20), 2)
            pygame.draw.line(screen, self.bottom_color, (x, y + h - 1), (x + w, y + h - 1), 2)
            pygame.draw.line(screen, self.bottom_color, (x + w - 1, y), (x + w - 1, y + h), 2)
            pygame.draw.line(screen, self.top_color, (x, y + 1), (x + w, y + 1), 2)
            pygame.draw.line(screen, self.top_color, (x + 1, y), (x + 1, y + h), 2)

    def shadow(self, screen, board):  # рисует тень блока(куда он падает)
        shadow_rects = copy.deepcopy(self.rects)
        block_cords = [board.get_cell(rect.center) for rect in shadow_rects]

        while not check_collide(board.board, block_cords):
            for rect in shadow_rects:
                rect.y += 40
            block_cords = [board.get_cell(rect.center) for rect in shadow_rects]
        for rect in shadow_rects:
            rect.y -= 40
        for rect in shadow_rects:
            pygame.draw.rect(screen, SHADOW_COLOR, rect, 3)

    def fill_rects(self, rects):  # обновляет (self.rects)
        rects.clear()
        x, y = self.rect.topleft
        for ky, cords in enumerate(self.cords):
            for kx, block in enumerate(cords):
                if block:
                    rects.append(
                        pygame.Rect(x + kx * self.cell_size, y + ky * self.cell_size, self.cell_size, self.cell_size)
                    )


def check_collide(board, block_cords):  # проверяет столкновения
    if not all(block_cords):
        return True
    # прибавляем 1 к оси x, чтобы проверить, что снизу блока находится
    for cords in block_cords:  # перебираем координаты
        if board[cords[1]][cords[0]]:  # если блок не пустой возвращаем TRUE столкновение
            return True
    return False
