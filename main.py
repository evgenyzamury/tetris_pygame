import random
import pygame
from blocks import *
from board import Board
from Button import ColorButton
from ui_in_game import InGameUI
from ui_menu import MenuUI
from settings_ui import SettingsUI
from UI_statistik import ui_show_statistic

SIZE = WIDTH, HEIGHT = 800, 900
FPS = 60

BLOCKS = [ZBlock, SBlock, IBlock, LBlock, TBlock, JBlock, OBlock]

score = 0
level = 1

is_paused = False


def gameplay():
    board.render(screen)
    block.update(colliders)
    block.shadow(screen, colliders)
    block.draw(screen)
    in_game_ui.render(screen)

    show_next_block()
    all_group.update(colliders)


def main_menu():
    start_button.check_hover(pos)
    start_button.draw(screen)
    menu_ui.render(screen)


def spawn_new_block(block=None, spawn_block_list=None):
    defeat = False
    # если у нас есть блок, то оставим его снизу
    if block:
        # переберём все ректы и поставим их в сетке
        color_index = spawn_block_list[0][1] + 1
        spawn_block_list = spawn_block_list[1::]
        spawn_block_list.append((random.randint(0, 6), random.randint(0, 6)))
        for rect in block.rects:
            x, y = rect.center
            cell = board.get_cell((x, y))
            board.create_block(cell, color_index)
            if cell[1] < 2:  # проверяем есть ли блок выше игрового поля
                defeat = True
                # если да, мы проиграли
        if defeat:
            return False, spawn_block_list
    block_index = spawn_block_list[0][0]  # определяем какой блок заспавниться
    color_index = spawn_block_list[0][1]  # определяем цвет блока
    block = BLOCKS[block_index](left, top, cell_size, speed, color_index)
    return block, spawn_block_list


def show_next_block():  # показывает следующий блок который заспавнится
    x, y = 670, 250
    font = pygame.font.SysFont(None, 30)
    img_text = font.render('Next: ', 1, (255, 255, 255))
    screen.blit(img_text, (x, y))
    block_index = spawn_block_list[1][0]
    color_index = spawn_block_list[1][1]
    show_block = BLOCKS[block_index](x - 70, y + 50, 20, 0, color_index)
    show_block.draw(screen)


