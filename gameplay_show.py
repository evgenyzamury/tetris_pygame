import pygame


def show_next_block(screen, spawn_block_list, BLOCKS):
    font = pygame.font.SysFont(None, 30)
    img_text = font.render('Next: ', 1, (255, 255, 255))
    screen.blit(img_text, (670, 250))
    block_index = spawn_block_list[1][0]
    color_index = spawn_block_list[1][1]
    show_block = BLOCKS[block_index]( 600, 300, 20, 0, color_index)
    show_block.draw(screen)


def show_time(screen, ticks, start_time):
    font = pygame.font.SysFont(None, 30)
    time = (ticks - start_time) // 1000
    time = f'{time // 60:02d}:' + f'{time % 60:02d}'
    img_time = font.render(time, 1, (255, 255, 255))
    img_time_text = font.render('Time', 1, (255, 255, 255))

    screen.blit(img_time_text, (660, 140))
    screen.blit(img_time, (670 + img_time_text.get_width(), 140))


def gameplay(screen, board, block, colliders, spawn_new_block_list, start_time, BLOCKS):
    board.render(screen)  # рисуем поле тетриса
    block.update(colliders)  # обновляем блок, проверяем на падение
    block.shadow(screen, colliders)  # находим и рисуем тень активного блока(подсказка куда он падает)
    block.draw(screen)  # рисуем активный блок
    show_next_block(screen, spawn_new_block_list, BLOCKS)  # показываем следующий блок который появиться активным
    show_time(screen, pygame.time.get_ticks(), start_time)
