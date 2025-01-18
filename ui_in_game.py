import pygame

from ui_menu import MenuUI


class InGameUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 30)
        self.pause_button_rect = pygame.Rect(10, 10, 100, 40)
        self.score = 0
        self.level = 1
        self.buttons = [self.pause_button_rect]

        self.is_paused = False
        self.menu_ui = MenuUI(self.width, self.height)

    def render(self, screen):
        if self.is_paused:
            self.menu_ui.render(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_button_rect.collidepoint(event.pos) and not self.is_paused:
                self.is_paused = True

        if self.is_paused:
            self.menu_ui.handle_event(event)
            action = self.menu_ui.get_button_action(event)
            if action == 'Continue':
                self.is_paused = False
            elif action == 'Save and Exit':
                self.is_paused = False

    def update_score(self, score, level):
        self.score = score
        self.level = level
