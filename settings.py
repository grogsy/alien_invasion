'''Various game settings'''
from random import uniform
BLACK = (0, 0, 0)
GREY  = (230, 230, 230)
WHITE = (255, 255, 255)

class Settings():
    '''Game settings'''

    def __init__(self):
        # Game screen settings
        self.screen_width  = 1200
        self.screen_height = 900
        self.bg_color      = BLACK

        # Ship settings
        #self.ship_speed_factor = 1.75
        self.ship_limit        = 3

        # Bullet settings
        #self.bullet_speed_factor = 3
        self.bullet_width        = 3
        self.bullet_height       = 15
        self.bullet_color        = WHITE
        self.available_bullets   = 3

        # Star settings
        self.star_height = 1
        self.star_width  = 1
        self.star_color  = WHITE
        self.star_speed  = .5
        self.star_limit  = 450

        # Alien settings
        self.fleet_direction    = 1     # 1 means moving right; -1 means left
        #self.alien_bullet_speed = uniform(.5, 2.25)

        # How quickly the game pace changes
        self.scale        = 1.075
        self.bullet_scale = 1.0725
        self.point_scale  = 1.25

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''initialize settings that change throughout the game'''
        self.ship_speed_factor   = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor  = 1
        self.fleet_direction     = 1
        self.alien_points        = 50
        self.fleet_drop_speed    = 20
        # very magicky number to produce random alien fire rate
        self.alien_fire_rate     = 247

    def increase_speed(self, level):
        '''Increase speed settings'''
        # Increase player stats every level
        # Increase drop speed every 3 levels
        if level % 3 == 0:
            self.fleet_drop_speed    *= self.scale

        elif level % 2 == 0:
            self.ship_speed_factor   *= self.scale
            self.bullet_speed_factor *= self.bullet_scale

        self.alien_fire_rate -= 10
        self.alien_speed_factor  *= self.scale
        self.alien_points = int(self.alien_points * self.point_scale)

