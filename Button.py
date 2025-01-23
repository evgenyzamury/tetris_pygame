import pygame


class ColorButton:
    def __init__(self, x, y, width, height, text, color, hover_color=None, text_color=(0, 0, 0),
                 bg_color=(0, 0, 0), text_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.color = pygame.Color(color)
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = pygame.font.SysFont(None, self.text_size)
        self.sound = pygame.mixer.Sound('data/sounds/button.mp3')
        self.hover_color = pygame.Color(hover_color if hover_color else color)
        self.hover = False
        self.is_hovered = False

    def draw(self, screen):
        # Если курсор на кнопке, рисуем её другим цветом
        color_to_draw = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color_to_draw, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
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
            self.sound.play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return self.text
        return None
