import pygame


class ColorButton:
    def __init__(self, x, y, width, height, text, color, hover_color=None, text_size=20):
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.color = pygame.Color(color)
        self.hover_color = pygame.Color(hover_color if hover_color else color)
        self.hover = False

    def draw(self, screen):
        if self.hover and self.hover_color:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text:
            font = pygame.font.Font(None, self.text_size)
            text = font.render(self.text, True, '#7b8a9c')
            screen.blit(text, (
                self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 - text.get_height() // 2))

        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 1)

    def check_hover(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.hover = True
        else:
            self.hover = False

    def handle_event(self, event):
        # проверяем произошло ли нажатие на кнопку мыши, нажата именно ЛКМ и наведён ли курсор на мышку
        if self.hover and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
