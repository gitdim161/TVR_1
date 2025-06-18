import pygame
import sys
from game import Game
from menu import Menu
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, FPS


def main():
    """Главная функция, запускающая игру."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Три в ряд + Tower Defense")
    clock = pygame.time.Clock()

    menu = Menu(screen)
    game = None

    running = True
    while running:
        try:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(WHITE)

            # Отрисовка
            if game:
                game.update()
                game.draw(screen)

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        result = game.handle_click(event.pos)
                        if result == "menu":
                            game = None
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r and game.game_over or game.win:
                            game = Game(menu.selected_difficulty)
            else:
                menu.draw()
                action = menu.handle_event(event)
                if action == "start":
                    game = Game(menu.selected_difficulty)
                elif action == "exit":
                    running = False

            pygame.display.flip()
            clock.tick(FPS)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
