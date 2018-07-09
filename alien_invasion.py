import pygame

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    """Инициализирует игру и создаёт объект экрана"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # Создание кнопки Play.
    play_button = Button(ai_settings, screen, "Play")
    # Создание экземпляров для хранения игровой статистики.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Создание корабля
    ship = Ship(ai_settings, screen)
    # Создание группы для хранения пуль
    bullets = Group()
    # Создание звёзд.
    stars = Group()
    gf.create_many_stars(ai_settings, screen, ship, stars)
    # Создание группы пришельцев.
    aliens = Group()
    # Создание флота пришельцев.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Запуск основного цикла игры.
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship,
                        aliens, bullets)
        # Функция update_screen согласно книге изначально была
        # внутри условия if stats.game_active и нигде позже не
        # было указания перенести вынести её в основыной цикл,
        # а из-за этого при назначении изначального значения
        # флага в False при запуске игры отображался чёрный
        # экран до нажатия наугад кнопки в центре экрана
        gf.update_screen(ai_settings, screen, ship, aliens, bullets,
                         stars, play_button, stats, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens,
                              bullets, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens,
                             bullets)


run_game()
