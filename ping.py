import pygame, random, os
from settings import Ping_settings
import time
from math import sqrt
class Ping_ball:

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.settings = Ping_settings()
        self.radius = self.settings.radius
        self.screen_rect = self.screen.get_rect()
        #self.image = pygame.image.load('images/football3.bmp')
        
        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect(0,0,self.settings.width,self.settings.height)
        #initialize the ping ball at the center
        self.rect.center = self.screen_rect.center
        
        #self.speedy = self.settings.speedy
        self.speed = self.settings.speed
        self.speedx = self.settings.speedx
        self._speed_y()
        self.moving_right = bool(random.randint(0,1))
        self.moving_down = bool(random.randint(0,1))
        self.visible = True
        self.start_dead_time = 0.0
       


    def blitping(self):
        #draw the ping at its current location
        #self.screen.blit(self.image, self.rect)
        
        pygame.draw.circle(self.screen,self.settings.color, (self.rect.centerx, self.rect.centery),\
            self.radius, 0)

    def _speed_y(self):
        self.speedy = sqrt((self.speed ** 2) -(self.speedx**2))

    def update_x_position(self):
        if self.moving_right:
            #if self.rect.y < self.game.dash_2.rect.y or self.rect.y > self.game.dash_2.rect.y+self.game.dash_2.rect.height:
            #check whether it collides with the right dash
            if not self.game.dash_2.rect.colliderect(self.rect):
                #self.rect.x += self.speedx
                if (self.rect.x) < self.screen_rect.width:
                    self.rect.x += self.speedx
                else:
                    self.game.score_sound.play()
                    self._reset_position()
                    self.start_dead_time = pygame.time.get_ticks()
                    self.visible = False
                    #self.game.dash_1.reset_position()
                    
                    #self.game.dash_2.reset_position()                    
                    #time.sleep(1)
                    return (1,0)
                    #return value to increment score of right dash by 1
                    #pass
                    #self.moving_right = False
            
                                
            else:
                self.game.tap_sound.play()  
                self._ping_accelerate()
                self.game.just_hit_ball = self.game.dash_2
                
                
            
                if self.game.dash_2.moving_down:
                    self._accelerate(-self.game.dash_2.settings.acc)
                elif self.game.dash_2.moving_up:
                    self._accelerate(self.game.dash_2.settings.acc)
                self.moving_right = False
                    
                              
        else:
            #check whether it collides with the left dash
            
            if not self.game.dash_1.rect.colliderect(self.rect):
                
                if self.rect.x > -self.rect.width:
                    self.rect.x -= self.speedx
                else:
                    #return value to increment of left dash by 1
                    self.game.score_sound.play()
                    self._reset_position()
                    self.start_dead_time = pygame.time.get_ticks()
                    self.visible = False
                    #self.game.dash_1.reset_position()
                    #self.game.dash_2.reset_position()
                    #time.sleep(1)

                    return (0,1)                
            else:
                self.game.tap_sound.play() 
                self._ping_accelerate()
                self.game.just_hit_ball = self.game.dash_1
                
                
                if self.game.dash_1.moving_down:
                    self._accelerate(self.game.dash_1.settings.acc)
                elif self.game.dash_2.moving_up:
                    self._accelerate(-self.game.dash_1.settings.acc)
                self.moving_right = True
                           
            
        return (0,0) #the ball did not crass wall 











    def update_y_position(self):
        if self.moving_down:

            if (self.rect.y+self.rect.height) < self.screen_rect.height:# not touching bottom screen
                self.rect.y += self.speedy
            else: #touching bottom screen
                
                
                self.game.border_sound.play()
                self.moving_down = False
        else:
            if self.rect.y > 0:
                self.rect.y -= self.speedy
            else:
                
                
                self.game.border_sound.play()
                self.moving_down = True    
    def _reset_position(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = random.uniform(0.2*self.screen_rect.height, 0.6*self.screen_rect.height)            
        self.moving_right = bool(random.randint(0,1))
        self.moving_down = bool(random.randint(0,1))
        #should make it reset after rounds, not at every goal though
        self.speed = self.settings.speed
        self.speedx = random.uniform(2.0, self.speed)
        self._speed_y()
        self.game.just_hit_ball = None
        
        
    def _accelerate(self, acc):

        self.speedy -= acc
    def _ping_accelerate(self):
        self.speed += self.settings.speed_acc
        self.speedx += random.uniform(0,self.settings.speed_acc)
        self._speed_y()




















    """
    def update_x_position(self, self.game.dash_1, self.game.dash_2):
        if self.moving_right:
            if self.rect.y < self.game.dash_2.rect.y or self.rect.y > self.game.dash_2.rect.y+self.game.dash_2.rect.height:
            #check whether it collides with the right dash
            #if not self.game.dash_2.rect.collidepoint(self.rect.x+3, self.rect.y):
                #self.rect.x += self.speedx
                if (self.rect.x+self.rect.width) < self.screen_rect.width:
                    self.rect.x += self.speedx
                else:
                    
                    self._reset_position()
                    self.game.dash_1.reset_position()
                    self.game.dash_2.reset_position()                    
                    time.sleep(2)
                    return (1,0)
                    #return value to increment score of right dash by 1
                    #pass
                    #self.moving_right = False
            
                                
            else:
                if (self.rect.x+self.rect.width) < self.screen_rect.width-self.game.dash_2.rect.width:
                    self.rect.x += self.speedx

                else:
                    if self.game.dash_2.moving_down:
                        self._accelerate(self.game.dash_2.settings.acc)
                    elif self.game.dash_2.moving_up:
                        self._accelerate(-self.game.dash_2.settings.acc)
                    self.moving_right = False      
                              
        else:
            #check whether it collides with the left dash
           
            #if not self.game.dash_1.rect.collidepoint(self.rect.x, self.rect.y):
                #self.rect.x -= self.speedx
            #else:
                #self.moving_right = True

           
            if self.rect.y < self.game.dash_1.rect.y or self.rect.y > self.game.dash_1.rect.y+self.game.dash_1.rect.height:
                if self.rect.x > -self.rect.width:
                    self.rect.x -= self.speedx
                else:
                    #return value to increment of left dash by 1
                    
                    self._reset_position()
                    self.game.dash_1.reset_position()
                    self.game.dash_2.reset_position()
                    time.sleep(1)

                    return (0,1)
                    #pass
                    #self.moving_right = True    
            else:
                #collision with left dash
                if self.rect.x > 0 + self.game.dash_1.rect.width:
                    self.rect.x -= self.speedx
                else:
                    if self.game.dash_1.moving_down:
                        self._accelerate(self.game.dash_1.settings.acc)
                    elif self.game.dash_2.moving_up:
                        self._accelerate(-self.game.dash_1.settings.acc)
                    self.moving_right = True                    
        return (0,0) #the ball did not crass wall  
    """        
