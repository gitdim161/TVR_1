import pygame
import random
from tile import Tile
from monster import Monster
from castle import Castle
from constants import GRID_SIZE, SPAWN_INTERVAL, COLORS, TILE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, SCREEN_WIDTH, BLACK, RED, WHITE, DIFFICULTY_SETTINGS, YELLOW, SCREEN_HEIGHT, MONSTER_PATH_Y, BUTTON_COLOR, TEXT_COLOR, WIN_SCORE, GREEN, SHADOW_COLOR


class Game:
    def __init__(self, difficulty="любитель"):
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.grid = []
        self.selected_tile = None
        self.score = 0
        self.level = 1
        self.monsters = []
        self.castle = Castle(settings["castle_hp"])
        self.spawn_interval = settings["spawn_interval"]
        self.monster_settings = {
            "hp": settings["monster_hp"],
            "damage": settings["monster_damage"],
            "speed": settings["monster_speed"]
        }
        self.spawn_timer = 0
        self.last_time = pygame.time.get_ticks()
        self.game_over = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.menu_button = pygame.Rect(SCREEN_WIDTH - 120, 500, 100, 40)
        self.initialize_grid()
        self.win = False

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
        for column in self.grid:
            for tile in column:
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
        pygame.draw.rect(surface, RED, (0, MONSTER_PATH_Y - 20, SCREEN_WIDTH, 60))
        pygame.draw.rect(surface, BLACK, (0, MONSTER_PATH_Y - 20, SCREEN_WIDTH, 60), 2)

        pygame.draw.rect(surface, (150, 150, 150), (0, MONSTER_PATH_Y - 15, SCREEN_WIDTH, 50))
        pygame.draw.lines(surface, YELLOW, False, [(0, MONSTER_PATH_Y + 10), (SCREEN_WIDTH, MONSTER_PATH_Y + 10)], 3)
        shadow_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, SHADOW_COLOR, (0, 0, TILE_SIZE, TILE_SIZE), border_radius=5)
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
        score_text = font.render(f"Очки: {self.score}", True, BLACK)
        level_text = font.render(f"Уровень: {self.level}", True, BLACK)
        castle_hp = max(0, self.castle.hp)
        castle_hp_text = font.render(
            f"Крепость: {self.castle.hp}/{self.castle.max_hp}", True, BLACK)

        surface.blit(score_text, (500, 500))
        surface.blit(level_text, (500, 540))
        surface.blit(castle_hp_text, (SCREEN_WIDTH - 200, 10))

        if self.game_over:
            game_over_text = font.render("ИГРА ОКОНЧЕНА!", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH //
                         2 - 100, SCREEN_HEIGHT // 2))

        pygame.draw.rect(surface, BUTTON_COLOR, self.menu_button)
        menu_text = self.font.render("Меню", True, TEXT_COLOR)
        surface.blit(menu_text, (self.menu_button.x + 20, self.menu_button.y + 10))

        if self.win:  # Добавляем сообщение о победе
            win_text = self.font.render(f"ПОБЕДА! Набрано {self.score} очков!", True, GREEN)
            restart_text = self.font.render("Нажмите R для рестарта", True, BLACK)
            surface.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))

    def handle_click(self, pos):
        if self.menu_button.collidepoint(pos):
            return "menu"
        if self.game_over or self.win:
            return

        # Проверяем условие победы
        if self.score >= WIN_SCORE:
            self.win = True
            return
        x = (pos[0] - GRID_OFFSET_X) // TILE_SIZE
        y = (pos[1] - GRID_OFFSET_Y) // TILE_SIZE

        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            if self.grid[x][y] is None:  # Проверка на пустую ячейку
                return
            if self.selected_tile is None:
                self.selected_tile = (x, y)
            else:
                # Проверяем, соседние ли тайлы
                prev_x, prev_y = self.selected_tile
                if (abs(x - prev_x) == 1 and y == prev_y) or (abs(y - prev_y) == 1 and x == prev_x):
                    # Меняем тайлы местами
                    self.swap_tiles((prev_x, prev_y), (x, y))

                    # Проверяем, есть ли совпадения
                    if not self.find_matches():
                        # Если нет, меняем обратно
                        self.swap_tiles((x, y), (prev_x, prev_y))
                    else:
                        # Если есть, удаляем совпадения и обновляем поле
                        self.remove_matches()
                        self.fill_empty_spaces()

                        # Продолжаем проверять совпадения после заполнения
                        while self.find_matches():
                            self.remove_matches()
                            self.fill_empty_spaces()

                self.selected_tile = None

    def swap_tiles(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        # Проверка на существование тайлов
        if not (0 <= x1 < GRID_SIZE and 0 <= y1 < GRID_SIZE and
                0 <= x2 < GRID_SIZE and 0 <= y2 < GRID_SIZE):
            return

        if self.grid[x1][y1] is None or self.grid[x2][y2] is None:
            return
        # Меняем тайлы местами в сетке
        self.grid[x1][y1], self.grid[x2][y2] = self.grid[x2][y2], self.grid[x1][y1]
        # Обновляем позиции тайлов
        self.grid[x1][y1].update_position(x1, y1)
        self.grid[x2][y2].update_position(x2, y2)

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
        special_effects = []

        for match in matches:
            # Проверяем, нужно ли применить спецэффекты
            if len(match) >= 5:
                # Удаляем все тайлы этого цвета
                color = self.grid[match[0][0]][match[0][1]].color
                special_effects.append(('color', color))
                damage += GRID_SIZE * GRID_SIZE  # Большой урон за спецэффект
            elif len(match) >= 4:
                # Удаляем строку или столбец
                if match[0][0] == match[1][0]:  # Вертикальный (столбец)
                    special_effects.append(('column', match[0][0]))
                else:  # Горизонтальный (строка)
                    special_effects.append(('row', match[0][1]))
                damage += GRID_SIZE  # Средний урон за спецэффект

            # Увеличиваем урон за каждый тайл
            damage += len(match)

        # Применяем спецэффекты
        for effect in special_effects:
            if effect[0] == 'color':
                color = effect[1]
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        if self.grid[x][y].color == color:
                            self.grid[x][y] = None
            elif effect[0] == 'column':
                x = effect[1]
                for y in range(GRID_SIZE):
                    self.grid[x][y] = None
            elif effect[0] == 'row':
                y = effect[1]
                for x in range(GRID_SIZE):
                    self.grid[x][y] = None

        # Удаляем совпадения
        for match in matches:
            for x, y in match:
                # Если еще не удален спецэффектом
                if self.grid[x][y] is not None:
                    self.grid[x][y] = None

        # Наносим урон монстрам
        self.apply_damage(damage)

        return len(matches) > 0

    def apply_damage(self, damage):
        if not self.monsters:
            return

        # Наносим урон текущему монстру
        self.monsters[0].hp -= damage
        self.score += damage

        if self.score >= WIN_SCORE:
            self.win = True
            return

        # Если монстр убит, удаляем его
        if self.monsters[0].hp <= 0:
            self.monsters.pop(0)

            # Если больше нет монстров, повышаем уровень
            if not self.monsters:
                self.level += 1

    def fill_empty_spaces(self):
        for x in range(GRID_SIZE):
            empty_spots = []
            for y in range(GRID_SIZE - 1, -1, -1):
                if self.grid[x][y] is None:
                    empty_spots.append(y)
                elif empty_spots and isinstance(self.grid[x][y], Tile):
                    # Перемещаем тайл вниз
                    lowest_empty = empty_spots.pop(0)
                    self.grid[x][lowest_empty] = self.grid[x][y]
                    self.grid[x][y] = None

                    # Настраиваем анимацию падения
                    self.grid[x][lowest_empty].is_falling = True
                    self.grid[x][lowest_empty].fall_speed = 15
                    self.grid[x][lowest_empty].update_position(x, lowest_empty)

            # Создаем новые тайлы сверху
            for empty_y in empty_spots:
                color = random.choice(COLORS)
                new_tile = Tile(x, empty_y, color)
                new_tile.pixel_y = -TILE_SIZE  # Начинаем падение сверху
                new_tile.is_falling = True
                new_tile.fall_speed = 15
                new_tile.update_position(x, empty_y)
                self.grid[x][empty_y] = new_tile

    def spawn_monster(self):
        hp = self.monster_settings["hp"] + self.level * 5
        damage = self.monster_settings["damage"] + self.level * 1
        speed = self.monster_settings["speed"] + self.level * 0.05
        self.monsters.append(Monster(hp, damage, speed))

    def update(self):
        if self.game_over or self.win:
            return

        # Обновляем анимации тайлов
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                tile = self.grid[x][y]
                if tile is not None and hasattr(tile, 'update'):
                    tile.update()
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        # Спавн монстров
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval and (not self.monsters or len(self.monsters) < 3):
            self.spawn_monster()
            self.spawn_timer = 0
            # Уменьшаем интервал спавна с уровнем
            self.spawn_interval = max(1000, SPAWN_INTERVAL - self.level * 200)

        # Обновляем монстров
        for monster in self.monsters:
            monster.update()

            # Проверяем, дошел ли монстр до крепости
            if monster.reached_castle():
                if self.castle.take_damage(monster.damage):
                    self.game_over = True
                self.monsters.remove(monster)

        if self.score >= WIN_SCORE:
            self.win = True
