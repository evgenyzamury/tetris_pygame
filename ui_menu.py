import pygame

from button import Button
from variables import translations


class MenuUI:
    def __init__(self, width, height, theme, language='en'):
        self.width = width
        self.height = height
        self.language = language

        self.continue_button = Button
        self.settings_button = Button
        self.results_button = Button
        self.save_exit_button = Button

        self.buttons = []
        self.theme = theme
        self.init_button()

        self.decoration_white_theme_1 = pygame.image.load('data/image/tetris (3).png')
        self.decoration_white_theme_2 = pygame.image.load('data/image/tetris (1).png')
        self.decoration_white_theme_qr_code = pygame.image.load('data/image/qr_code.jpg')

        self.decoration_dark_theme_1 = pygame.image.load('data/image/dark_theme_tetris (3).png')
        self.decoration_dark_theme_2 = pygame.image.load('data/image/dark_theme_tetris (1).png')
        self.decoration_dark_theme_qr_code = pygame.image.load('data/image/dark_theme_qr_code.jpg')

    def render(self, screen):
        for button in self.buttons:
            button.draw(screen)

        if self.theme == 0:
            scaled_img = pygame.transform.scale(self.decoration_white_theme_qr_code, (200, 200))
            screen.blit(scaled_img, (10, 680))

            scaled_img = pygame.transform.scale(self.decoration_white_theme_2, (60, 60))
            screen.blit(scaled_img, (10, 10))

            scaled_img = pygame.transform.scale(self.decoration_white_theme_1, (60, 60))
            screen.blit(scaled_img, (710, 800))
        else:
            scaled_img = pygame.transform.scale(self.decoration_dark_theme_qr_code, (200, 200))
            screen.blit(scaled_img, (10, 680))

            scaled_img = pygame.transform.scale(self.decoration_dark_theme_2, (60, 60))
            screen.blit(scaled_img, (10, 10))

            scaled_img = pygame.transform.scale(self.decoration_dark_theme_1, (60, 60))
            screen.blit(scaled_img, (710, 800))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)

    def get_button_action(self, event):
        # если произошло нажатие
        if event.type == pygame.MOUSEBUTTONDOWN:
            # перебираем кнопки
            for button in self.buttons:
                # ищём кнопку на которую навились мышкой
                if button.hover:
                    # возвращаем кнопку
                    return button
        return None

    def init_button(self):
        button_width = 200
        button_height = 60
        spacing = 20
        center_x = self.width // 2 - button_width // 2
        start_y = self.height // 2 - (2 * button_height + 1.5 * spacing)

        self.log_in_button = Button(center_x, start_y + 1, button_width, button_height,
                                    translations[self.language]['Log in'],
                                    ((0, 0, 0) if self.theme else (255, 255, 255)),
                                    hover_color='gray', text_size=30, theme=self.theme)

        self.continue_button = Button(center_x, start_y + 1 * (button_height + spacing), button_width,
                                      button_height,
                                      translations[self.language]['Start Game'],
                                      ((0, 0, 0) if self.theme else (255, 255, 255)),
                                      hover_color='gray', text_size=30, theme=self.theme)

        self.settings_button = Button(center_x, start_y + 2 * (button_height + spacing), button_width,
                                      button_height,
                                      translations[self.language]['Settings'],
                                      ((0, 0, 0) if self.theme else (255, 255, 255)), hover_color='gray',
                                      text_size=30, theme=self.theme)

        self.results_button = Button(center_x, start_y + 3 * (button_height + spacing), button_width,
                                     button_height, translations[self.language]['Results'],
                                     ((0, 0, 0) if self.theme else (255, 255, 255)),
                                     hover_color='gray', text_size=30, theme=self.theme)

        self.save_exit_button = Button(center_x, start_y + 4 * (button_height + spacing), button_width,
                                       button_height, translations[self.language]['Save and Exit'],
                                       ((0, 0, 0) if self.theme else (255, 255, 255)),
                                       hover_color='gray', text_size=30, theme=self.theme)

        self.buttons = [
            self.continue_button,
            self.settings_button,
            self.results_button,
            self.save_exit_button,
            self.log_in_button,
        ]

    def change_theme(self):
        # так как темы 2, просто перевернём её
        self.theme = int(not (bool(self.theme)))
        # заново инициализируем кнопки
        self.init_button()

    def change_language(self, language):
        # меняем язык на противоположный
        self.language = language
        # заново инициализируем кнопки
        self.init_button()
