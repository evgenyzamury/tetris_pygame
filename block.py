import pygame
import os
import sys

CELL_SIZE = 40


def load_image(name):
    fullname = os.path.join('image', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Block(pygame.sprite.Sprite):
    block_image = load_image('1.png')
    block_image = pygame.transform.scale(block_image, (CELL_SIZE * 3, CELL_SIZE * 2))

    def __init__(self, group, left, top, cell_size):
        super().__init__()
        self.speed = 4
        self.tick = 0
        self.is_ground = False
        self.image = Block.block_image
        # self.image = pygame.Surface((40, 40))
        # self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        self.rect.y = top
        self.rects = []
        self.cell_size = cell_size
        self.fill_rects()
        print(self.rects)

    def fill_rects(self):
        self.rects = []
        x, y = self.rect.topleft
        self.rects.append(pygame.Rect(x + 40, y, 40, 40))
        self.rects.append(pygame.Rect(x + 80, y, 40, 40))
        self.rects.append(pygame.Rect(x, y + 40, 40, 40))
        self.rects.append(pygame.Rect(x + 40, y + 40, 40, 40))

    def update(self, v, h):
        self.tick += self.speed / 60
        if self.tick >= 1:
            if not self.is_ground:
                self.rect.y += 1
                self.fill_rects()
                if self.check_collide(h):
                    self.rect.y -= 0
                    self.is_ground = True
                else:
                    self.rect.y += self.cell_size
                self.rect.y -= 1
            else:
                self.kill()
            self.tick = 0
        self.fill_rects()

    def check_collide(self, collider_list):
        for rect in self.rects:
            if rect.collidelist(collider_list) != -1:
                return True
        else:
            return False

    def move_right(self):
        self.rect.x += self.cell_size

    def move_left(self):
        self.rect.x -= self.cell_size

    def draw(self, screen):
        x, y = self.rect.topleft
        pygame.draw.rect(screen, (255, 255, 255), self.rects[0], 5)
        pygame.draw.rect(screen, (255, 255, 255), self.rects[1], 5)
        pygame.draw.rect(screen, (255, 255, 255), self.rects[2], 5)
        pygame.draw.rect(screen, (255, 255, 255), self.rects[3], 5)
