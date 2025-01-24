import pygame
from variables import WIDTH, HEIGHT, difficulty_list, language_list, theme_list
from database import get_player_settings, update_player_settings


class SettingsUI:
    def __init__(self):
        music_volume, block_volume, difficulty, language, theme = get_player_settings()
        self.width = WIDTH
        self.height = HEIGHT
        self.font = pygame.font.SysFont(None, 30)

        self.theme_colors = {
            "Light": {"bg": pygame.Color("white"), "text": pygame.Color("black")},
            "Dark": {"bg": pygame.Color("black"), "text": pygame.Color("white")},
        }

        self.options = {
            "music_volume": music_volume,
            "block_volume": block_volume,
            "difficulty": difficulty,
            "language": language,
            "theme": theme,
        }
        print(self.options)

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
        print(theme)
        self.bg_color = self.theme_colors[theme_list[theme]]["bg"]
        self.text_color = self.theme_colors[theme_list[theme]]["text"]

    def render(self, screen):
        screen.fill(self.bg_color)

        title = self.font.render("Settings", True, self.text_color)
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))

        music_label = self.font.render("Music Volume", True, self.text_color)
        screen.blit(music_label, (50, 90))
        pygame.draw.rect(screen, self.text_color, self.music_slider_rect, 2)
        volume_indicator = pygame.Rect(
            self.music_slider_rect.x + (self.music_slider_rect.width * self.options["music_volume"] // 100) - 5,
            self.music_slider_rect.y - 5, 10, 20)
        pygame.draw.rect(screen, self.text_color, volume_indicator)

        block_label = self.font.render("Block Volume", True, self.text_color)
        screen.blit(block_label, (50, 190))
        pygame.draw.rect(screen, self.text_color, self.block_slider_rect, 2)
        block_indicator = pygame.Rect(
            self.block_slider_rect.x + (self.block_slider_rect.width * self.options["block_volume"] // 100) - 5,
            self.block_slider_rect.y - 5, 10, 20)
        pygame.draw.rect(screen, self.text_color, block_indicator)

        difficulty_label = self.font.render("Difficulty", True, self.text_color)
        screen.blit(difficulty_label, (50, 290))
        for button in self.difficulty_buttons:
            pygame.draw.rect(screen, self.text_color, button["rect"], 2)
            text = self.font.render(button["text"], True, self.text_color)
            screen.blit(text, (button["rect"].x + (button["rect"].width - text.get_width()) // 2,
                               button["rect"].y + (button["rect"].height - text.get_height()) // 2))

        language_label = self.font.render("Language", True, self.text_color)
        screen.blit(language_label, (50, 390))
        for button in self.language_buttons:
            pygame.draw.rect(screen, self.text_color, button["rect"], 2)
            text = self.font.render(button["text"], True, self.text_color)
            screen.blit(text, (button["rect"].x + (button["rect"].width - text.get_width()) // 2,
                               button["rect"].y + (button["rect"].height - text.get_height()) // 2))

        theme_label = self.font.render("Theme", True, self.text_color)
        screen.blit(theme_label, (50, 490))
        for button in self.theme_buttons:
            pygame.draw.rect(screen, self.text_color, button["rect"], 2)
            text = self.font.render(button["text"], True, self.text_color)
            screen.blit(text, (button["rect"].x + (button["rect"].width - text.get_width()) // 2,
                               button["rect"].y + (button["rect"].height - text.get_height()) // 2))

        pygame.draw.rect(screen, self.text_color, self.back_button_rect, 2)
        back_text = self.font.render("Back", True, self.text_color)
        screen.blit(back_text, (self.back_button_rect.x + (self.back_button_rect.width - back_text.get_width()) // 2,
                                self.back_button_rect.y + (self.back_button_rect.height - back_text.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.music_slider_rect.collidepoint(event.pos):
                self.options["music_volume"] = max(0, min(100, (
                        event.pos[0] - self.music_slider_rect.x) * 100 // self.music_slider_rect.width))
                print('ok')
                print(self.options["music_volume"])
                update_player_settings(self.options["music_volume"], self.options["block_volume"],
                                       self.options["difficulty"],
                                       self.options["language"], self.options["theme"])

            elif self.block_slider_rect.collidepoint(event.pos):
                self.options["block_volume"] = max(0, min(100, (
                        event.pos[0] - self.block_slider_rect.x) * 100 // self.block_slider_rect.width))
                update_player_settings(self.options["music_volume"], self.options["block_volume"],
                                       self.options["difficulty"],
                                       self.options["language"], self.options["theme"])

            elif self.back_button_rect.collidepoint(event.pos):
                return "back", self.options["music_volume"] / 100

            for button in self.difficulty_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.options["difficulty"] = button["text"]
                    update_player_settings(self.options["music_volume"], self.options["block_volume"],
                                           self.options["difficulty"],
                                           self.options["language"], self.options["theme"])

            for button in self.language_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.options["language"] = button["text"]
                    update_player_settings(self.options["music_volume"], self.options["block_volume"],
                                           self.options["difficulty"],
                                           self.options["language"], self.options["theme"])

            for button in self.theme_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.options["theme"] = theme_list.index(button["text"])
                    self.update_theme_colors()
                    update_player_settings(self.options["music_volume"], self.options["block_volume"],
                                           self.options["difficulty"],
                                           self.options["language"], self.options["theme"])

        return None, self.options["music_volume"] / 100
