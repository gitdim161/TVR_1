import pygame
from src.utils.constants import (
    BLACK, RED, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT,
    BUTTON_COLOR, TEXT_COLOR, BUTTON_HOVER_COLOR
)


class GameRenderer:
    def __init__(self, game_state, castle):
        self.game_state = game_state
        self.castle = castle
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 36)

    def draw_game_info(self, surface):
        """Отрисовывает игровую информацию (здоровье крепости, кнопку меню).

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        pygame.draw.rect(surface, BUTTON_COLOR, self.game_state.menu_button)
        menu_text = self.font.render("Меню", True, TEXT_COLOR)
        surface.blit(menu_text, (self.game_state.menu_button.x + 20, self.game_state.menu_button.y + 10))

    def draw_game_over(self, surface):
        """Отрисовывает сообщение о поражении.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        if self.game_state.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    def draw_win(self, surface):
        """Отрисовывает сообщение о победе.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        if self.game_state.win:
            win_text = self.font.render('ПОБЕДА!', True, GREEN)
            restart_text = self.font.render('Нажмите R для рестарта', True, BLACK)
            surface.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))

    def draw_pause(self, surface):
        """Отрисовывает меню паузы.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        if self.game_state.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))

            pause_text = self.big_font.render("ПАУЗА", True, TEXT_COLOR)
            surface.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 150))

            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.game_state.pause_buttons):
                is_hovered = button.collidepoint(mouse_pos)
                color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
                pygame.draw.rect(surface, color, button, border_radius=10)
                pygame.draw.rect(surface, BLACK, button, 2, border_radius=10)

                label = self.font.render(["Продолжить", "Рестарт", "Выход"][i], True, TEXT_COLOR)
                surface.blit(label, (button.centerx - label.get_width() // 2, button.centery - label.get_height() // 2))
