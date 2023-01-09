import pygame, sys, tkinter as tk, random, time
from settings import Screen_settings
from dash import Dash
from ping import Ping_ball
from button import *
from game_stats import Gamestats

class Ping_game:

    def __init__(self, player2 = False):
        """initializing the a game object"""
        pygame.init()
        pygame.mixer.music.load('sound_tracks/space_invaders.wav')
        self.settings = Screen_settings()
        pygame_icon = pygame.image.load('images/ping_ball.ico')
        pygame.display.set_icon(pygame_icon)
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        
        pygame.display.set_caption('Ping Pong')
        #write a function here to check for a second player...
        self.dash_1 = Dash(self)
        self.dash_2 = Dash(self, left= False)
        self.ping_ball = Ping_ball(self)
        self.play_button = Button(self.screen, 'Play')
        self.game_stats = Gamestats(self)
        self.mainClock = pygame.time.Clock()
        self.tap_sound = pygame.mixer.Sound('sound_tracks/punch.wav')
        self.score_sound = pygame.mixer.Sound('sound_tracks/ting.wav')
        self.border_sound = pygame.mixer.Sound('sound_tracks/tap.wav')
        self.game_over_sound = pygame.mixer.Sound('sound_tracks/game_over.wav')
        self.game_over_bool = False
        self.play_mode_button_1 = Select_mode_button(self.screen, 1)
        self.play_mode_button_2 = Select_mode_button(self.screen, 2)
        self.play_mode_button_3 = Select_mode_button(self.screen, 3)
        self.auto_play_1 = False
        self.auto_play_2 = False
        self.select_mode = True
        self.just_hit_ball = None



    def run_game(self):
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.pause()
        
        while True:
            
        #check keyboard events
            self._check_event()
            if self.game_stats.game_active:
                self.dash_1.update_position()
                self.dash_2.update_position()
                if self.ping_ball.visible:
                    increment1, increment2 = self.ping_ball.update_x_position()


                #if increment1==1 or increment2 == 1:
                    #self.game_stats.game_active = False
                    self.game_stats.player_1_score += increment1
                    self.game_stats.player_2_score += increment2
                if self.game_stats.player_1_score > 9:
                    self.game_over('Green player wins!', self.dash_1.color)
                    self.game_over_bool = True
                if self.game_stats.player_2_score > 9:
                    self.game_over('Blue player wins!', self.dash_2.color)
                    self.game_over_bool = True    
                if self.ping_ball.visible:
                    self.ping_ball.update_y_position()
            self._update_screen()
            self.mainClock.tick_busy_loop(self.settings.frame_rate)

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.dash_1.moving_down = True
                
                elif event.key == pygame.K_UP:
                    #assert self.dash_1.moving_down == False if I do this, both keys won't be pressable at the same time...
                    self.dash_1.moving_up = True
                if event.key == pygame.K_s:
                    self.dash_2.moving_down = True
                elif event.key == pygame.K_w:
                    self.dash_2.moving_up = True
                
                elif event.key == pygame.K_SPACE:
                    self.game_stats.game_active = False
                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.pause()
              
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and not self.auto_play_1:
                    self.dash_1.moving_down = False
                    self.dash_1.reset_speed()
                elif event.key == pygame.K_UP and not self.auto_play_1:
                    self.dash_1.moving_up = False
                    self.dash_1.reset_speed()
                if event.key == pygame.K_s and not self.auto_play_2:
                    self.dash_2.moving_down = False
                    self.dash_2.reset_speed()
                elif event.key == pygame.K_w and not self.auto_play_2:
                    self.dash_2.moving_up = False
                    self.dash_2.reset_speed()
            elif event.type== pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if self.select_mode:
                    self._check_mode_button(mouse_position)
                else:    
                    self._check_play_button(mouse_position)
                
                    pygame.mixer.music.unpause()                   

    
    def _update_screen(self):
        
        self.screen.fill(self.settings.bg_color)
        if self.ping_ball.visible:
            self.ping_ball.blitping()
        elif (pygame.time.get_ticks()-self.ping_ball.start_dead_time)/1000 > 1.5:
            self.ping_ball.start_dead_time = 0.0
            self.ping_ball.visible = True

        self.dash_1.draw()
        self.dash_2.draw()
        self.game_stats.draw()
        self._draw_line()
        if not self.game_stats.game_active:
            if self.select_mode:
                self.play_mode_button_1.draw_button()
                self.play_mode_button_2.draw_button()
                self.play_mode_button_3.draw_button()
                self._draw_option_lines()
            else:
                self.play_button.draw_button()
        if self.game_over_bool:
            self.game_over_button.draw_button()
            pygame.display.update()
            time.sleep(3)
            self._get_paul()
            self.screen.blit(self.game_over_img, self.img_rect)
            pygame.display.update()
            time.sleep(3)
            self.game_over_bool = False
            self.game_stats.game_active = False
            self.game_stats.player_1_score = 0 
            self.game_stats.player_2_score = 0
            pygame.mouse.set_visible(True)
        pygame.display.flip()
        #pygame.display.update()
    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            self.game_stats.game_active = True
            pygame.mouse.set_visible(False)
    def _check_mode_button(self, mouse_pos):
        if self.play_mode_button_1.rect.collidepoint(mouse_pos):
            #autoplay
            self.auto_play_2  = True
            self.dash_2.auto = True
            self.dash_2.set_auto_settings()
            del self.play_mode_button_1
            del self.play_mode_button_2
            del self.play_mode_button_3
            self.select_mode = False
        elif self.play_mode_button_2.rect.collidepoint(mouse_pos):
            self.auto_play_1 = False
            del self.play_mode_button_1
            del self.play_mode_button_2
            del self.play_mode_button_3
            self.select_mode = False
        elif self.play_mode_button_3.rect.collidepoint(mouse_pos):
            #autoplay
            self.auto_play_1  = True
            self.auto_play_2 = True
            self.dash_1.auto = True
            self.dash_1.set_auto_settings()
            self.dash_2.auto = True
            self.dash_2.set_auto_settings()

            del self.play_mode_button_1
            del self.play_mode_button_2
            del self.play_mode_button_3
            self.select_mode = False            

    def _draw_line(self):
        pygame.draw.line(self.screen, self.settings.line_color, \
            (int(0.5* self.settings.width), int(0.2*self.settings.height)), 
        (int(0.5* self.settings.width),int(0.8*self.settings.height))\
            , self.settings.line_thickness)
    def _draw_option_lines(self):
        pygame.draw.line(self.screen, self.settings.line_color, \
            (int((self.settings.width-self.play_mode_button_1.rect.width)/2), self.play_mode_button_2.rect.y), 
        (int((self.settings.width-self.play_mode_button_1.rect.width)/2)+self.play_mode_button_1.rect.width,self.play_mode_button_2.rect.y)\
            , self.settings.line_thickness)
        pygame.draw.line(self.screen, self.settings.line_color, \
            (int((self.settings.width-self.play_mode_button_1.rect.width)/2), self.play_mode_button_3.rect.y), 
        (int((self.settings.width-self.play_mode_button_1.rect.width)/2)+self.play_mode_button_1.rect.width,self.play_mode_button_3.rect.y)\
            , self.settings.line_thickness)    


    def game_over(self, message, color):
        self.ping_ball.visible = False
        self.game_over_button = Game_over_button(self.screen, message, color)
        self.game_over_sound.play()

    def _get_paul(self):
        self.game_over_img = pygame.image.load('images/Paul_Biya_2014.png')
        self.img_rect = self.game_over_img.get_rect()
        self.img_rect.center = self.screen.get_rect().center


if __name__ == '__main__':
    ping = Ping_game()
    ping.run_game()


                
