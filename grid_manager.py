import pygame
import random
from tile import Tile
from constants import GRID_SIZE_X, GRID_SIZE_Y, COLORS, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, WHITE


class GridManager:
    def __init__(self):
        self.grid = []
        self.initialize_grid()

    def initialize_grid(self):
        self.grid = []
        for x in range(GRID_SIZE_X):
            column = []
            for y in range(GRID_SIZE_Y):
                color = random.choice(COLORS)
                column.append(Tile(x, y, color))
            self.grid.append(column)

        while self.find_matches():
            self.remove_matches()
            self.fill_empty_spaces()

    def draw_grid(self, surface):
        for x in range(GRID_SIZE_X):
            for y in range(GRID_SIZE_Y):
                tile = self.grid[x][y]
                if tile is not None:
                    tile.draw(surface)

    def draw_selected_tile(self, surface, selected_tile):
        if selected_tile:
            x, y = selected_tile
            rect = pygame.Rect(
                GRID_OFFSET_X + x * TILE_SIZE,
                GRID_OFFSET_Y + y * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(surface, WHITE, rect, 3)

    def swap_tiles(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        if not (0 <= x1 < GRID_SIZE_X and 0 <= y1 < GRID_SIZE_Y and
                0 <= x2 < GRID_SIZE_X and 0 <= y2 < GRID_SIZE_Y):
            return False

        if self.grid[x1][y1] is None or self.grid[x2][y2] is None:
            return False

        self.grid[x1][y1], self.grid[x2][y2] = self.grid[x2][y2], self.grid[x1][y1]
        self.grid[x1][y1].update_position(x1, y1)
        self.grid[x2][y2].update_position(x2, y2)
        return True

    def find_matches(self):
        matches = []
        # Горизонтальные совпадения
        for y in range(GRID_SIZE_Y):
            x = 0
            while x < GRID_SIZE_X - 2:
                if self.grid[x][y] is None:
                    x += 1
                    continue

                color = self.grid[x][y].color
                match_length = 1

                while (x + match_length < GRID_SIZE_X and
                       self.grid[x + match_length][y] is not None and
                       self.grid[x + match_length][y].color == color):
                    match_length += 1

                if match_length >= 3:
                    matches.append([(x + i, y) for i in range(match_length)])
                    x += match_length
                else:
                    x += 1

        # Вертикальные совпадения
        for x in range(GRID_SIZE_X):
            y = 0
            while y < GRID_SIZE_Y - 2:
                if self.grid[x][y] is None:
                    y += 1
                    continue

                color = self.grid[x][y].color
                match_length = 1

                while (y + match_length < GRID_SIZE_Y and
                       self.grid[x][y + match_length] is not None and
                       self.grid[x][y + match_length].color == color):
                    match_length += 1

                if match_length >= 3:
                    matches.append([(x, y + i) for i in range(match_length)])
                    y += match_length
                else:
                    y += 1

        return matches

    def remove_matches(self):
        matches = self.find_matches()
        damage = 0
        positions_to_clear = set()

        for match in matches:
            match_length = len(match)
            first_x, first_y = match[0]
            color = self.grid[first_x][first_y].color
            is_horizontal = all(m[1] == first_y for m in match)

            if match_length == 4:
                if is_horizontal:
                    for x in range(GRID_SIZE_X):
                        positions_to_clear.add((x, first_y))
                else:
                    for y in range(GRID_SIZE_Y):
                        positions_to_clear.add((first_x, y))
                damage += GRID_SIZE_X * 2

            elif match_length >= 5:
                for x in range(GRID_SIZE_X):
                    for y in range(GRID_SIZE_Y):
                        if self.grid[x][y] is not None and self.grid[x][y].color == color:
                            positions_to_clear.add((x, y))
                damage += GRID_SIZE_X * GRID_SIZE_Y

            else:
                for pos in match:
                    positions_to_clear.add(pos)
                damage += len(match)

        for x, y in positions_to_clear:
            if self.grid[x][y] is not None:
                self.grid[x][y] = None

        if positions_to_clear:
            self.fill_empty_spaces()

        return damage

    def fill_empty_spaces(self):
        for x in range(GRID_SIZE_X):
            empty_spots = []
            for y in range(GRID_SIZE_Y - 1, -1, -1):
                if self.grid[x][y] is None:
                    empty_spots.append(y)
                elif empty_spots:
                    lowest_empty = empty_spots.pop(0)
                    self.grid[x][lowest_empty] = self.grid[x][y]
                    self.grid[x][y] = None
                    self.grid[x][lowest_empty].update_position(x, lowest_empty)
                    self.grid[x][lowest_empty].is_falling = True
                    self.grid[x][lowest_empty].fall_speed = 5
                    self.grid[x][lowest_empty].pixel_y = GRID_OFFSET_Y + y * TILE_SIZE
                    empty_spots.append(y)

            for empty_y in empty_spots:
                color = random.choice(COLORS)
                new_tile = Tile(x, empty_y, color)
                new_tile.pixel_y = GRID_OFFSET_Y - TILE_SIZE
                new_tile.is_falling = True
                new_tile.fall_speed = 5
                self.grid[x][empty_y] = new_tile

    def update_tiles(self):
        for x in range(GRID_SIZE_X):
            for y in range(GRID_SIZE_Y):
                tile = self.grid[x][y]
                if tile is not None:
                    tile.update()
                    if hasattr(tile, 'effect_timer'):
                        tile.effect_timer += 1
                        if tile.effect_timer > 90:
                            tile.special_effect = None
