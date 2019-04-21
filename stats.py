class GameStats:
    '''Track statistics for Alien Invasion'''

    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()

        # Start game in active state
        self.active = False
        # variable to toggle pause/unpause
        self.paused = False
        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        '''reset stats'''
        self.ships_left = self.settings.ship_limit
        self.play_score = 0
        self.level      = 1

        self.shots_fired  = 0
        self.shots_landed = 0
