import sqlite3
import pygame
from variables import WIDTH, HEIGHT


def main_menu(screen, start_button, stats_button, pos):
    start_button.check_hover(pos)
    start_button.draw(screen)
    stats_button.check_hover(pos)
    stats_button.draw(screen)


def show_statistics(screen, exit_to_main_menu, pos):
    con = sqlite3.connect('data/tetris.db')
    cur = con.cursor()
    query = """SELECT * FROM stats INNER JOIN players on players.id = stats.player_id
                WHERE player = (SELECT player FROM players WHERE active_player = 1)"""
    result = cur.execute(query).fetchone()
    con.close()
    exit_to_main_menu.check_hover(pos, (WIDTH * 0.05, HEIGHT * 0.05))
    exit_to_main_menu.draw(screen, (WIDTH * 0.05, HEIGHT * 0.05))
    font = pygame.font.SysFont(None, 40)
    img_best_score = font.render('Best score', 1, '#03dac6', (0, 0, 0))
    img_best_score_amount = font.render(str(result[1]), 1, '#03dac6')
    img_all_score = font.render('All score', 1, '#03dac6', (0, 0, 0))
    img_all_score_amount = font.render(str(result[2]), 1, '#03dac6')
    img_play_time = font.render('Play time (min)', 1, '#03dac6', (0, 0, 0))
    img_play_time_amount = font.render(str(result[3] // 60), 1, '#03dac6')

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
