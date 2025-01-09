import pygame
from board import Board
from block import Block

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

    cell_height = 19
    cell_width = 10
    vertical_borders = []
    horizontal_borders = []
    all_group = pygame.sprite.Group()

    left = (WIDTH - (cell_width * cell_size)) // 2
    top = (HEIGHT - (cell_height * cell_size)) // 2
    print(left, top)

    board.set_view(left, top, cell_size, vertical_borders, horizontal_borders)
    active_block = Block(all_group, left, top, cell_size)
    print(vertical_borders, horizontal_borders)

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_DOWN]:
                    active_block.speed = 20
                if event.key == pygame.K_RIGHT:
                    active_block.move_right()
                if event.key == pygame.K_LEFT:
                    active_block.move_left()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    active_block.speed = 4

        if active_block.is_ground:
            active_block = Block(all_group, left, top, cell_size)

        board.render(screen)
        all_group.draw(screen)
        all_group.update(vertical_borders, horizontal_borders)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
