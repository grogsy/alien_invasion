import pygame.font

class Button:
    def __init__(self, settings, screen, msg):
        '''Initialize button attributes'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width        = 255
        self.height       = 50
        self.button_color = (0, 255, 0)
        self.text_color   = (255, 255, 255)
        self.font         = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect        = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Allow some buttons to be interactable only sometimes
        self.activatable = True

        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''Render text as image and center it on the button'''
        self.msg_img      = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def draw_button(self):
        '''Draw the button to screen'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)
