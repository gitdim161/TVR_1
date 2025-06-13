import pygame
from constants import BLACK, RED, GREEN, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_COLOR, TEXT_COLOR


class GameState:
    def __init__(self, difficulty="любитель"):
        self.difficulty = difficulty
        self.selected_tile = None
        self.game_over = False
        self.win = False
        self.game_time = 0
        self.last_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('Arial', 24)
        self.menu_button = pygame.Rect(50, 10, 100, 40)

    def update_time(self):
        current_time = pygame.time.get_ticks()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        self.game_time += delta_time
        return delta_time

    def draw_game_info(self, surface, castle):
        castle_hp_text = self.font.render(
            f"Крепость: {castle.hp}/{castle.max_hp}", True, BLACK)
        surface.blit(castle_hp_text, (SCREEN_WIDTH - 200, 10))

        pygame.draw.rect(surface, BUTTON_COLOR, self.menu_button)
        menu_text = self.font.render("Меню", True, TEXT_COLOR)
        surface.blit(menu_text, (self.menu_button.x + 20, self.menu_button.y + 10))

    def draw_game_over(self, surface):
        if self.game_over:
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА!", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    def draw_win(self, surface):
        if self.win:
            win_text = self.font.render('ПОБЕДА!', True, GREEN)
            restart_text = self.font.render('Нажмите R для рестарта', True, BLACK)
            surface.blit(win_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
            surface.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
