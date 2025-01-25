import pygame


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color=None,
                 bg_color=(0, 0, 0), text_size=20, theme=0):
        self.theme = theme
        self.rect = pygame.Rect(x, y, width, height)
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.color = pygame.Color(color)
        self.text_color = (255, 255, 255) if theme else (0, 0, 0)
        self.bg_color = bg_color
        self.font = pygame.font.SysFont(None, self.text_size)
        self.sound = pygame.mixer.Sound('data/sounds/button.mp3')
        self.hover_color = pygame.Color(hover_color if hover_color else color)
        self.hover = False

    def draw(self, screen):
        # Если курсор на кнопке, рисуем её другим цветом
        color_to_draw = self.hover_color if self.hover else self.color
        pygame.draw.rect(screen, color_to_draw, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))
        pygame.draw.rect(screen, self.text_color, self.rect, 1)

    def check_hover(self, pos):  # проверяем навились ли мы на кнопку`
        if self.rect.collidepoint(pos):
            if not self.hover:
                self.sound.set_volume(0.8)
                self.sound.play()
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
