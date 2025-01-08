import pygame
from board import Board

SIZE = WIDTH, HEIGHT = 800, 800
FPS = 60

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('shablon')

    clock = pygame.time.Clock()
    running = True

    board = Board(10, 19)
    cell_size = 40
    left = (WIDTH - 10 * cell_size) // 2
    top = (HEIGHT - 19 * cell_size) // 2
    board.set_view(left, top, cell_size)

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        board.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
