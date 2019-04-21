import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''Class to represent a single alient in the fleet'''

    def __init__(self, settings, screen):
        '''Init the alien obj and set its starting pos'''
        super().__init__()
        self.screen   = screen
        self.settings = settings

        # Load the img and set its rect representation
        self.image = pygame.image.load('images/space_alien.bmp')
        self.rect  = self.image.get_rect()

        # Start each alien spawned at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact pos
        self.x = float(self.rect.x)

    def check_edges(self):
        '''Return true if alien is at the edge of the screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        '''Move the alien right or left'''
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        '''Draw the alien at its current pos
           Method is called in game_functions.update_screen()
        '''
        self.screen.blit(self.image, self.rect)
