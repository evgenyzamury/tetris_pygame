from variables import WIDTH, HEIGHT


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # сдвинуть камеру на координаты:
    def update(self, target):
        self.dx = target[0]
        self.dy = target[1]
