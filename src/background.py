import pygame
from pygame.sprite import Sprite

class Background(Sprite):
    """Parent background class for Blast."""
    def __init__(self, screen):
        """Init background and starting position."""
        super(Background, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('../images/background.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
    
    def blitme(self):
        """Draw background"""
        self.screen.blit(self.image, self.rect)