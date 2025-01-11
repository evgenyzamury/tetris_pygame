import pygame
import numpy


class Block(pygame.sprite.Sprite):
    def __init__(self, cell_size):
        super().__init__()
        self.speed = 4
        self.tick = 0
        self.is_ground = False
        self.rects = []
        self.cords = []
        self.rect = None
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
        if self.check_collide(colliders):
            self.rect.x -= self.cell_size
            self.fill_rects()

    def move_left(self, colliders):
        self.rect.x -= self.cell_size
        self.fill_rects()
        if self.check_collide(colliders):
            self.rect.x += self.cell_size
            self.fill_rects()

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
            pygame.draw.rect(screen, (255, 255, 255), rect, 5)

    def check_collide(self, collider_list):
        for rect in self.rects:
            if rect.collidelist(collider_list) != -1:
                return True
        else:
            return False

    def fill_rects(self):
        self.rects = []
        x, y = self.rect.topleft
        x, y = x + 5, y + 5
        for ky, cords in enumerate(self.cords):
            for kx, block in enumerate(cords):
                if block:
                    self.rects.append(pygame.Rect(x + kx * self.cell_size, y + ky * self.cell_size, 30, 30))
