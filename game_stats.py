from settings import Game_stats_settings
import pygame.font
class Gamestats:
    def __init__(self, game):
        self._reset()
        self.game = game
        self.game_active = False
        self.settings = Game_stats_settings()
        self.font = pygame.font.SysFont(None, self.settings.font_size)
        self.rect_player_1 = pygame.Rect(self.settings.font_size*3, 0, self.settings.font_size*3, self.settings.font_size*3)
        self.rect_player_2 = pygame.Rect(game.settings.width - self.settings.font_size*3, 0, self.settings.font_size*3, self.settings.font_size*3)
        


    def _prep_msg(self):
        """Turn message into a rendered image and center text on the button."""
        msg1 = str(self.player_1_score)
        msg2 = str(self.player_2_score)
        self.msg_image_1 = self.font.render(msg1, True, self.game.dash_1.color, self.settings.bg_color)
        self.msg_image_2 = self.font.render(msg2, True, self.game.dash_2.color, self.settings.bg_color)
        #self.msg_image_rect_1 = self.msg_image.get_rect()
        #self.msg_image_rect_1.center = self.rect_player_1.center
        #self.msg_image_rect_2 = self.msg_image.get_rect()
        #self.msg_image_rect_2.center = self.rect_player_1.center

    def _reset(self):
        self.player_1_score = 0
        self.player_2_score = 0
    def  draw(self):
        self._prep_msg()
        #self.game.screen.fill(self.settings.bg_color, self.rect)
        self.game.screen.blit(self.msg_image_1, self.rect_player_1)
        self.game.screen.blit(self.msg_image_2, self.rect_player_2)
