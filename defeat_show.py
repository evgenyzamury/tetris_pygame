import pygame
from variables import WIDTH, HEIGHT
from gameplay_show import show_time


def show_defeat(screen, board, restart_button, exit_to_main_menu, start_time, end_time, pos):
    board.render(screen)  # показываем основное поле с блоками
    show_time(screen, end_time, start_time)  # показываем время игры
    restart_button.check_hover(pos)  # проверяем наводку курсора на кнопку
    restart_button.draw(screen)  # рисуем кнопку перезапуска на экране
    exit_to_main_menu.check_hover(pos)  # проверяем наводку курсора на кнопку
    exit_to_main_menu.draw(screen)  # рисуем кнопку выхода в главное меню на экране
    # создаём и рисуем надпись проигрыша
    font = pygame.font.SysFont(None, 100)
    img = font.render('You lose!', 1, (255, 255, 255), '#34495e')
    screen.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height()))
