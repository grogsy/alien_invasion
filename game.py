'''Main program to run game'''
from collections import namedtuple

import pygame
import pygame.time
from pygame.sprite import Group    # Third Party

from button import Button
from game_functions import (check_events, create_alien_fleet, update_bullets,
                            update_screen, update_aliens)
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship              # User-defined
from star import Star
from stats import GameStats


def run_game():
    '''main toplevel function for the game'''
    # Init game, settings and create a screen object
    pygame.init()
    settings = Settings()
    screen_x, screen_y = settings.screen_width, settings.screen_height
    screen = pygame.display.set_mode((screen_x, screen_y))
    stats  = GameStats(settings)
    pygame.display.set_caption("Alien Invasion")

    # Create containers for application objects so arg passing to functions isn't bloated
    MetaObjs = namedtuple('MetaObj', 'settings screen stats buttons scoreboard')
    GameObjs = namedtuple('GameObj', 'ship bullets aliens stars alien_bullets')
    Buttons = namedtuple('Buttons', 'play pause')

    # Prep up buttons
    buttons = Buttons(
        play=Button(settings, screen, 'Click to Start'),
        pause=Button(settings, screen, 'Paused')
    )

    meta_objs = MetaObjs(
        settings=settings,
        screen=pygame.display.set_mode((screen_x, screen_y)),
        stats=stats,
        buttons=buttons,
        scoreboard=Scoreboard(settings, screen, stats)
    )

    game_objs = GameObjs(
        ship=Ship(settings, screen),
        bullets=Group(), stars=Group(), aliens=Group(), alien_bullets=Group()
    )

    # Create first alien fleet
    create_alien_fleet(meta_objs, game_objs)

    # Main game loop
    while True:
        game_objs.stars.add(Star(meta_objs.settings, meta_objs.screen))
        check_events(meta_objs, game_objs)
        if meta_objs.stats.active:
            game_objs.ship.update()
            update_bullets(meta_objs, game_objs)
            update_aliens(meta_objs, game_objs)
        update_screen(meta_objs, game_objs)


if __name__ == "__main__":
    run_game()
