import copy
import pygame
import random


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 20
        self.top = 20
        self.cell_size = 60
        self.step = 0
        self.first_step = True
        self.color_step = None

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                x = self.left + self.cell_size * j
                y = self.top + self.cell_size * i
                if elem == 0:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                elif elem == 1:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size, self.cell_size), 0)

                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        x -= self.left
        y -= self.top
        x //= self.cell_size
        y //= self.cell_size
        if (x >= 0 and y >= 0) and (
                x < self.width and y < self.height):
            return x, y
        return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell):
        if cell:
            x, y = cell
            self.board[y][x] = 1


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.red = False
        self.red_cords = None
        self.amount_blue = 0
        self.board = [[1000] * width for _ in range(height)]
        self.need_go = False

    def render(self, screen):
        self.amount_blue = 0
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                x = self.left + self.cell_size * j
                y = self.top + self.cell_size * i
                if elem == 1000:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                      self.cell_size, self.cell_size), 0)
                elif elem == 2000:
                    pygame.draw.circle(screen, (0, 0, 255),
                                       (x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2 - 1, 0)
                    self.amount_blue += 1

                elif elem == 100:
                    pygame.draw.circle(screen, (255, 0, 0),
                                       (x + self.cell_size // 2, y + self.cell_size // 2), self.cell_size // 2 - 1, 0)
                # else: # стоимость пути
                #     font = pygame.font.Font(None, 50)
                #     img = font.render(f'{elem - 2}', False, (0, 255, 0))
                #     screen.blit(img, (x, y))

                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def on_click(self, cell):
        if cell:
            x, y = cell
            if self.board[y][x] == 1000:
                print('ok', self.red)
                if self.red:
                    if self.has_path(x, y, self.red_cords[0], self.red_cords[1]):
                        self.need_go = True
                    else:
                        self.clear_price()

                else:
                    self.board[y][x] = 2000
            elif self.board[y][x] == 2000 and not self.red:
                self.board[y][x] = 100
                self.red = True
                self.red_cords = (x, y)

            elif self.board[y][x] == 100:
                print('ok')
                self.board[y][x] = 2000
                self.red = False

    def go(self):
        if self.need_go:
            xx, yy = self.red_cords
            min = 1000
            cord = (xx, yy)
            if xx + 1 < self.width and self.board[yy][xx + 1] < min:
                min = self.board[yy][xx + 1]
                cord = (xx + 1, yy)
            if xx - 1 >= 0 and self.board[yy][xx - 1] < min:
                min = self.board[yy][xx - 1]
                cord = (xx - 1, yy)
            if yy + 1 < self.height and self.board[yy + 1][xx] < min:
                min = self.board[yy + 1][xx]
                cord = (xx, yy + 1)
            if yy - 1 >= 0 and self.board[yy - 1][xx] < min:
                min = self.board[yy - 1][xx]
                cord = (xx, yy - 1)
            self.red_cords = cord
            self.board[cord[1]][cord[0]] = 100
            self.board[yy][xx] = 1000
            if min == 2:
                self.need_go = False
                self.clear_price()

    def clear_price(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] < 100:
                    self.board[y][x] = 1000

    def has_path(self, x1, y1, x2, y2):
        points = [(x1, y1)]
        weight = 0
        points_with_weight = [((x1, y1), weight)]
        points_copy = copy.deepcopy(points)
        tmp_board = copy.deepcopy(self.board)
        need_find = (x2, y2)
        adfa = 0
        while need_find not in points:
            points_copy = copy.deepcopy(points)
            weight += 1
            for cords in points_copy:
                x, y = (cords[0], cords[1])

                if x + 1 < self.width and (x + 1, y) not in points and tmp_board[y][x + 1] != 2000:
                    points.append((x + 1, y))
                    points_with_weight.append(((x + 1, y), weight))

                if x - 1 >= 0 and (x - 1, y) not in points and tmp_board[y][x - 1] != 2000:
                    points.append((x - 1, y))
                    points_with_weight.append(((x - 1, y), weight))

                if y + 1 < self.height and (x, y + 1) not in points and tmp_board[y + 1][x] != 2000:
                    points.append((x, y + 1))
                    points_with_weight.append(((x, y + 1), weight))

                if y - 1 >= 0 and (x, y - 1) not in points and tmp_board[y - 1][x] != 2000:
                    points.append((x, y - 1))
                    points_with_weight.append(((x, y - 1), weight))

            if points == points_copy:
                break
        self.show_path(points_with_weight)
        return need_find in points

    def show_path(self, points):
        for point in points:
            x, y = point[0]
            weight = point[1] + 2
            self.board[y][x] = weight


if __name__ == '__main__':
    a = 30
    size = width, height = 700, 700
    pygame.init()
    screen = pygame.display.set_mode(size)
    line = Lines(10, 10)
    running = True
    clock = pygame.time.Clock()
    speed = 5
    start_game = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not start_game:
                line.get_click(event.pos)
        screen.fill((0, 0, 0))
        line.go()
        line.render(screen)
        clock.tick(speed)
        pygame.display.flip()
