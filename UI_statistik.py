import pygame
from variables import HEIGHT, WIDTH
from database import get_statistic

best_score, all_score, play_time = get_statistic()  # получаем статистику из базы данных


def ui_show_statistic(screen):  # рисуем статистику на экране
    font = pygame.font.SysFont(None, 40)
    img_best_score = font.render('Best score', 1, '#03dac6', (0, 0, 0))
    img_best_score_amount = font.render(str(best_score), 1, '#03dac6')
    img_all_score = font.render('All score', 1, '#03dac6', (0, 0, 0))
    img_all_score_amount = font.render(str(all_score), 1, '#03dac6')
    img_play_time = font.render('Play time (min)', 1, '#03dac6', (0, 0, 0))
    img_play_time_amount = font.render(str(play_time), 1, '#03dac6')

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
