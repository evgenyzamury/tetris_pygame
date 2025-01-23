import pygame
from Button import ColorButton


class MenuUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sound = pygame.mixer.Sound('data/sounds/button.mp3')
        self.buttons = []

        button_width = 200
        button_height = 60
        spacing = 20

        center_x = self.width // 2 - button_width // 2
        start_y = self.height // 2 - (2 * button_height + 1.5 * spacing)

        self.continue_button = ColorButton(center_x, start_y, button_width, button_height, 'Continue', 'black',
                                           hover_color='gray', text_size=30)
        self.settings_button = ColorButton(center_x, start_y + button_height + spacing, button_width, button_height,
                                           'Settings', 'black', hover_color='gray', text_size=30)
        self.results_button = ColorButton(center_x, start_y + 2 * (button_height + spacing), button_width,
                                          button_height, 'Results', 'black', hover_color='gray', text_size=30)
        self.save_exit_button = ColorButton(center_x, start_y + 3 * (button_height + spacing), button_width,
                                            button_height, 'Save and Exit', 'black', hover_color='gray', text_size=30)

        self.buttons = [
            self.continue_button,
            self.settings_button,
            self.results_button,
            self.save_exit_button
        ]

    def render(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    if not button.is_hovered:
                        self.sound.play()
                        button.is_hovered = True
                else:
                    button.is_hovered = False


    def get_button_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    return button.text
        return None
