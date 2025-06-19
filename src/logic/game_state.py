import pygame
from src.utils.constants import SCREEN_WIDTH


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
        self.paused = False
        self.game_time = 0
        self.last_time = pygame.time.get_ticks()
        self.menu_button = pygame.Rect(50, 10, 100, 40)
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
