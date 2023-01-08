import random, os

class Screen_settings:
    def __init__(self):
        self.bg_color = (255,248,220)
        self.width = 1200
        self.height = 600
        self.frame_rate= 250
        self.line_color =  (165, 42, 42)
        self.dash_lengths = [5,5]
        self.line_thickness= 2

class Dash_settings:
    def __init__(self):
        self.width = 10
        self.height = 100
        self.colorleft = (144, 238, 144)
        self.colorright = (0, 0, 139)

        self.speed = 1.6
        self.acc = 0.04
class Ping_settings:
    def __init__(self):
        self.random_speed()#for some reason, using 0.3 in the place of 0.8 makes the game bug
        self.speed_acc = 0.1
        self.color = (165, 42, 42)
        self.width = 20
        self.height = self.width
        self.radius = self.width/2.0
        
    def random_speed(self):
       #self.speedx, self.speedy = (.5 , .5)
       self.speed = 3.0
       self.speedx = random.uniform(2.0,self.speed)
       
class Button_settings:
    def __init__(self):
        self.button_color = (144,238,144) #light gray
        self.text_color = (255,255,255)
        self.width, self.height = 200, 50
        self.font_size = 48
class Game_stats_settings:
    def __init__(self):
        self.width, self.height = 300, 100
        self.text_color = (255,255,255)
        self.font_size = 40
        self.bg_color = (255,248,220)