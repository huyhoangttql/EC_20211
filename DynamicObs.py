import pygame


class DynamicObs:
    def __init__(self,screen,dynX,dynY,speedX,speedY,lower_limit,upper_limit,radius):
        self.screen = screen
        self.dynX = dynX
        self.dynY = dynY
        self.speedX = speedX
        self.speedY = speedY
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.radius = radius
    
    def move(self):
        self.dynX += self.speedX
        self.dynY += self.speedY
        
        if self.dynX <= self.lower_limit or self.dynX >= self.upper_limit:
            self.speedX = -self.speedX # cho hình dội lại
            self.speedY = -self.speedY # cho hình dội lại

        pygame.draw.circle(self.screen,(0,191,255),(self.dynX,self.dynY),self.radius)
