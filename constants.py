# Настройки экрана
SCREEN_WIDTH = 1535
SCREEN_HEIGHT = 800
FPS = 60

# Настройки сетки
GRID_SIZE_X = 24
GRID_SIZE_Y = 8
TILE_SIZE = 50
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 100

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]

# Настройки монстров
BASE_MONSTER_HP = 20
BASE_MONSTER_DAMAGE = 5
BASE_MONSTER_SPEED = 0.5
SPAWN_INTERVAL = 3000  # 3 секунды

# Меню
MENU_BG_COLOR = (50, 50, 80)
BUTTON_COLOR = (70, 70, 120)
BUTTON_HOVER_COLOR = (90, 90, 140)
TEXT_COLOR = (255, 255, 255)

# Добавляем настройки сложности
DIFFICULTY_SETTINGS = {
    "новичок": {
        "monster_hp": 15,
        "monster_damage": 3,
        "monster_speed": 0.3,
        "spawn_interval": 4000,
        "castle_hp": 100,
        "total_monsters": 20,  # Общее количество монстров за игру
        "spawn_acceleration": 50  # Ускорение спавна
    },
    "любитель": {
        "monster_hp": 25,
        "monster_damage": 5,
        "monster_speed": 0.5,
        "spawn_interval": 4000,
        "castle_hp": 100,
        "total_monsters": 30,
        "spawn_acceleration": 70
    },
    "профи": {
        "monster_hp": 40,
        "monster_damage": 8,
        "monster_speed": 0.7,
        "spawn_interval": 4000,
        "castle_hp": 100,
        "total_monsters": 40,
        "spawn_acceleration": 100
    }
}

MIN_CASTLE_HP = 0
TILE_FALL_SPEED = 0.5  # Можно регулировать скорость анимации
SHADOW_COLOR = (100, 100, 100, 150)  # Цвет тени для тайлов
BRIDGE_WIDTH = SCREEN_WIDTH - 200  # Ширина моста
BRIDGE_HEIGHT = 150  # Высота моста
BRIDGE_X = 0  # Позиция моста по X
BRIDGE_Y = 650  # Позиция моста по Y (выше игрового поля)
MONSTER_PATH_Y = BRIDGE_Y + BRIDGE_HEIGHT // 2 - 20  # Центр моста для движения монстров
