import pygame
from constants import TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y


class Tile:
    def __init__(self, grid_x, grid_y, color):
        """Инициализирует тайл с заданными координатами и цветом.

        Args:
            grid_x (int): Координата X в сетке.
            grid_y (int): Координата Y в сетке.
            color (tuple): Цвет тайла в формате RGB.
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.color = color
        self.pixel_x = GRID_OFFSET_X + grid_x * TILE_SIZE
        self.pixel_y = GRID_OFFSET_Y + grid_y * TILE_SIZE
        self.rect = pygame.Rect(self.pixel_x, self.pixel_y, TILE_SIZE, TILE_SIZE)
        self.is_falling = False
        self.fall_speed = 0
        self.special_effect = None
        self.effect_timer = 0
        self.image = None
        self.load_image()

    def load_image(self):
        """Загружает изображение в зависимости от цвета тайла"""
        color_to_image = {
            (255, 0, 0): r'images\fire.png',     # RED
            (0, 255, 0): r'images\air.png',   # GREEN
            (0, 0, 255): r'images\water.png',    # BLUE
            (255, 255, 0): r'images\light.png',  # YELLOW
            (255, 0, 255): r'images\dark.png',  # PURPLE
            (0, 255, 255): r'images\earth.png'   # CYAN
        }
        image_file = color_to_image.get(self.color, r'images\default.png')
        self.image = pygame.image.load(image_file).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))

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
        """Обновляет координаты в сетке и пересчитывает пиксельные коор-ты

        Args:
            new_grid_x (int): Новая координата X в сетке.
            new_grid_y (int): Новая координата Y в сетке.
        """
        self.grid_x = new_grid_x
        self.grid_y = new_grid_y
        self.pixel_x = GRID_OFFSET_X + new_grid_x * TILE_SIZE
        self.pixel_y = GRID_OFFSET_Y + new_grid_y * TILE_SIZE
        self.rect.x = self.pixel_x
        self.rect.y = self.pixel_y

    def draw(self, surface):
        """Отрисовывает тайл на указанной поверхности.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        surface.blit(self.image, (self.pixel_x, self.pixel_y))
        # Если есть спецэффект, рисуем поверх
        if self.special_effect:
            self.draw_effect(surface)

    def draw_effect(self, surface):
        """Отрисовывает спецэффекты для тайла"""
        effect_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        if self.special_effect == 'row_clear':
            pygame.draw.line(effect_surface, (255, 255, 0, 150),
                             (0, TILE_SIZE//2), (TILE_SIZE, TILE_SIZE//2), 3)
        elif self.special_effect == 'column_clear':
            pygame.draw.line(effect_surface, (255, 255, 0, 150),
                             (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE), 3)
        elif self.special_effect == 'color_clear':
            pygame.draw.circle(effect_surface, (255, 255, 0, 150),
                               (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2, 2)

        surface.blit(effect_surface, (self.pixel_x, self.pixel_y))
