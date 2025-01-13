import pygame
import random
import numpy
from variables import COLOR


class Block(pygame.sprite.Sprite):

    def __init__(self, cell_size):
        super().__init__()
        self.speed = 2
        self.tick = 0
        self.is_ground = False
        self.rects = []
        self.cords = []

        self.color_index = random.randint(0, 6)
        self.main_color = COLOR[self.color_index][0]
        self.inside_color = COLOR[self.color_index][1]
        self.bottom_color = COLOR[self.color_index][2]
        self.top_color = COLOR[self.color_index][3]
        self.color_index += 1

        self.rect = pygame.Rect((100, 100, 100, 100))
        self.cell_size = cell_size

    def update(self, h):
        self.tick += self.speed / 60
        if self.tick >= 1:
            if not self.is_ground:
                self.rect.y += 40
                self.fill_rects()
                if self.check_collide(h):
                    self.rect.y -= 0
                    self.is_ground = True
                else:
                    self.rect.y += self.cell_size
                self.rect.y -= 40
            else:
                self.kill()
            self.tick = 0
        self.fill_rects()

    def move_right(self, colliders):
        self.rect.x += self.cell_size
        self.fill_rects()
        if self.check_collide(colliders) or self.is_ground:
            self.rect.x -= self.cell_size
            self.fill_rects()

    def move_left(self, colliders):
        self.rect.x -= self.cell_size
        self.fill_rects()
        if self.check_collide(colliders) or self.is_ground:
            self.rect.x += self.cell_size
            self.fill_rects()

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
        self.fill_rects()
        if self.check_collide(colliders):
            self.cords = cords
            self.fill_rects()

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

    def check_collide(self, collider_list):
        for rect in self.rects:
            if rect.collidelist(collider_list) != -1:
                return True
        else:
            return False

    def fill_rects(self):
        self.rects = []
        x, y = self.rect.topleft
        for ky, cords in enumerate(self.cords):
            for kx, block in enumerate(cords):
                if block:
                    self.rects.append(
                        pygame.Rect(x + kx * self.cell_size, y + ky * self.cell_size, self.cell_size, self.cell_size)
                    )
