from settings import Dash_settings
import pygame

class Dash:
    def __init__(self, game, left = True):
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Dash_settings()
        self.moving_up = False
        self.moving_down = False
        self.left = left
        self.rect = pygame.Rect(0,0,self.settings.width, self.settings.height)
        #self.rect.centery = self.screen_rect.centery
        self.speed = self.settings.speed
        if self.left:
            self.color = self.settings.colorleft
            self.rect.midleft = self.screen_rect.midleft
        else:
            self.color = self.settings.colorright
            self.rect.midright = self.screen_rect.midright
        self.auto = False
    def draw(self):
        #Draw dash at current position
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update_position(self):
        if self.auto:
            self._follow()
        if self.moving_up and self.rect.y > 0:
            self.rect.y -= self.speed
            self.speed += self.settings.acc
        if self.moving_down and ((self.rect.y + self.rect.height) < self.screen_rect.height):#seems like this condition makes it slower to go down
            self.rect.y += self.speed
            self.speed += self.settings.acc     
    def reset_position(self):
        if self.left:
            self.rect.midleft = self.screen_rect.midleft
        else:
            self.rect.midright = self.screen_rect.midright
    def reset_speed(self):
        self.speed = self.settings.speed

    def _cal_target(self):
        #in case the paddle(dash) just hit the ball
        if self.game.just_hit_ball == self:
            self.target = int(self.screen_rect.height/2)
        else:
        
            #calculate the the point where the ping ball touches the\
            #left screen using the equation of its displacement. 
            #gradient = ping_ball_y_speed/ping_ball_x_speed
            #equation: y = gradient*(x - current_x) + current_y
            if self.game.ping_ball.moving_down:#positive y direction
                coefy = 1
            else:#negative y direction
                coefy = -1
            if self.game.ping_ball.moving_right:#positive x direction
                coefx = 1
            else:
                coefx = -1
            
            if self.left:
                #target = subsitute the x component of the left wall(x=0)
                self.target = ((coefy*self.game.ping_ball.speedy)/(coefx*self.game.ping_ball.speedx))\
                    *(0-self.game.ping_ball.rect.x) + self.game.ping_ball.rect.y
            else:
                self.target = ((coefy*self.game.ping_ball.speedy)/(coefx*self.game.ping_ball.speedx))\
                    *(self.screen_rect.width-(self.game.ping_ball.rect.x+self.game.ping_ball.rect.width)) + self.game.ping_ball.rect.y
    def _follow(self):
        
        self._cal_target()
        if self.target < self.rect.y:
            self.moving_up = True
            self.moving_down = False
        elif self.target > self.rect.y+self.rect.height:
            self.moving_down = True
            self.moving_up = False
        else:
            self.moving_down = False
            self.movign_down = False

    def set_auto_settings(self):
        self.settings.speed *= 0.3
        self.settings.acc *= 0.01




    
