from settings import Dash_settings
import pygame

class Dash:
    def __init__(self, screen, left = True):
        self.screen = screen
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
    def draw(self):
        #Draw dash at current position
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update_position(self):
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