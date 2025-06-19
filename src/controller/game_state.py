import pygame
from src.utils.constants import BLACK, RED, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_COLOR, TEXT_COLOR, BUTTON_HOVER_COLOR


class GameState:
    def __init__(self, difficulty="любитель"):
        """Инициализирует состояние игры.

        Args:
            difficulty (str): Уровень сложности ('новичок', 'любитель', 'профи').
        """
        self.difficulty = difficulty
        self.selected_tile = None
        self.game_over = False
        self.win = False
        self.game_time = 0
        self.last_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 36)
        self.menu_button = pygame.Rect(50, 10, 100, 40)
        self.paused = False

        button_width, button_height = 200, 50
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        self.pause_buttons = [
            pygame.Rect(center_x, 250, button_width, button_height),  # Продолжить
            pygame.Rect(center_x, 320, button_width, button_height),  # Рестарт
            pygame.Rect(center_x, 390, button_width, button_height)   # Выход
        ]

    def update_time(self):
        """Обновляет игровое время.

        Returns:
            int: Время, прошедшее с последнего обновления (в миллисекундах).
        """
        if self.paused:
            return 0

        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        self.game_time += delta_time
        return delta_time

    def draw_game_info(self, surface, castle):
        """Отрисовывает игровую информацию (здоровье крепости, кнопку меню).

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
            castle (Castle): Объект крепости.
        """

        pygame.draw.rect(surface, BUTTON_COLOR, self.menu_button)
        menu_text = self.font.render("Меню", True, TEXT_COLOR)
        surface.blit(menu_text, (self.menu_button.x + 20, self.menu_button.y + 10))

    def draw_game_over(self, surface):
        """Отрисовывает сообщение о конце игры.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        if self.game_over:
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА!", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    def draw_win(self, surface):
        """Отрисовывает сообщение о победе.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        if self.win:
            win_text = self.font.render('ПОБЕДА!', True, GREEN)
            restart_text = self.font.render('Нажмите R для рестарта', True, BLACK)
            surface.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))

    def draw_pause(self, surface):
        """Отрисовывает меню паузы.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        if self.paused:
            # Затемнение фона
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))

            # Заголовок
            pause_text = self.big_font.render("ПАУЗА", True, TEXT_COLOR)
            surface.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 150))

            # Кнопки
            button_labels = ["Продолжить", "Рестарт", "Выход"]
            mouse_pos = pygame.mouse.get_pos()

            for i, button in enumerate(self.pause_buttons):
                is_hovered = button.collidepoint(mouse_pos)
                color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR

                pygame.draw.rect(surface, color, button, border_radius=10)
                pygame.draw.rect(surface, BLACK, button, 2, border_radius=10)

                label = self.font.render(button_labels[i], True, TEXT_COLOR)
                surface.blit(label, (button.x + button.width // 2 - label.get_width() // 2,
                             button.y + button.height // 2 - label.get_height() // 2))

    def handle_pause_click(self, pos):
        """Обрабатывает клики в меню паузы.

        Args:
            pos (tuple): Координаты клика (x, y).
        Returns:
            str or None: Действие ("continue", "restart", "exit") или None.
        """
        if not self.paused:
            return None

        for i, button in enumerate(self.pause_buttons):
            if button.collidepoint(pos):
                if i == 0:  # Продолжить
                    return "continue"
                elif i == 1:  # Рестарт
                    return "restart"
                elif i == 2:  # Выход
                    return "exit"
        return None
