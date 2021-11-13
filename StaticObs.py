import pygame


class StaticObs:
    def __init__(self,screen,startpointX,startpointY,length,width):
        self.screen = screen
        self.startpointX = startpointX
        self.startpointY = startpointY
        self.length = length
        self.width = width
    
    def draw(self):
        pygame.draw.rect(self.screen,(0,0,0),(self.startpointX,self.startpointY,self.length,self.width))
        