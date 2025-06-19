import pygame
from src.model.castle import Castle
from src.view.game_renderer import GameRenderer
from src.utils.constants import (
    GRID_SIZE_X, GRID_SIZE_Y, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y,
    SCREEN_WIDTH, DIFFICULTY_SETTINGS, SCREEN_HEIGHT, BRIDGE_HEIGHT,
    BRIDGE_WIDTH, BRIDGE_X, BRIDGE_Y
)
from src.logic.grid_manager import GridManager
from src.logic.monster_manager import MonsterManager
from src.logic.game_state import GameState


class Game:
    def __init__(self, difficulty="любитель"):
        """Инициализирует игру с указанным уровнем сложности.

        Args:
            difficulty (str): Уровень сложности ('новичок', 'любитель', 'профи').
        """
        self.difficulty = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.state = GameState(difficulty)
        self.grid_manager = GridManager()
        self.monster_manager = MonsterManager(difficulty)
        self.castle = Castle(settings["castle_hp"])

        # Загрузка изображений
        self.bridge_image = pygame.image.load(
            r'assets\images\bridge.png').convert_alpha()
        self.bridge_image = pygame.transform.scale(
            self.bridge_image, (BRIDGE_WIDTH, BRIDGE_HEIGHT))
        self.background = pygame.image.load(r'assets\images\game.png').convert()
        self.background = pygame.transform.scale(
            self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.renderer = GameRenderer(self.state, self.castle)

    def draw(self, surface):
        """Отрисовывает все компоненты игры на поверхности.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        surface.blit(self.background, (0, 0))
        surface.blit(self.bridge_image, (BRIDGE_X, BRIDGE_Y))

        # Рисуем игровое поле
        self.grid_manager.draw_grid(surface)
        self.grid_manager.draw_selected_tile(surface, self.state.selected_tile)

        # Рисуем монстров и крепость
        for monster in self.monster_manager.monsters:
            monster.draw(surface)
        self.castle.draw(surface)

        # Игровая информация (HP крепости, кнопка меню)
        self.renderer.draw_game_info(surface)
        self.renderer.draw_pause(surface)
        self.renderer.draw_game_over(surface)
        self.renderer.draw_win(surface)

    def handle_click(self, pos):
        """Обрабатывает клик мыши по игровому полю.

        Args:
            pos (tuple): Координаты клика (x, y).

        Returns:
            str or None: "menu" если клик по кнопке меню, иначе None.
        """
        if self.state.menu_button.collidepoint(pos):
            self.toggle_pause()
            return "menu"

        if self.state.paused:
            action = self.state.handle_pause_click(pos)
            if action == "continue":
                self.toggle_pause()
            elif action == "restart":
                return "restart"
            elif action == "exit":
                return "exit"
            return None

        if self.state.game_over or self.state.win:
            return None

        x = (pos[0] - GRID_OFFSET_X) // TILE_SIZE
        y = (pos[1] - GRID_OFFSET_Y) // TILE_SIZE

        if not (0 <= x < GRID_SIZE_X and 0 <= y < GRID_SIZE_Y):
            return None
        if self.grid_manager.grid[x][y] is None:
            return None

        if self.state.selected_tile is None:
            self.state.selected_tile = (x, y)
        else:
            prev_x, prev_y = self.state.selected_tile
            if (abs(x - prev_x) == 1 and y == prev_y) or (abs(y - prev_y) == 1 and x == prev_x):
                self.grid_manager.swap_tiles((prev_x, prev_y), (x, y))

                if not self.grid_manager.find_matches():
                    self.grid_manager.swap_tiles((x, y), (prev_x, prev_y))
                else:
                    damage = self.grid_manager.remove_matches()
                    while self.grid_manager.find_matches():
                        damage += self.grid_manager.remove_matches()

                    if self.monster_manager.apply_damage(damage):
                        self.state.win = True

            self.state.selected_tile = None

    def update(self):
        """Обновляет состояние игры."""
        if self.state.game_over or self.state.win or self.state.paused:
            return

        delta_time = self.state.update_time()
        self.grid_manager.update_tiles()

        if self.monster_manager.update(delta_time, self.state.game_time, self.castle):
            self.state.game_over = True

    def toggle_pause(self):
        """Переключает состояние паузы"""
        self.state.paused = not self.state.paused
