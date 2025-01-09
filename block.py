import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, group, left, top, cell_size):
        super().__init__(group)
        self.speed = 4
        self.tick = 0
        self.is_ground = False
        self.image = pygame.Surface((40, 40))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.x = left + cell_size * 4
        print(top)
        self.rect.y = top
        self.cell_size = cell_size
        print(self.rect.x, self.rect.y)

    def update(self, v, h):
        self.tick += self.speed / 60
        if self.tick >= 1:
            if not self.is_ground:
                self.rect.y += 1
                if self.rect.collidelist(h) == 0:
                    self.rect.y -= 0
                    self.is_ground = True
                else:
                    self.rect.y += self.cell_size
                self.rect.y -= 1
            self.tick = 0

    def move_right(self):
        self.rect.x += self.cell_size

    def move_left(self):
        self.rect.x -= self.cell_size
