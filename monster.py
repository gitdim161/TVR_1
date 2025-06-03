import pygame
from constants import SCREEN_WIDTH, RED, BLACK, GREEN, MONSTER_PATH_Y


class Monster:
    def __init__(self, hp, damage, speed):
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.speed = speed
        self.x = -50
        self.y = MONSTER_PATH_Y
        self.width = 40
        self.height = 40
        self.progress = 0
        self.image = None
        self.image = pygame.image.load(r'images\monster.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def update(self):
        self.progress += self.speed / 1000
        self.x = self.progress * (SCREEN_WIDTH - 100)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, self.y - 10, self.width, 5))
        pygame.draw.rect(surface, GREEN,
                         (self.x, self.y - 10, self.width * (self.hp / self.max_hp), 5))

    def reached_castle(self):
        return self.progress >= 0.9
