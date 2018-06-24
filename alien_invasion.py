import pygame

from settings import Settings
from ship import Ship
from troll import Troll
import game_functions as gf


def run_game():
    """Инициализирует игру и создаёт объект экрана"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Создание корабля
    ship = Ship(screen)
    troll = Troll(screen)

    # Запуск основного цикла игры
    while True:
        # Запуск основного цикла игры.
        gf.check_events(ship)
        ship.update()
        gf.update_screen(ai_settings, screen, ship, troll)


run_game()
