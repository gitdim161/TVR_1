import pygame
from src.utils.constants import (
    BLACK, GREEN, MONSTER_PATH_Y, BRIDGE_X, BRIDGE_WIDTH
)


class Monster:
    def __init__(self, hp, damage, speed):
        """Инициализирует монстра с указанными характеристиками.

        Args:
            hp (int): Здоровье монстра.
            damage (int): Урон, наносимый монстром.
            speed (float): Скорость движения монстра.
        """
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.speed = speed
        self.x = BRIDGE_X   # Начинаем движение слева от моста
        self.y = MONSTER_PATH_Y - 140  # Центрируем по вертикали моста
        self.width = 100
        self.height = 120
        self.progress = 0
        self.image = None
        self.image = pygame.image.load(r'assets\images\monster.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        """Обновляет позицию монстра на мосту."""
        self.progress += self.speed / 1000
        self.x = BRIDGE_X + self.progress * BRIDGE_WIDTH

    def draw(self, surface):
        '''Отрисовка монстров и полоски hp'''
        surface.blit(self.image, (self.x, self.y))
        pygame.draw.rect(surface, BLACK, (self.x, self.y - 10, self.width, 5))
        pygame.draw.rect(surface, GREEN,
                         (self.x, self.y - 10, self.width * (self.hp / self.max_hp), 5))

    def reached_castle(self):
        """Проверяет, достиг ли монстр крепости.

        Returns:
            bool: True, если монстр достиг крепости, иначе False.
        """
        return self.progress >= 0.9
