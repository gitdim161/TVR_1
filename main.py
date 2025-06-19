import pygame
import sys
from src.controller.game import Game
from src.view.menu import Menu
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, FPS


def main():
    """Главная функция, запускающая игру."""
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Три в ряд + Tower Defense")
    clock = pygame.time.Clock()

    pygame.mixer.music.load(r'assets\sounds\menu.mp3')
    pygame.mixer.music.set_volume(0.5)  # Громкость от 0 до 1
    pygame.mixer.music.play(-1)  # -1 означает зацикливание
    menu = Menu(screen)
    game = None

    running = True
    while running:
        try:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    running = False

            screen.fill(WHITE)

            # Отрисовка
            if game:
                game.update()
                game.draw(screen)

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        result = game.handle_click(event.pos)
                        if result == "restart":
                            game = Game(game.difficulty)
                        elif result == "exit":
                            game = None
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r and game.state.game_over or game.state.win:
                            game = Game(menu.selected_difficulty)
            else:
                menu.draw()
                action = menu.handle_event(event)
                for event in events:
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
