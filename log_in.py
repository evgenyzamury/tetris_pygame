import pygame
import sys
from database import get_players_name, create_player, change_player
from button import Button
from variables import translations


def show_log_in(screen, theme, language):
    signals = []
    bg_color = 'Black' if theme else 'White'
    color_text = (255, 255, 255) if theme else (0, 0, 0)
    running = True
    input_box = InputBox(theme, 120, 10)

    back_button = Button(10, 10, 100, 40, translations[language]['Back'], bg_color,
                         hover_color='gray', text_size=30, theme=theme)

    font = pygame.font.Font(None, 30)
    players_in_system_text_surface = font.render(f'--{translations[language]['Players in system']}:', True, color_text)

    players_in_system = get_players_name()
    players_text_surface_list = []
    for player in players_in_system:
        players_text_surface_list.append(font.render(player, True, color_text))

    while running:
        screen.fill(bg_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                back_button.check_hover(event.pos)
            elif event.type == pygame.USEREVENT:
                if event.button == back_button:
                    running = False
            signal, name = input_box.handle_event(event, players_in_system)
            if signal:
                signals.append(signal)
            back_button.handle_event(event)
            if signal == 'create':
                players_text_surface_list.append(font.render(name, True, color_text))
        x, y = 50, 150
        screen.blit(players_in_system_text_surface, (x, y))
        for player in players_text_surface_list:  # отображаем всех игроков которые есть в бд
            y += 50
            screen.blit(player, (x, y))

        input_box.draw(screen)

        back_button.draw(screen)
        pygame.display.flip()
    return signals[-1] if signals else None


class InputBox:
    def __init__(self, theme, x, y):
        self.rect = pygame.Rect(x, y, 300, 50)
        self.color = '#574547' if theme else "gray"
        self.active_color = '#241e22' if theme else "black"
        self.not_active_color = '#574547' if theme else "gray"
        self.text = ''
        self.font = pygame.font.Font(None, 50)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event, players):
        signal = None
        name = ''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.active_color if self.active else self.not_active_color
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:  # отслеживаем нажатие клавишы enter
                if self.text not in players:
                    create_player(self.text)
                    players.append(self.text)
                    signal = 'create'
                    name = self.text
                else:
                    change_player(self.text)
                    signal = 'change'
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1:]
            else:
                self.text += event.unicode  # добавляем в текст нажатый символ
            self.txt_surface = self.font.render(self.text, True, self.color)
        return signal, name

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2 + int(self.active))
