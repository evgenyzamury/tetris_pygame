import sys

import pygame

from variables import HEIGHT, WIDTH
from database import get_statistic
from button import Button
from ui_menu import MenuUI


def ui_show_statistic(screen):
    menu_ui = MenuUI(WIDTH, HEIGHT, theme=0)
    running = True

    # Получаем статистику из базы данных
    best_score, all_score, play_time = get_statistic()

    # Устанавливаем шрифт
    font = pygame.font.SysFont(None, 40)

    # Рендерим текст статистики
    img_best_score = font.render('Best score', 1, '#03dac6', (0, 0, 0))
    img_best_score_amount = font.render(str(best_score), 1, '#03dac6')
    img_all_score = font.render('All score', 1, '#03dac6', (0, 0, 0))
    img_all_score_amount = font.render(str(all_score), 1, '#03dac6')
    img_play_time = font.render('Play time (min)', 1, '#03dac6', (0, 0, 0))
    img_play_time_amount = font.render(str(play_time), 1, '#03dac6')

    # Отрисовка статистики
    screen.blit(img_best_score, (40, HEIGHT // 2 - (img_best_score.get_height() * 2)))
    screen.blit(img_best_score_amount,
                (40 - img_best_score_amount.get_width() + img_best_score.get_width() // 2, HEIGHT // 2))
    screen.blit(img_all_score,
                (WIDTH // 2 - img_all_score.get_width() // 2, HEIGHT // 2 - (img_all_score.get_height() * 2)))
    screen.blit(img_all_score_amount,
                ((WIDTH // 2 - img_all_score_amount.get_width() // 2), HEIGHT // 2))
    screen.blit(img_play_time,
                (WIDTH - 40 - img_play_time.get_width(), HEIGHT // 2 - img_play_time_amount.get_height() * 2))
    screen.blit(img_play_time_amount,
                (WIDTH - 40 - img_play_time.get_width() // 2, HEIGHT // 2))

    # Создаем кнопку "Назад"
    back_button = Button(10, 10, 100, 40, 'Back', (255, 255, 255),
                         hover_color='gray', text_size=30, theme=0)

    back_button.draw(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                back_button.check_hover(event.pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    menu_ui.render(screen)
                    running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu_ui.render(screen)
                running = False

        back_button.draw(screen)
        pygame.display.update()
