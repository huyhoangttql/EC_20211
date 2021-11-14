from os import error
import pygame,sys
import json
from DynamicObs import *
from StaticObs import *
pygame.init()

screen = pygame.display.set_mode((1050,600))
pygame.display.set_caption("Mapppp")
running = True

#font
font = pygame.font.SysFont('sans', 32)
font_small = pygame.font.SysFont('sans', 15)

#input_text
input_text = ''
load_file_input_text = font_small.render('Fill in and press F1 to load the map',True,(0,0,0))

#input_form
input_rect = pygame.Rect(860,100,130,50)


#color
white = (255,255,255)
yellow = (255,255,51)
red = (255,0,0)
black = (0,0,0)
blue = (0,191,255)
pink = (205,192,203)

#Init posiotion of robot and goal 
x_robot = y_robot = 100
x_goal = 700
y_goal = 500

active = False

def inputLoader(input_file):
    inputLoad = True
    staticObss = []
    dynamicObss = []
    while inputLoad:
        # inputfile = input("Nhap file input: ")
        try:
            with open (f"{input_file}") as f:
                data = json.load(f)
                for i in data:
                    if i["Dynamic"] == "0":
                        staticObs = StaticObs(screen,int(i["startpointX"]),int(i["startpointY"]),int(i["length"]),int(i["width"]))
                        staticObss.append(staticObs)
                    if i["Dynamic"] == "1":
                        dynamicObs = DynamicObs(screen,int(i["dynX"]),int(i["dynY"]),int(i["speedX"]),
                        int(i["speedY"]),int(i["lower_limit"]),int(i["upper_limit"]),int(i["radius"]))
                        dynamicObss.append(dynamicObs)    
            inputLoad = False
        except Exception:
            print("Wrong file path")
        finally:
            break
    return staticObss,dynamicObss



clock = pygame.time.Clock()
staticObss = []
dynamicObss = []
while running:
    screen.fill(white)

    #get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()  
    text_mouse = font_small.render("(" + str(mouse_x) + "," + str(mouse_y) + ")", True, black)
    screen.blit(text_mouse, (mouse_x + 10, mouse_y))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #handle file input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
            if event.key == pygame.K_F1:
                print(input_text)
                staticObss,dynamicObss = inputLoader(input_text)

    #draw input form
    text_input_surface = font.render(input_text,True,(0,0,0))
    screen.blit(load_file_input_text,(835,80))
    pygame.draw.rect(screen,red,input_rect,2)
    screen.blit(text_input_surface,(input_rect.x+10,input_rect.y+8))
    input_rect.w = max(150,text_input_surface.get_width()+10)
    pygame.draw.line(screen,black,(800,0),(800,600),4)

    #draw robot and goal
    pygame.draw.circle(screen,yellow,(x_robot,y_robot),12)
    pygame.draw.rect(screen,red,[x_goal,y_goal,20,20])
    
    #draw map
    for obstacle in staticObss:
        obstacle.draw()
    for obstacle in dynamicObss:
        obstacle.move()
   


    pygame.display.update()

    clock.tick(30)

pygame.quit()
quit()