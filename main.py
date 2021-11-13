import pygame
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

ls = [[200,300,50,70],
    [225,270,60,30],
    [400,400,30,70],
    [550,150,70,25],
    [590,175,30,45]]

staticObss = []
for i in ls:
    staticObs = StaticObs(screen,i[0],i[1],i[2],i[3])
    staticObss.append(staticObs)


clock = pygame.time.Clock()
dynX1=150
dynY1=250
speedX1 = 4
speedY1 = 3
radius = 10
dynObs1 = DynamicObs(screen,dynX1,dynY1,speedX1,speedY1,150,300,radius)
dynObs2 = DynamicObs(screen,300,350,-4,5,250,400,10)
while running:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.draw.circle(screen,yellow,(x_robot,y_robot),12)
    pygame.draw.rect(screen,red,[x_goal,y_goal,20,20])
    for j in staticObss:
        j.draw()
    dynObs1.move()
    dynObs2.move()


    pygame.display.update()

    clock.tick(30)

pygame.quit()
quit()