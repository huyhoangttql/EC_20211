import pygame

class Robot:
    def __init__(self,screen,robot_x,robot_y,list_point,radius):
        self.screen = screen
        self.robot_x = robot_x
        self.robot_y = robot_y
        self.list_point = list_point
        self.radius = radius

    
    def draw(self, screen, pos):
        

        pygame.draw.circle(screen,(255,255,51),(pos[0],pos[1]),self.radius)
            
     