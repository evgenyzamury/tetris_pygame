import pygame

import blocks
from variables import WIDTH, HEIGHT, difficulty_list, language_list, theme_list, get_translation
from database import get_player_settings, update_player_settings
from ui_menu import MenuUI


class SettingsUI:
    def __init__(self, music_volume, block_volume, difficulty, language, theme):
        self.width = WIDTH
        self.height = HEIGHT
        self.font = pygame.font.SysFont(None, 30)

        self.white_img_instruction = pygame.image.load('data/image/instructions.jpg')
        self.dark_img_instruction = pygame.image.load('data/image/dark_img_instructions.jpg')
        self.decoretion_white_theme = pygame.image.load('data/image/gameboy.png')
        self.decoretion_dark_theme = pygame.image.load('data/image/dark_theme_gameboy.png')

        self.theme_colors = {
            "Light": {"bg": pygame.Color("white"), "text": pygame.Color("black")},
            "Dark": {"bg": pygame.Color("black"), "text": pygame.Color("white")},
        }

        self.options = {
            "music_volume": music_volume,
            "sfx_volume": block_volume,
            "difficulty": difficulty,
            "language": language,
            "theme": theme,
        }

        self.update_theme_colors()

        self.music_slider_rect = pygame.Rect(200, 100, 300, 10)
        self.block_slider_rect = pygame.Rect(200, 200, 300, 10)
        self.difficulty_buttons = [
            {"text": difficulty_list[0], "rect": pygame.Rect(200, 300, 100, 40)},
            {"text": difficulty_list[1], "rect": pygame.Rect(310, 300, 100, 40)},
            {"text": difficulty_list[2], "rect": pygame.Rect(420, 300, 150, 40)},
        ]
        self.language_buttons = [
            {"text": language_list[0], "rect": pygame.Rect(200, 400, 100, 40)},
            {"text": language_list[1], "rect": pygame.Rect(310, 400, 100, 40)},
        ]
        self.theme_buttons = [
            {"text": "Light", "rect": pygame.Rect(200, 500, 100, 40)},
            {"text": "Dark", "rect": pygame.Rect(310, 500, 100, 40)},
        ]
        self.back_button_rect = pygame.Rect(50, 600, 120, 50)

    def update_theme_colors(self):
        theme = self.options["theme"]
        self.bg_color = self.theme_colors[theme_list[theme]]["bg"]
        self.text_color = self.theme_colors[theme_list[theme]]["text"]

    def render(self, screen):
        screen.fill(self.bg_color)

        title = self.font.render(get_translation("Settings", self.options["language"]), True, self.text_color)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))

        music_label = self.font.render(get_translation("Music Volume", self.options["language"]), True, self.text_color)
        screen.blit(music_label, (50, 90))
        pygame.draw.rect(screen, self.text_color, self.music_slider_rect, 2)
        volume_indicator = pygame.Rect(
            self.music_slider_rect.x + (self.music_slider_rect.width * self.options["music_volume"] // 100) - 5,
            self.music_slider_rect.y - 5, 10, 20)
        pygame.draw.rect(screen, self.text_color, volume_indicator)

        block_label = self.font.render(get_translation("SFX Volume", self.options["language"]), True, self.text_color)
        screen.blit(block_label, (50, 190))
        pygame.draw.rect(screen, self.text_color, self.block_slider_rect, 2)
        block_indicator = pygame.Rect(
            self.block_slider_rect.x + (self.block_slider_rect.width * self.options["sfx_volume"] // 100) - 5,
            self.block_slider_rect.y - 5, 10, 20)
        pygame.draw.rect(screen, self.text_color, block_indicator)

        difficulty_label = self.font.render(get_translation("Difficulty", self.options["language"]), True,
                                            self.text_color)
        screen.blit(difficulty_label, (50, 290))
        for button in self.difficulty_buttons:
            pygame.draw.rect(screen, self.text_color, button["rect"], 2)
            text = self.font.render(button["text"], True, self.text_color)
            screen.blit(text, (button["rect"].x + (button["rect"].width - text.get_width()) // 2,
                               button["rect"].y + (button["rect"].height - text.get_height()) // 2))

        language_label = self.font.render(get_translation("Language", self.options["language"]), True, self.text_color)
        screen.blit(language_label, (50, 390))
        for button in self.language_buttons:
            pygame.draw.rect(screen, self.text_color, button["rect"], 2)
            text = self.font.render(button["text"], True, self.text_color)
            screen.blit(text, (button["rect"].x + (button["rect"].width - text.get_width()) // 2,
                               button["rect"].y + (button["rect"].height - text.get_height()) // 2))

        theme_label = self.font.render(get_translation("Theme", self.options["language"]), True, self.text_color)
        screen.blit(theme_label, (50, 490))
        for button in self.theme_buttons:
            pygame.draw.rect(screen, self.text_color, button["rect"], 2)
            text = self.font.render(button["text"], True, self.text_color)
            screen.blit(text, (button["rect"].x + (button["rect"].width - text.get_width()) // 2,
                               button["rect"].y + (button["rect"].height - text.get_height()) // 2))

        pygame.draw.rect(screen, self.text_color, self.back_button_rect, 2)
        back_text = self.font.render(get_translation("Back", self.options["language"]), True, self.text_color)
        screen.blit(back_text, (self.back_button_rect.x + (self.back_button_rect.width - back_text.get_width()) // 2,
                                self.back_button_rect.y + (self.back_button_rect.height - back_text.get_height()) // 2))

        # инструкция управления
        if self.bg_color == (255, 255, 255):
            scaled_img = pygame.transform.scale(self.white_img_instruction, (320, 390))
            screen.blit(scaled_img, (440, 460))

            scaled_img = pygame.transform.scale(self.decoretion_white_theme, (60, 60))
            screen.blit(scaled_img, (720, 10))
        else:
            scaled_img = pygame.transform.scale(self.dark_img_instruction, (320, 390))
            screen.blit(scaled_img, (440, 460))

            scaled_img = pygame.transform.scale(self.decoretion_dark_theme, (60, 60))
            screen.blit(scaled_img, (720, 10))

    def change_speed_block(self):
        # Установка скорости в зависимости от сложности
        if self.options['difficulty'] == 0:
            self.options['block_speed'] = 1
        elif self.options['difficulty'] == 1:
            self.options['block_speed'] = 3
        elif self.options['difficulty'] == 2:
            self.options['block_speed'] = 10

    def handle_event(self, event):
        # создадим переменную в которую будем записывать сигнал, если пользователь что-то поменяет
        signal = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            # смена звук музыки
            if self.music_slider_rect.collidepoint(event.pos):
                self.options["music_volume"] = max(0, min(100, (
                        event.pos[0] - self.music_slider_rect.x) * 100 // self.music_slider_rect.width))
                signal = 'music volume'

            # смена звука блока
            elif self.block_slider_rect.collidepoint(event.pos):
                self.options["sfx_volume"] = max(0, min(100, (
                        event.pos[0] - self.block_slider_rect.x) * 100 // self.block_slider_rect.width))
                signal = 'sfx volume'

            # сигнал кнопки назад
            elif self.back_button_rect.collidepoint(event.pos):
                signal = 'back'

            # ловим сигнал смены сложности
            for button in self.difficulty_buttons:
                if button["rect"].collidepoint(event.pos):  # Если пользователь кликнул по кнопке
                    selected_difficulty = button["text"]
                    # Обновляем выбранную сложность
                    self.options["difficulty"] = difficulty_list.index(selected_difficulty)

                    # Установка скорости в зависимости от сложности
                    self.change_speed_block()

                    signal = 'difficulty'

            # ловим сигнал смены языка
            for button in self.language_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.options["language"] = "en" if button['text'] == 'English' else 'ru'
                    signal = 'language'

            # ловим темы
            for button in self.theme_buttons:
                if button["rect"].collidepoint(event.pos):
                    # проверяем что нажата клавиша новой темы
                    if self.options["theme"] != theme_list.index(button["text"]):
                        self.options["theme"] = theme_list.index(button["text"])
                        self.update_theme_colors()
                        signal = 'theme'

        if signal:
            # обновляем базу данных
            update_player_settings(self.options["music_volume"], self.options["sfx_volume"],
                                   self.options["difficulty"],
                                   self.options["language"], self.options["theme"])

        return signal