def get_button_action(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                return button.text
    return None


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('tetris')
    settings_ui = SettingsUI(800, 600)

    clock = pygame.time.Clock()
    running = True

    defeat = False
    tetris_game_running = False
    start_menu = True
    show_statistic = False

    board = Board(10, 21)
    cell_size = 40
    cell_height = 21
    cell_width = 10
    colliders = []
    all_group = pygame.sprite.Group()
    left = (WIDTH - (cell_width * cell_size)) // 2
    top = (HEIGHT - (cell_height * cell_size)) // 2 - 30
    board.set_view(left, top, cell_size, colliders)

    speed = 2
    spawn_block_list = [(random.randint(0, 6), random.randint(0, 6)), (random.randint(0, 6), random.randint(0, 6))]
    block, spawn_block_list = spawn_new_block(spawn_block_list=spawn_block_list)

    width = 260
    height = 80
    start_button = ColorButton(WIDTH // 2 - width // 2, (HEIGHT // 2 - height // 2) - 200, width, height,
                               'TETRIS GAME', 'black', hover_color='gray', text_size=40)
    pause_button = ColorButton(WIDTH - 770, 20, 80, 40, 'Pause', 'black', hover_color='gray', text_size=30)

    pos = 0, 0

    menu_ui = MenuUI(WIDTH, HEIGHT)
    in_game_ui = InGameUI(WIDTH, HEIGHT)

    back_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 - 95, 200, 50, 'Back to Menu', 'black', hover_color='gray',
                              text_size=30)
    continue_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, 'Continue', 'black', hover_color='gray',
                                  text_size=30)
    settings_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, 'Settings', 'black', hover_color='gray',
                                  text_size=30)
    results_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 + 45, 200, 50, 'Results', 'black', hover_color='gray',
                                 text_size=30)
    quit_button = ColorButton(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, 'Quit', 'black', hover_color='gray',
                              text_size=30)

    while running:
        board.update(colliders)
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if tetris_game_running and event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_DOWN]:
                    block.speed = 20
                if event.key == pygame.K_RIGHT:
                    block.move_right(colliders)
                if event.key == pygame.K_LEFT:
                    block.move_left(colliders)
                if event.key == pygame.K_UP:
                    block.rotation(colliders)
                if event.key == pygame.K_SPACE:
                    block.instant_fall(colliders)
                if event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused
            elif tetris_game_running and event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    block.speed = speed

            if event.type == pygame.MOUSEMOTION:
                pause_button.handle_event(event)
                continue_button.handle_event(event)
                settings_button.handle_event(event)
                quit_button.handle_event(event)
                pos = event.pos

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.rect.collidepoint(event.pos):
                    is_paused = not is_paused

                # Логика для главного меню
                if start_menu:
                    action = menu_ui.get_button_action(event)
                    if action == 'Continue' and start_menu:
                        start_menu = False
                        tetris_game_running = True
                    elif action == 'Settings':
                        settings_open = True
                        while settings_open:
                            screen.fill((0, 0, 0))
                            settings_ui.render(screen)
                            pygame.display.flip()
                            for settings_event in pygame.event.get():
                                if settings_event.type == pygame.QUIT:
                                    running = False
                                    exit()
                                if settings_event.type == pygame.KEYDOWN and settings_event.key == pygame.K_ESCAPE:
                                    settings_open = False
                                settings_action = settings_ui.handle_event(settings_event)
                                if settings_action == "back":
                                    settings_open = False

                    elif action == 'Quit' and start_menu:
                        running = False

                    elif action == "Save and Exit":
                        running = False

                # Логика паузы
                if is_paused:
                    if continue_button.rect.collidepoint(event.pos):
                        is_paused = False
                    elif back_button.rect.collidepoint(event.pos):
                        tetris_game_running = False
                        is_paused = False
                        start_menu = True
                    elif settings_button.rect.collidepoint(event.pos):
                        settings_open = True
                        while settings_open:
                            screen.fill((0, 0, 0))
                            settings_ui.render(screen)
                            pygame.display.flip()
                            for settings_event in pygame.event.get():
                                if settings_event.type == pygame.QUIT:
                                    running = False
                                    exit()
                                if settings_event.type == pygame.KEYDOWN and settings_event.key == pygame.K_ESCAPE:
                                    settings_open = False
                                settings_action = settings_ui.handle_event(settings_event)
                                if settings_action == "back":
                                    settings_open = False

                    elif quit_button.rect.collidepoint(event.pos):
                        running = False

                # Проверка кнопки старта в главном меню
                elif event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(event.pos):
                    start_menu = False
                    tetris_game_running = True

        if tetris_game_running:
            if is_paused:
                # Меню паузы
                back_button.draw(screen)
                continue_button.draw(screen)
                settings_button.draw(screen)
                results_button.draw(screen)
                quit_button.draw(screen)
            else:
                pause_button.draw(screen)
                gameplay()

        if tetris_game_running and block.is_ground:
            block, spawn_block_list = spawn_new_block(block, spawn_block_list=spawn_block_list)
            if block:
                lines_filled = board.check_fill_line()
                if lines_filled > 0:
                    score += lines_filled * 100
                if score >= level * 1000:
                    level += 1
            else:
                defeat = True
                tetris_game_running = False

        if start_menu:
            main_menu()
            menu_ui.handle_event(event)

        if tetris_game_running:
            font = pygame.font.SysFont(None, 30)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            level_text = font.render(f"Level: {level}", True, (255, 255, 255))
            screen.blit(level_text, (620, 20))
            screen.blit(score_text, (620, 70))

        if defeat:
            board.render(screen)
            font = pygame.font.SysFont(None, 100)
            img = font.render("YOU LOSE!", 1, (255, 255, 255), (0, 0, 0))
            screen.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height()))

        colliders.clear()
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
