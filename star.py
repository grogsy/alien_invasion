'''Star background'''
import random

import pygame
from pygame.sprite import Sprite


class Star(Sprite):
    '''Just a dot on a screen that appears randomly in places'''

    def __init__(self, settings, screen,):
        super().__init__()
        self.settings = settings
        self.screen   = screen
        self.color    = settings.star_color
        self.speed    = settings.star_speed

        self.rect        = pygame.Rect(0, 0, settings.star_height, settings.star_width)
        self.screen_rect = screen.get_rect()

        # Starting position
        starting_positions = (
            (0, random.choice(range(self.settings.screen_height))),
            (random.choice(range(self.settings.screen_width)), 0)
        )
        x_start, y_start = random.choice(starting_positions)


        self.rect.x  = x_start
        self.rect.y  = y_start

        # Change in position
        self.dx = float(self.rect.x)
        self.dy = float(self.rect.y)

    def update(self):
        '''Put the star in a random position'''
        self.dx += self.speed
        self.dy += self.speed

        # update rect pos
        self.rect.x = self.dx
        self.rect.y = self.dy
        # kill sprites that fall off screen surafce
        if not self.screen_rect.contains(self):
            self.kill()

    def draw_star(self):
        '''Draw star to the screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)
