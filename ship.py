import pygame

class Ship:
    '''ship model. The player controls the ship
       and it is spawned in the main game method
    '''

    def __init__(self, settings, screen):
        '''init the ship and its starting position'''

        # Get the screen surface onto which the ship object
        # will be rendered
        self.screen   = screen
        # Settings to adjust things of the ship such as speed
        self.speed    = settings.ship_speed_factor

        # Load the ship image and get its rectangular representation
        self.image       = pygame.image.load('images/galaga_ship.bmp')
        self.rect        = self.image.get_rect()

        # Set the starting pos for the ship at the bottom of the screen center
        self.screen_rect  = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom  = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        # This is to overcome the fact that rect
        # attributes can only store integers
        # The values below are used instead by
        # update() to adjust the ship's movement
        self.x_center = float(self.rect.centerx)
        self.y_center = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left  = False
        self.moving_up    = False
        self.moving_down  = False

    def blitme(self):
        '''Draw the ship's img at it's rectangle's current position
           Called in game_functions.update_screen() method
        '''
        self.screen.blit(self.image, self.rect)

    def adjust_ship_speed(self, speed):
        self.speed = speed

    def center_ship(self):
        '''Set the ship back to its starting position'''
        self.center = self.screen_rect.centerx

    def update(self):
        '''update the location of the img's rectangle.
           The img will trace to the rectangle object
           through the call to blitme() (blit is short for
           "BLock Image Transfer"). That is to say the img
           will be moved to the location of the rectangle obj

           This function is called in the game's main loop(game.run_game())
           '''
        # Using if as opposed to elif is the
        # preferred way to handle conditional blocks.
        # This allows for smooth movement when the user
        # simultaneously holds down multiple keys

        # Update the ship's center value, not rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x_center += self.speed
        if self.moving_left and self.rect.left > 0:
            self.x_center -= self.speed
        # Make sure the player doesn't go more than a quarter of the screen
        # previously: self.moving_up and self.rect.top > 0
        if self.moving_up and self.rect.top > self.screen_rect.centery * 1.5:
            self.y_center -= self.speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y_center += self.speed

        # Update the center of rec
        self.rect.centerx = self.x_center
        self.rect.centery = self.y_center
