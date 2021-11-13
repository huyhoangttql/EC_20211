import pygame
import json
from DynamicObs import *
from StaticObs import *
pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Mapppp")
running = True

#color
white = (255,255,255)
yellow = (255,255,51)
red = (255,0,0)
black = (0,0,0)
blue = (0,191,255)

#Khoi tao vi tri ban dau cua robot va dich
x_robot = y_robot = 100
x_goal = 700
y_goal = 500

staticObss = []
dynamicObss = []
with open ("input1.json") as f:
    data = json.load(f)
    for i in data:
        if i["Dynamic"] == "0":
            staticObs = StaticObs(screen,int(i["startpointX"]),int(i["startpointY"]),int(i["length"]),int(i["width"]))
            staticObss.append(staticObs)
        if i["Dynamic"] == "1":
            dynamicObs = DynamicObs(screen,int(i["dynX"]),int(i["dynY"]),int(i["speedX"]),
            int(i["speedY"]),int(i["lower_limit"]),int(i["upper_limit"]),int(i["radius"]))
            dynamicObss.append(dynamicObs) 



clock = pygame.time.Clock()

while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.draw.circle(screen,yellow,(x_robot,y_robot),12)
    pygame.draw.rect(screen,red,[x_goal,y_goal,20,20])
    for obstacle in staticObss:
        # print(j)
        obstacle.draw()
    for obstacle in dynamicObss:
        obstacle.move()


    pygame.display.update()

    clock.tick(30)

pygame.quit()
quit()