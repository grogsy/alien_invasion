import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''Class which manages projectiles fired by the ship
       Bullets are spawned in the call to game_functions.fire_bullet() method
    '''

    def __init__(self, settings, screen, ship):
        '''Bullets are created at the ships current pos'''
        super().__init__()
        self.screen = screen
        self.w = settings.bullet_width
        self.h = settings.bullet_height

        # Create a bullet rect at (0, 0) and then set the pos
        # on the ship. No image loaded for the projectile
        # so we use pygame.Rect() to build one from scratch
        self.rect         = pygame.Rect(0, 0, self.w, self.h)

        # Now set the bullet pos to the ship
        self.rect.centerx = ship.rect.centerx
        self.rect.top     = ship.rect.top

        # Store the bullet's position as a decimal
        # and store the bullet's motion as a float
        self.y = float(self.rect.y)

        # Bullet color and speed
        self.color = settings.bullet_color
        self.speed = settings.bullet_speed_factor

    def update(self):
        '''Move the bullet up the screen.
           Called in game_functions.update_bullets() method
        '''
        # Update the decimal position of the bullet
        self.y -= self.speed
        # Then update the rectangle
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw the bullet to the screen.
           Called in game_functions.update_screen() method
        '''
        pygame.draw.rect(self.screen, self.color, self.rect)


class AlienBullet(Sprite):
    '''Bullets which aliens fire'''
    def __init__(self, settings, screen, alien, speed):
        super().__init__()
        self.screen = screen
        self.w = settings.bullet_width
        self.h = settings.bullet_height-1
        self.screen_rect = screen.get_rect()

        self.rect = pygame.Rect(0, 0, self.w, self.h)

        self.rect.centerx = alien.rect.centerx
        self.rect.bottom  = alien.rect.bottom

        self.y = float(self.rect.y)

        self.color = (0, 255, 0)
        self.speed = speed

    def update(self):
        self.y += self.speed
        self.rect.y =  self.y
        if not self.screen_rect.contains(self):
            self.kill()

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
