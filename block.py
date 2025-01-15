import copy

import pygame
import random
import numpy
from variables import COLOR, SHADOW_COLOR


class Block(pygame.sprite.Sprite):

    def __init__(self, all_group, cell_size, speed, color_index):
        super().__init__(all_group)
        self.speed = speed
        self.tick = 0
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

    def update(self, colliders):
        self.tick += self.speed / 60
        if self.tick >= 1:
            if not self.is_ground:
                self.rect.y += 40
                self.fill_rects(self.rects)
                if check_collide(self.rects, colliders):
                    if self.ground_more_time:
                        self.is_ground = True
                    else:
                        self.ground_more_time = True
                else:
                    self.rect.y += self.cell_size
                self.rect.y -= 40
            else:
                self.kill()
            self.tick = 0
        self.fill_rects(self.rects)

    def move_right(self, colliders):
        self.rect.x += self.cell_size
        self.fill_rects(self.rects)
        if check_collide(self.rects, colliders) or self.is_ground:
            self.rect.x -= self.cell_size
            self.fill_rects(self.rects)

    def move_left(self, colliders):
        self.rect.x -= self.cell_size
        self.fill_rects(self.rects)
        if check_collide(self.rects, colliders) or self.is_ground:
            self.rect.x += self.cell_size
            self.fill_rects(self.rects)

    def instant_fall(self, horizontal_colliders):
        speed = self.speed
        self.speed = 100
        while not self.is_ground:
            self.update(horizontal_colliders)
        self.speed = speed

    def rotation(self, colliders):
        cords = numpy.array(self.cords)
        rotate_matrix = numpy.rot90(cords)
        self.cords = rotate_matrix
        self.fill_rects(self.rects)
        if check_collide(self.rects, colliders):
            self.cords = cords
            self.fill_rects(self.rects)

    def draw(self, screen):
        for rect in self.rects:
            x, y = rect.x, rect.y
            w, h = rect.width, rect.height
            pygame.draw.rect(screen, self.main_color, (x, y, w, h), 0)
            pygame.draw.rect(screen, self.inside_color, (x + 10, y + 10, w - 20, h - 20), 2)
            pygame.draw.line(screen, self.bottom_color, (x, y + h - 1), (x + w, y + h - 1), 2)
            pygame.draw.line(screen, self.bottom_color, (x + w - 1, y), (x + w - 1, y + h), 2)
            pygame.draw.line(screen, self.top_color, (x, y + 1), (x + w, y + 1), 2)
            pygame.draw.line(screen, self.top_color, (x + 1, y), (x + 1, y + h), 2)

    def shadow(self, screen, colliders):
        shadow_rects = copy.deepcopy(self.rects)
        while not check_collide(shadow_rects, colliders):
            for rect in shadow_rects:
                rect.y += 40
        for rect in shadow_rects:
            rect.y -= 40
        for rect in shadow_rects:
            pygame.draw.rect(screen, SHADOW_COLOR, rect, 3)

    def fill_rects(self, rects):
        rects.clear()
        x, y = self.rect.topleft
        for ky, cords in enumerate(self.cords):
            for kx, block in enumerate(cords):
                if block:
                    rects.append(
                        pygame.Rect(x + kx * self.cell_size, y + ky * self.cell_size, self.cell_size, self.cell_size)
                    )


def check_collide(rects, collider_list):
    for rect in rects:
        if rect.collidelist(collider_list) != -1:
            return True
    else:
        return False
