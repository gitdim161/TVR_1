import pygame
import sys
from src.logic.game import Game
from src.view.menu import Menu
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, FPS


def handle_events(events, menu, game):
    """Централизованный обработчик событий"""
    for event in events:
        if event.type == pygame.QUIT:
            return "quit"

        if game:
            # Обработка событий во время игры
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = game.handle_click(event.pos)
                if result in ("restart", "exit"):
                    return result

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game.state.game_over or game.state.win):
                    return "restart"
        else:
            # Обработка событий в меню
            action = menu.handle_event(event)
            if action in ("start", "exit"):
                return action

    return None


def main():
    """Основная функция игры"""
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Три в ряд + Tower Defense")
    clock = pygame.time.Clock()

    # Настройка музыки
    pygame.mixer.music.load(r'assets\sounds\menu.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    menu = Menu(screen)
    game = None
    running = True

    while running:
        events = pygame.event.get()
        action = handle_events(events, menu, game)

        # Обработка действий
        if action == "quit":
            running = False
        elif action == "start":
            game = Game(menu.selected_difficulty)
        elif action == "exit":
            running = False
        elif action == "restart":
            game = Game(menu.selected_difficulty)

        # Отрисовка
        screen.fill(WHITE)
        if game:
            game.update()
            game.draw(screen)
        else:
            menu.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
