import pygame.font
from settings import Button_settings
class Button:
    def __init__(self, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Button_settings()

        #Set the dimensions and properties of the button.
        self.msg = msg
        self._init_font()
        self._prep_msg()

    def _prep_msg(self):
        """Turn message into a rendered image and center text on the button."""
        self.msg_image = self.font.render(self.msg, True, self.settings.text_color, self.settings.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    def _init_font(self):
        self.font = pygame.font.SysFont(None, self.settings.font_size)

        # Build the button's rect  object and center it.
        self.rect = pygame.Rect(0, 0, self.settings.width, self.settings.height)
        self.rect.center = self.screen_rect.center

        #The button message needs to be prepped only once.
    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
    
class Game_over_button(Button):
    def __init__(self,screen,msg, player_color):
        super().__init__(screen, msg)
        self.settings.width = 320
        self.settings.height = 50
        self.settings.button_color =  player_color
        self._init_font()
        self._prep_msg()

class Select_mode_button(Button):
    def __init__(self, screen, mode):
        super().__init__(screen, '')
        if mode == 1:
            self.msg = "Play solo vs AI"
            self.settings.width = 320
            self.settings.height = 50

            self._init_font()
            #push the rect half way up to centralize the options for
            #the second mode
            self.rect.centery -= (self.rect.height/2)
            self._prep_msg()
        elif mode == 2:
            self.msg = "Play 1 vs 1"
            self.settings.width = 320
            self.settings.height = 50
            self._init_font()
            self.rect.centery += (self.rect.height/2)
            self._prep_msg()
        
        elif mode == 3:
            self.msg = "AI vs AI"
            self.settings.width = 320
            self.settings.height = 50
            self._init_font()
            self.rect.centery += (self.rect.height/2 + self.rect.height)
            self._prep_msg()
