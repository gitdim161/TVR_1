import pygame
from src.utils.constants import BUTTON_COLOR, BUTTON_HOVER_COLOR, BLACK, TEXT_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT


class Button:
    def __init__(self, x, y, width, height, text, action):
        """Инициализирует кнопку меню.

        Args:
            x (int): Координата X.
            y (int): Координата Y.
            width (int): Ширина кнопки.
            height (int): Высота кнопки.
            text (str): Текст кнопки.
            action (str): Действие кнопки.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 30)

    def draw(self, surface):
        """Отрисовывает кнопку.

        Args:
            surface (pygame.Surface): Поверхность для отрисовки.
        """
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)

        text_surf = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        """Проверяет, был ли клик по кнопке.

        Args:
            pos (tuple): Координаты клика (x, y).
        Returns:
            bool: True если клик был по кнопке, иначе False.
        """
        return self.rect.collidepoint(pos)


class Menu:
    def __init__(self, screen):
        """Инициализирует меню.

        Args:
            screen (pygame.Surface): Экран для отрисовки.
        """
        self.screen = screen
        self.buttons = []
        self.difficulty_buttons = []
        self.selected_difficulty = "любитель"  # По умолчанию
        self.show_difficulty = False
        self.background = pygame.image.load(r'assets\images\menu.jpg').convert()
        # Масштабируем под размер экрана
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.music_on = True
        self.create_buttons()

    def create_buttons(self):
        """Создает кнопки меню."""
        width, height = 200, 50
        center_x = SCREEN_WIDTH // 2 - width // 2
        # Основные кнопки
        self.buttons = [
            Button(center_x, 250, width, height, "Начать игру", "start"),
            Button(center_x, 320, width, height, "Сложность", "difficulty"),
            Button(center_x, 390, width, height,
                   "Музыка: Вкл" if self.music_on else "Музыка: Выкл", "toggle_music"),
            Button(center_x, 450, width, height, "Выход", "exit")
        ]
        # Кнопки выбора сложности
        self.difficulty_buttons = [
            Button(center_x, 150, width, height, "Новичок", "novice"),
            Button(center_x, 220, width, height, "Любитель", "amateur"),
            Button(center_x, 290, width, height, "Профи", "professional"),
            Button(center_x, 360, width, height, "Назад", "back")
        ]

    def handle_event(self, event):
        """Обрабатывает события меню.

        Args:
            event (pygame.Event): Событие для обработки.

        Returns:
            str or None: Действие, связанное с нажатой кнопкой, или None.
        """
        if event.type == pygame.MOUSEMOTION:
            buttons = self.difficulty_buttons if self.show_difficulty else self.buttons
            for button in buttons:
                button.is_hovered = button.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            buttons = self.difficulty_buttons if self.show_difficulty else self.buttons
            for button in buttons:
                if button.is_hovered:
                    if button.action == "toggle_music":
                        self.music_on = not self.music_on
                        button.text = "Музыка: Вкл" if self.music_on else "Музыка: Выкл"
                        pygame.mixer.music.set_volume(0.5 if self.music_on else 0)
                        return None
                    if button.action == "difficulty":
                        self.show_difficulty = True
                        return None
                    elif button.action == "back":
                        self.show_difficulty = False
                        return None
                    elif button.action in ("novice", "amateur", "professional"):
                        self.selected_difficulty = {
                            "novice": "новичок",
                            "amateur": "любитель",
                            "professional": "профи"
                        }[button.action]
                        self.show_difficulty = False
                    return button.action
        return None

    def draw(self):
        '''Отрисовка меню'''
        self.screen.blit(self.background, (0, 0))

        # Затемнение фона для лучшей читаемости текста
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Полупрозрачный чёрный
        self.screen.blit(overlay, (0, 0))

        # Заголовок
        title_font = pygame.font.SysFont('Arial', 50, bold=True)
        title = title_font.render("Три в ряд: Защита", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title, title_rect)

        # Текущая сложность
        if not self.show_difficulty:
            diff_font = pygame.font.SysFont('Arial', 30)
            diff_text = diff_font.render(
                f"Сложность: {self.selected_difficulty}", True, TEXT_COLOR)
            self.screen.blit(diff_text, (SCREEN_WIDTH//2 -
                             diff_text.get_width()//2, 500))

        # Рисуем активные кнопки
        buttons = self.difficulty_buttons if self.show_difficulty else self.buttons
        for button in buttons:
            button.draw(self.screen)
