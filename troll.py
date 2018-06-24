import pygame


class Troll():
    def __init__(self, screen):
        """Инициализирует тролля и задает его начальную позицию."""
        self.screen = screen
        # Загрузка изображения тролля и получение прямоугольника.
        self.image = pygame.image.load('images/troll.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый новый тролль появляется в центре экрана.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def blitme(self):
        """Рисует тролля в текущей позиции."""
        self.screen.blit(self.image, self.rect)
