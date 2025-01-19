import pygame


class ColorButton:
    def __init__(self, x, y, width, height, text, color, hover_color=None, text_size=20):
        self.rect = pygame.Rect(x, y, width, height)  # Создание rect
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.color = pygame.Color(color)
        self.font = pygame.font.SysFont(None, self.text_size)
        self.hover_color = pygame.Color(hover_color if hover_color else color)
        self.hover = False
        self.is_hovered = False

    def draw(self, screen):
        # Если курсор на кнопке, рисуем её другим цветом
        color_to_draw = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color_to_draw, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def check_hover(self, pos):  # проверяем навились ли мы на кнопку
        if self.rect.collidepoint(pos):
            self.hover = True
        else:
            self.hover = False

    def handle_event(self, event):
        # проверяем произошло ли нажатие на кнопку мыши, нажата именно ЛКМ и наведён ли курсор на мышку
        if self.hover and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.text
        return None


class MenuUI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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

    def draw(self, screen):
        # Используем цвет подсветки, если кнопка наведена
        color_to_use = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color_to_use, self.rect)

        # Рисуем текст на кнопке
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        # Проверка, находится ли курсор над кнопкой
        if self.rect.collidepoint(pos):
            self.is_hovered = True
        else:
            self.is_hovered = False

    def render(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return self.text
        return None

    def get_button_action(self, event):
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                return button.text
        return None
