import pygame.font

class Scoreboard:
    '''Score information'''

    def __init__(self, settings, screen, stats):
        self.screen      = screen
        self.screen_rect = screen.get_rect()
        self.settings    = settings
        self.stats       = stats

        # Font settings for scoring information
        self.text_color = (0, 255, 0)
        self.font       = pygame.font.SysFont(None, 48)

        # Prep initial score and level images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        '''Turn score into a rendered image'''
        score_str      = '{:,}'.format(self.stats.play_score)
        self.score_img = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect       = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right
        self.score_rect.top   = 0

    def prep_level(self):
        '''display the level image'''
        self.level_img = self.font.render(str(self.stats.level), True,
                                          self.text_color, self.settings.bg_color)

        # Position the level below score
        self.level_rect       = self.level_img.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_high_score(self):
        '''Turn the high score into a rendered image'''
        high_score          = '{:,}'.format(self.stats.high_score)
        self.high_score_img = self.font.render(high_score, True,
                                               self.text_color, self.settings.bg_color)
        # Center the high score at the top of the screen
        self.high_score_rect         = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top     = self.score_rect.top

    def show_score(self):
        '''Draw score onto the screen'''
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
