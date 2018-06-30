import pygame

from settings import Settings
from ship import Ship
from troll import Troll
from pygame.sprite import Group
import game_functions as gf


def run_game():
    """Инициализирует игру и создаёт объект экрана"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Создание корабля
    ship = Ship(ai_settings, screen)
    troll = Troll(screen)
    # Создание группы для хранения пуль
    bullets = Group()

    # Запуск основного цикла игры.
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_screen(ai_settings, screen, ship, troll, bullets)


run_game( )
