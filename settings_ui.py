import pygame


class SettingsUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 30)

        self.theme_colors = {
            "Light": {"bg": pygame.Color("white"), "text": pygame.Color("black")},
            "Dark": {"bg": pygame.Color("black"), "text": pygame.Color("white")},
        }

        self.options = {
            "music_volume": 50,
            "block_volume": 50,
            "difficulty": "Medium",
            "language": "English",
            "theme": "Light",
        }

        self.update_theme_colors()

        self.music_slider_rect = pygame.Rect(200, 100, 300, 10)
        self.block_slider_rect = pygame.Rect(200, 200, 300, 10)
        self.difficulty_buttons = [
            {"text": "Easy", "rect": pygame.Rect(200, 300, 100, 40)},
            {"text": "Medium", "rect": pygame.Rect(310, 300, 100, 40)},
            {"text": "Impossible", "rect": pygame.Rect(420, 300, 150, 40)},
        ]
        self.language_buttons = [
            {"text": "English", "rect": pygame.Rect(200, 400, 100, 40)},
            {"text": "Русский", "rect": pygame.Rect(310, 400, 100, 40)},
        ]
        self.theme_buttons = [
            {"text": "Light", "rect": pygame.Rect(200, 500, 100, 40)},
            {"text": "Dark", "rect": pygame.Rect(310, 500, 100, 40)},
        ]
        self.back_button_rect = pygame.Rect(50, 600, 120, 50)

    def update_theme_colors(self):
        theme = self.options["theme"]
        self.bg_color = self.theme_colors[theme]["bg"]
        self.text_color = self.theme_colors[theme]["text"]

    def render(self, screen):
        screen.fill((0, 0, 0))
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
            elif self.block_slider_rect.collidepoint(event.pos):
                self.options["block_volume"] = max(0, min(100, (
                            event.pos[0] - self.block_slider_rect.x) * 100 // self.block_slider_rect.width))
            elif self.back_button_rect.collidepoint(event.pos):
                return "back"
            for button in self.difficulty_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.options["difficulty"] = button["text"]
            for button in self.language_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.options["language"] = button["text"]
            for button in self.theme_buttons:
                if button["rect"].collidepoint(event.pos):
                    self.options["theme"] = button["text"]
                    self.update_theme_colors()
        return None
