import pygame
from constants import TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, BLACK


class Tile:
    def __init__(self, grid_x, grid_y, color):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.pixel_x = GRID_OFFSET_X + grid_x * TILE_SIZE
        self.pixel_y = GRID_OFFSET_Y + grid_y * TILE_SIZE
        self.rect = pygame.Rect(self.pixel_x, self.pixel_y, TILE_SIZE, TILE_SIZE)
        self.is_falling = False
        self.fall_speed = 0
        self.special_effect = None  # 'row_clear', 'column_clear', 'color_clear'
        self.effect_timer = 0

    def update(self):
        """Обновляет позицию для анимации падения"""
        if self.is_falling:
            target_y = GRID_OFFSET_Y + self.grid_y * TILE_SIZE
            if self.pixel_y < target_y:
                self.pixel_y = min(target_y, self.pixel_y + self.fall_speed)
                self.rect.y = self.pixel_y
            else:
                self.is_falling = False
                self.pixel_y = target_y
                self.rect.y = self.pixel_y

    def update_position(self, new_grid_x, new_grid_y):
        """Обновляет координаты в сетке и пересчитывает пиксельные коор-ты"""
        self.grid_x = new_grid_x
        self.grid_y = new_grid_y
        self.pixel_x = GRID_OFFSET_X + new_grid_x * TILE_SIZE
        self.pixel_y = GRID_OFFSET_Y + new_grid_y * TILE_SIZE
        self.rect.x = self.pixel_x
        self.rect.y = self.pixel_y

    def draw(self, surface):
        """Отрисовывает тайл"""
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 1)
