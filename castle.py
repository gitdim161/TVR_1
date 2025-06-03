import pygame
from constants import SCREEN_WIDTH, BLACK, GREEN, BRIDGE_X, BRIDGE_Y, BRIDGE_WIDTH


class Castle:
    def __init__(self, hp=100):
        self.hp = hp
        self.max_hp = hp
        self.width = 200
        self.height = 250
        self.x = BRIDGE_X + BRIDGE_WIDTH - 40  # Ставим крепость в конце моста
        self.y = BRIDGE_Y - self.height + 30  # Выравниваем по низу моста

        # Загрузка изображения
        self.image = pygame.image.load(r'images\castle.png').convert_alpha()
        # Масштабирование под нужный размер
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, (150, 150, 150), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, BLACK, (self.x, self.y - 20, self.width, 10))
        pygame.draw.rect(surface, BLACK, (self.x, self.y - 20, self.width, 10))
        pygame.draw.rect(surface, GREEN,
                         (self.x, self.y - 20, self.width * (self.hp / self.max_hp), 10))

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)  # Гарантируем, что HP не станет отрицательным
        return self.hp <= 0  # Возвращаем True, если крепость уничтожена
