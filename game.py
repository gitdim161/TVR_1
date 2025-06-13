import pygame
from castle import Castle
from constants import GRID_SIZE_X, GRID_SIZE_Y, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, SCREEN_WIDTH, DIFFICULTY_SETTINGS, SCREEN_HEIGHT, BRIDGE_HEIGHT, BRIDGE_WIDTH, BRIDGE_X, BRIDGE_Y
from grid_manager import GridManager
from monster_manager import MonsterManager
from game_state import GameState


class Game:
    def __init__(self, difficulty="любитель"):
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.state = GameState(difficulty)
        self.grid_manager = GridManager()
        self.monster_manager = MonsterManager(difficulty)
        self.castle = Castle(settings["castle_hp"])

        # Загрузка изображений
        self.bridge_image = pygame.image.load(
            r'images\bridge.png').convert_alpha()
        self.bridge_image = pygame.transform.scale(
            self.bridge_image, (BRIDGE_WIDTH, BRIDGE_HEIGHT))
        self.background = pygame.image.load(r'images\game.png').convert()
        self.background = pygame.transform.scale(
            self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.bridge_image, (BRIDGE_X, BRIDGE_Y))

        self.grid_manager.draw_grid(surface)
        self.grid_manager.draw_selected_tile(surface, self.state.selected_tile)

        for monster in self.monster_manager.monsters:
            monster.draw(surface)

        self.castle.draw(surface)
        self.state.draw_game_info(surface, self.castle)
        self.state.draw_game_over(surface)
        self.state.draw_win(surface)

    def handle_click(self, pos):
        if self.state.menu_button.collidepoint(pos):
            return "menu"
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
        if self.state.game_over or self.state.win:
            return

        delta_time = self.state.update_time()
        self.grid_manager.update_tiles()

        if self.monster_manager.update(delta_time, self.state.game_time, self.castle):
            self.state.game_over = True
