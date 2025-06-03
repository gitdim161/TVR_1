import pygame
import random
from tile import Tile
from monster import Monster
from castle import Castle
from constants import GRID_SIZE, SPAWN_INTERVAL, COLORS, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, SCREEN_WIDTH, BLACK, RED, WHITE, DIFFICULTY_SETTINGS, YELLOW, SCREEN_HEIGHT, MONSTER_PATH_Y, BUTTON_COLOR, TEXT_COLOR, GREEN, SHADOW_COLOR


class Game:
    def __init__(self, difficulty="любитель"):
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.difficulty = difficulty
        self.grid = []
        self.selected_tile = None
        self.monsters = []
        self.castle = Castle(settings["castle_hp"])
        self.spawn_interval = settings["spawn_interval"]
        self.max_moves = settings["max_moves"]
        self.moves_left = self.max_moves
        self.monster_settings = {
            "hp": settings["monster_hp"],
            "damage": settings["monster_damage"],
            "speed": settings["monster_speed"]
        }
        self.spawn_timer = 0
        self.last_time = pygame.time.get_ticks()
        self.game_over = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.menu_button = pygame.Rect(50, 10, 100, 40)
        self.win = False
        self.initialize_grid()

    def initialize_grid(self):
        self.grid = []
        for x in range(GRID_SIZE):
            column = []
            for y in range(GRID_SIZE):
                color = random.choice(COLORS)
                column.append(Tile(x, y, color))
            self.grid.append(column)

        while self.find_matches():
            self.remove_matches()
            self.fill_empty_spaces()

    def draw(self, surface):
        surface.fill(WHITE)
        # Рисуем сетку
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                tile = self.grid[x][y]
                if tile is not None:
                    tile.draw(surface)
        # Рисуем выделенный тайл
        if self.selected_tile:
            x, y = self.selected_tile
            rect = pygame.Rect(
                GRID_OFFSET_X + x * TILE_SIZE,
                GRID_OFFSET_Y + y * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(surface, WHITE, rect, 3)
        pygame.draw.rect(
            surface, RED, (0, MONSTER_PATH_Y - 20, SCREEN_WIDTH, 60))
        pygame.draw.rect(
            surface, BLACK, (0, MONSTER_PATH_Y - 20, SCREEN_WIDTH, 60), 2)

        pygame.draw.rect(surface, (150, 150, 150),
                         (0, MONSTER_PATH_Y - 15, SCREEN_WIDTH, 50))
        pygame.draw.lines(surface, YELLOW, False, [
                          (0, MONSTER_PATH_Y + 10), (SCREEN_WIDTH, MONSTER_PATH_Y + 10)], 3)
        shadow_surface = pygame.Surface(
            (TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, SHADOW_COLOR,
                         (0, 0, TILE_SIZE, TILE_SIZE), border_radius=5)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y] is not None:
                    # Рисуем сам тайл
                    self.grid[x][y].draw(surface)
        # Рисуем монстров
        for monster in self.monsters:
            monster.draw(surface)

        # Рисуем крепость
        self.castle.draw(surface)

        # Рисуем информацию
        font = pygame.font.SysFont('Arial', 24)
        moves_text = font.render(f"Ходы: {self.moves_left}/{self.max_moves}", True, BLACK)
        castle_hp_text = font.render(
            f"Крепость: {self.castle.hp}/{self.castle.max_hp}", True, BLACK)

        surface.blit(moves_text, (500, 500))
        surface.blit(castle_hp_text, (SCREEN_WIDTH - 200, 10))

        if self.game_over:
            game_over_text = font.render("ИГРА ОКОНЧЕНА!", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH //
                         2 - 100, SCREEN_HEIGHT // 2))

        pygame.draw.rect(surface, BUTTON_COLOR, self.menu_button)
        menu_text = self.font.render("Меню", True, TEXT_COLOR)
        surface.blit(menu_text, (self.menu_button.x +
                     20, self.menu_button.y + 10))

        if self.win:  # Добавляем сообщение о победе
            win_text = self.font.render(
                f'ПОБЕДА!', True, GREEN)
            restart_text = self.font.render(
                'Нажмите R для рестарта', True, BLACK)
            surface.blit(win_text, (SCREEN_WIDTH // 2 -
                         150, SCREEN_HEIGHT // 2 - 30))
            surface.blit(restart_text, (SCREEN_WIDTH //
                         2 - 120, SCREEN_HEIGHT // 2 + 20))

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                tile = self.grid[x][y]
                if tile is not None and hasattr(tile, 'special_effect'):
                    if tile.special_effect == 'row_clear':
                        pygame.draw.line(surface, (255, 255, 0, 150),
                                         (GRID_OFFSET_X, GRID_OFFSET_Y +
                                          y * TILE_SIZE + TILE_SIZE//2),
                                         (GRID_OFFSET_X + GRID_SIZE * TILE_SIZE,
                                          GRID_OFFSET_Y + y * TILE_SIZE + TILE_SIZE//2),
                                         3)
                    elif tile.special_effect == 'column_clear':
                        pygame.draw.line(surface, (255, 255, 0, 150),
                                         (GRID_OFFSET_X + x * TILE_SIZE +
                                          TILE_SIZE//2, GRID_OFFSET_Y),
                                         (GRID_OFFSET_X + x * TILE_SIZE + TILE_SIZE //
                                          2, GRID_OFFSET_Y + GRID_SIZE * TILE_SIZE),
                                         3)
                    elif tile.special_effect == 'color_clear':
                        pygame.draw.circle(surface, (255, 255, 0, 150),
                                           (GRID_OFFSET_X + x * TILE_SIZE + TILE_SIZE//2,
                                           GRID_OFFSET_Y + y * TILE_SIZE + TILE_SIZE//2),
                                           TILE_SIZE//2, 2)

    def handle_click(self, pos):
        if self.menu_button.collidepoint(pos):
            return "menu"
        if self.game_over or self.win:
            return None

        x = (pos[0] - GRID_OFFSET_X) // TILE_SIZE
        y = (pos[1] - GRID_OFFSET_Y) // TILE_SIZE

        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return None
        if self.grid[x][y] is None:  # Проверка на пустую ячейку
            return None
        if self.selected_tile is None:
            self.selected_tile = (x, y)
        else:
            # Проверяем, соседние ли тайлы
            prev_x, prev_y = self.selected_tile
            if (abs(x - prev_x) == 1 and y == prev_y) or (abs(y - prev_y) == 1 and x == prev_x):
                # Меняем тайлы местами
                self.swap_tiles((prev_x, prev_y), (x, y))
                self.moves_left -= 1

                # Проверяем, есть ли совпадения
                if not self.find_matches():
                    # Если нет, меняем обратно
                    self.swap_tiles((x, y), (prev_x, prev_y))
                    self.moves_left += 1
                else:
                    # Если есть, удаляем совпадения и обновляем поле
                    self.remove_matches()
                    self.fill_empty_spaces()

                    # Продолжаем проверять совпадения после заполнения
                    while self.find_matches():
                        self.remove_matches()
                        self.fill_empty_spaces()

                if self.moves_left <= 0 and len(self.monsters) > 0:
                    self.game_over = True
                elif len(self.monsters) == 0 and self.spawn_timer >= self.spawn_interval:
                    self.win = True

            self.selected_tile = None

    def swap_tiles(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        # Проверка на существование тайлов
        if not (0 <= x1 < GRID_SIZE and 0 <= y1 < GRID_SIZE and
                0 <= x2 < GRID_SIZE and 0 <= y2 < GRID_SIZE):
            return False

        if self.grid[x1][y1] is None or self.grid[x2][y2] is None:
            return False

        # Меняем тайлы местами в сетке
        self.grid[x1][y1], self.grid[x2][y2] = self.grid[x2][y2], self.grid[x1][y1]
        # Обновляем позиции тайлов
        self.grid[x1][y1].update_position(x1, y1)
        self.grid[x2][y2].update_position(x2, y2)
        return True

    def find_matches(self):
        matches = []
        # Проверяем горизонтальные совпадения
        for y in range(GRID_SIZE):
            x = 0
            while x < GRID_SIZE - 2:
                # Пропускаем пустые ячейки
                if self.grid[x][y] is None:
                    x += 1
                    continue

                color = self.grid[x][y].color
                match_length = 1

                # Проверяем следующие тайлы
                while (x + match_length < GRID_SIZE and
                       self.grid[x + match_length][y] is not None and
                       self.grid[x + match_length][y].color == color):
                    match_length += 1

                if match_length >= 3:
                    matches.append([(x + i, y) for i in range(match_length)])
                    x += match_length  # Пропускаем проверенные тайлы
                else:
                    x += 1

        # Проверяем вертикальные совпадения
        for x in range(GRID_SIZE):
            y = 0
            while y < GRID_SIZE - 2:
                # Пропускаем пустые ячейки
                if self.grid[x][y] is None:
                    y += 1
                    continue

                color = self.grid[x][y].color
                match_length = 1

                # Проверяем следующие тайлы
                while (y + match_length < GRID_SIZE and
                       self.grid[x][y + match_length] is not None and
                       self.grid[x][y + match_length].color == color):
                    match_length += 1

                if match_length >= 3:
                    matches.append([(x, y + i) for i in range(match_length)])
                    y += match_length  # Пропускаем проверенные тайлы
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

            # Определяем направление совпадения (горизонтальное или вертикальное)
            is_horizontal = all(m[1] == first_y for m in match)

            # Обработка спецэффектов
            if match_length == 4:
                # 4 в ряд - уничтожаем всю строку или столбец
                if is_horizontal:
                    # Горизонтальное - уничтожаем строку
                    for x in range(GRID_SIZE):
                        positions_to_clear.add((x, first_y))
                else:
                    # Вертикальное - уничтожаем столбец
                    for y in range(GRID_SIZE):
                        positions_to_clear.add((first_x, y))
                damage += GRID_SIZE * 2  # Больший урон за спецэффект

            elif match_length >= 5:
                # 5+ в ряд - уничтожаем все тайлы этого цвета
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        if self.grid[x][y] is not None and self.grid[x][y].color == color:
                            positions_to_clear.add((x, y))
                damage += GRID_SIZE * GRID_SIZE  # Очень большой урон

            else:
                # Обычное совпадение 3 в ряд
                for pos in match:
                    positions_to_clear.add(pos)
                damage += len(match)

        # Удаляем тайлы в отмеченных позициях
        for x, y in positions_to_clear:
            if self.grid[x][y] is not None:
                self.grid[x][y] = None

        # Наносим урон монстрам
        self.apply_damage(damage)

        # Заполняем пустые места с анимацией
        if positions_to_clear:
            self.fill_empty_spaces()

        return len(positions_to_clear) > 0

    def apply_damage(self, damage):
        if not self.monsters:
            return

        # Наносим урон текущему монстру
        self.monsters[0].hp -= damage

        # Если монстр убит, удаляем его
        if self.monsters[0].hp <= 0:
            self.monsters.pop(0)
            if len(self.monsters) == 0:
                self.win = True

    def fill_empty_spaces(self):
        # Сначала перемещаем существующие тайлы вниз
        for x in range(GRID_SIZE):
            empty_spots = []
            for y in range(GRID_SIZE - 1, -1, -1):
                if self.grid[x][y] is None:
                    empty_spots.append(y)
                elif empty_spots:
                    # Находим самую нижнюю пустую позицию
                    lowest_empty = empty_spots.pop(0)

                    # Перемещаем тайл вниз
                    self.grid[x][lowest_empty] = self.grid[x][y]
                    self.grid[x][y] = None

                    # Настраиваем анимацию падения
                    self.grid[x][lowest_empty].update_position(x, lowest_empty)
                    self.grid[x][lowest_empty].is_falling = True
                    self.grid[x][lowest_empty].fall_speed = 5
                    self.grid[x][lowest_empty].pixel_y = GRID_OFFSET_Y + \
                        y * TILE_SIZE

                    # Добавляем оставшиеся пустые позиции обратно в список
                    empty_spots.append(y)

            # Создаем новые тайлы для оставшихся пустых мест
            for empty_y in empty_spots:
                color = random.choice(COLORS)
                new_tile = Tile(x, empty_y, color)
                new_tile.pixel_y = GRID_OFFSET_Y - TILE_SIZE  # Начинаем выше экрана
                new_tile.is_falling = True
                new_tile.fall_speed = 5
                self.grid[x][empty_y] = new_tile

    def spawn_monster(self):
        hp = self.monster_settings["hp"]
        damage = self.monster_settings["damage"]
        speed = self.monster_settings["speed"]
        self.monsters.append(Monster(hp, damage, speed))

    def update(self):
        if self.game_over or self.win:
            return

        # Обновляем анимации тайлов
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                tile = self.grid[x][y]
                if tile is not None:
                    tile.update()
                    if hasattr(tile, 'effect_timer'):
                        tile.effect_timer += 1
                        if tile.effect_timer > 90:  # Эффект длится 90 кадров
                            tile.special_effect = None
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        # Спавн монстров
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval and (not self.monsters or len(self.monsters) < 3):
            self.spawn_monster()
            self.spawn_timer = 0
            # Уменьшаем интервал спавна с уровнем
            self.spawn_interval = max(1000, SPAWN_INTERVAL - self.moves_left * 20)

        # Обновляем монстров
        for monster in self.monsters[:]:
            if monster is None:
                self.monsters.remove(monster)
                continue
            monster.update()

            # Проверяем, дошел ли монстр до крепости
            if monster.reached_castle():
                if self.castle.take_damage(monster.damage):
                    self.game_over = True
                self.monsters.remove(monster)
