import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, cell_size):
        super().__init__()
        self.speed = 4
        self.tick = 0
        self.is_ground = False
        self.rects = []
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

    def move_right(self):
        self.rect.x += self.cell_size

    def move_left(self):
        self.rect.x -= self.cell_size

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
        pass
