import sys
import pygame
from bullet import Bullet
from alien import Alien
from stars import Star
from random import randint
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets,
                         stats, aliens, sb):
    """Реагирует на нажатие клавиш."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            write_record(stats)
            sys.exit()
        elif event.key == pygame.K_p:
            start_game(ai_settings, stats, aliens, bullets, screen,
                       ship, sb)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship,
                 aliens, bullets, sb):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y,
                              sb)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets,
                         stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, play_button,
ship, aliens, bullets, mouse_x, mouse_y, sb):
    """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, stats, aliens, bullets, screen,
                   ship, sb)




def start_game(ai_settings, stats, aliens, bullets, screen, ship,
               sb):
    """Запуск новой игры"""
    # Сброс игровых настроек.
    ai_settings.initialize_dynamic_settings()
    # Указатель мыши скрывается.
    pygame.mouse.set_visible(False)
    # Сброс игровой статистики.
    stats.reset_stats()
    stats.game_active = True
    # Очистка списков пришельцев и пуль.
    aliens.empty()
    bullets.empty()
    # Создание нового флота и размещение корабля в центре.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    # Загрузка рекорда
    read_record(stats)
    # Сброс изображений счетов и уровня.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    # Сброс игровой статистики.
    stats.reset_stats()
    stats.game_active = True



def update_screen(ai_settings, screen, ship, aliens, bullets,
                  stars, play_button, stats, sb):
    """Обновляет изображения на экране на экран."""
    # При каждом проходе цикла перерисовывается экран.
    screen.fill(ai_settings.bg_color)
    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    stars.draw(screen)
    aliens.draw(screen)
    # Вывод счета.
    sb.show_score()
    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()
    # Отображение последнего прорисованного экрана.
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    bullets.update()
    # Удаление пуль, вышедших за край экрана.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens,
                                  bullets, stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens,
                                  bullets, stats, sb):
    """Обработка коллизий пуль с пришельцами"""
    # Удаление пришельцев и пуль, участвующих в колллизиях
    collisions = pygame.sprite.groupcollide(bullets, aliens, True,
                                            True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота.
        bullets.empty()
        ai_settings.increase_speed()
        # Увеличение уровня.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут."""
    # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * \
                   row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings,
                                          alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # Создание флота пришельцев.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    # Пришлось перенести сюда опускание флота из change_fleet_direction
    # после добавления collisions в update_bullets, потому что иначе
    # после первого попадания пули все пришельцы улетали вниз
    # сразу после касания краёв экрана
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings)
            for alien in aliens.sprites():
                alien.rect.y += ai_settings.fleet_drop_speed
            break

def change_fleet_direction(ai_settings):
    """Меняет направление флота."""
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, ship, aliens,
                         bullets, sb):
    """Проверяет, достиг ли флот края, после чего
     обновляет позиции всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка коллизий "пришелец-корабль".
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens,
                 bullets, sb)
    # Проверка пришельцев, добравшихся до нижнего края экрана.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens,
                        bullets, sb)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens,
                        bullets, sb):
    """Проверяет, добрались ли пришельцы до нижнего края
    экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении c кораблём.
            ship_hit(ai_settings, stats, screen, ship, aliens,
                     bullets, sb)
            break

def create_star(ai_settings, screen, stars, star_number, row_number):
    """Создает звезду и размещает его в ряду."""
    star = Star(ai_settings, screen)
    star_width = star.rect.width
    star.x = star_width + 4 * star_width * star_number + randint(-32,32)
    star.rect.x = star.x
    star.rect.y = star.rect.height + 4 * star.rect.height * \
                   row_number + randint(-32,32)
    stars.add(star)

def get_number_stars_x(ai_settings, star_width):
    """Вычисляет количество звёзд в ряду."""
    available_space_x = ai_settings.screen_width - 2 * star_width
    number_stars_x = int(available_space_x / (4 * star_width))
    return number_stars_x

def get_number_star_rows(ai_settings, ship_height, star_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height -
                         (3 * star_height) - ship_height)
    number_rows = int(available_space_y / (4 * star_height))
    return number_rows

def create_many_stars(ai_settings, screen, ship, stars):
    """Создает звёзды."""
    # Создание звезды и вычисление количества заёзд в ряду.
    star = Star(ai_settings, screen)
    number_stars_x = get_number_stars_x(ai_settings,
                                          star.rect.width)
    number_rows = get_number_star_rows(ai_settings, ship.rect.height,
                                  star.rect.height)
    # Создание множества звёзд.
    for row_number in range(number_rows):
        for star_number in range(number_stars_x):
            create_star(ai_settings, screen, stars, star_number,
                         row_number)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """Обрабатывает столкновение корабля с пришельцем."""
    if stats.ships_left > 0:
        # Уменьшение ships_left.
        stats.ships_left -= 1
        # Обновление игровой информации.
        sb.prep_ships()

        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def write_record(stats):
    f = open('record.txt', 'w')
    f.write(str(stats.high_score))
    f.close()

def read_record(stats):
    f = open('record.txt', 'r')
    stats.high_score = int(f.read())
    f.close()
