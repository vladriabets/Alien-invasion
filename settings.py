class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_color = (0, 0, 230)
        # Настройки корабля
        self.ship_speed_factor = 1.5