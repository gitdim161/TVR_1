from src.model.monster import Monster
from src.utils.constants import DIFFICULTY_SETTINGS


class MonsterManager:
    def __init__(self, difficulty):
        """Инициализирует менеджер монстров с настройками сложности.

        Args:
            difficulty (str): Уровень сложности ('новичок', 'любитель', 'профи').
        """
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.monsters = []
        self.initial_spawn_interval = settings["spawn_interval"]
        self.spawn_interval = settings["spawn_interval"]
        self.spawn_acceleration = settings["spawn_acceleration"]
        self.total_monsters = settings["total_monsters"]
        self.monsters_spawned = 0
        self.spawn_timer = 0
        self.monster_settings = {
            "hp": settings["monster_hp"],
            "damage": settings["monster_damage"],
            "speed": settings["monster_speed"]
        }

    def spawn_monster(self):
        """Создает нового монстра, если это возможно.

        Returns:
            bool: True, если монстр был создан, иначе False.
        """
        if (self.monsters_spawned < self.total_monsters and
                len(self.monsters) < 5):
            hp = self.monster_settings["hp"]
            damage = self.monster_settings["damage"]
            speed = self.monster_settings["speed"]
            self.monsters.append(Monster(hp, damage, speed))
            self.monsters_spawned += 1
            return True
        return False

    def update(self, delta_time, game_time, castle):
        """Обновляет состояние менеджера монстров.

        Args:
            delta_time (int): Время, прошедшее с последнего обновления.
            game_time (int): Общее время игры.
            castle (Castle): Объект крепости.
        Returns:
            bool: True, если крепость уничтожена, иначе False.
        """
        self.spawn_interval = max(500, self.initial_spawn_interval -
                                  (game_time // 1000) * self.spawn_acceleration)

        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_monster()
            self.spawn_timer = 0

        for monster in self.monsters[:]:
            monster.update()
            if monster.reached_castle():
                if castle.take_damage(monster.damage):
                    return True  # Game over
                self.monsters.remove(monster)

        return False  # Game continues

    def apply_damage(self, damage):
        """Наносит урон первому монстру в списке.

        Args:
            damage (int): Количество наносимого урона.
        Returns:
            bool: True, если все монстры побеждены, иначе False.
        """
        if not self.monsters:
            return False

        self.monsters[0].hp -= damage
        if self.monsters[0].hp <= 0:
            self.monsters.pop(0)
            if not self.monsters and self.monsters_spawned >= self.total_monsters:
                return True  # Win
        return False  # Continue
