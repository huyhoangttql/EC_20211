# from os import error
import pygame,sys
import json
from DynamicObs import *
from StaticObs import *
from algo import list_vertices,list_node
import time
from Robot import *
from clean import list_node1,list_vertices1
pygame.init()

screen = pygame.display.set_mode((800,700))
pygame.display.set_caption("Mapppp")
running = True

#font
font = pygame.font.SysFont('sans', 32)
font_small = pygame.font.SysFont('sans', 15)

#input_text
input_text = ''
load_file_input_text = font_small.render('Fill in and press F1 to load the map',True,(0,0,0))

#input_form
input_rect = pygame.Rect(560,100,130,50)


#color
white = (255,255,255)
yellow = (255,255,51)
red = (255,0,0)
black = (0,0,0)
blue = (0,191,255)
pink = (205,192,203)

#Init posiotion of robot and goal 
x_robot = 200
y_robot = 600
x_goal = 300
y_goal = 170

# active = False

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

list_vertices.insert(0,[x_robot,y_robot])
list_vertices.append([x_goal,y_goal])
list_vertices1.append([x_goal,y_goal])
# list_vertices.append([0,0])
# print(len(list_vertices))
robot = Robot(screen,200,600,list_vertices,12)

def distance(a,b):
    return(((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5)

clock = pygame.time.Clock()
staticObss = []
dynamicObss = []
it = 0
def draw_vertices(lst,color):
    for i in range(len(lst)):
        pygame.draw.rect(screen,color,[lst[i][0],lst[i][1],3,3])
# dyn1 = [DynamicObs(screen,100,100,3,4,80,120,5),DynamicObs(screen,150,150,2,3,130,160,3)
# ]
staticObss,dynamicObss = inputLoader(input_file='input3.json')
while it!= len(list_vertices) and running:
    #print(list_vertices[it])

    #get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()  
    text_mouse = font_small.render("(" + str(mouse_x) + "," + str(mouse_y) + ")", True, black)
    screen.blit(text_mouse, (mouse_x + 10, mouse_y))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #handle file input
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_BACKSPACE:
        #         input_text = input_text[:-1]
        #     else:
        #         input_text += event.unicode
        #     if event.key == pygame.K_F1:
        #         print(input_text)
        #         staticObss,dynamicObss = inputLoader(input_text)
    # staticObss,dynamicObss = inputLoader(input_file='input1.json')
    screen.fill(white)

    #draw input form
    text_input_surface = font.render(input_text,True,(0,0,0))
    screen.blit(load_file_input_text,(550,80))
    pygame.draw.rect(screen,red,input_rect,2)
    screen.blit(text_input_surface,(input_rect.x+10,input_rect.y+8))
    input_rect.w = max(150,text_input_surface.get_width()+10)
    pygame.draw.line(screen,black,(500,0),(500,600),4)

    # draw_vertices(list_node,red)
    # draw_vertices(list_vertices,black)
    #draw robot and goal

    robot.draw(screen=screen, pos = list_vertices[it])
    pygame.draw.rect(screen,red,[x_goal,y_goal,20,20])
    # for i in dyn1:
    #     i.move()
    
    #draw map
    for obstacle in staticObss:
        obstacle.draw()
    for obstacle in dynamicObss:
        obstacle.move()
   


    pygame.display.update()
    pygame.time.delay(300)
    clock.tick(30)
    for obstacle in dynamicObss:  

        if(distance(list_vertices[it],[obstacle.dynX,obstacle.dynY])<40):
            print("detect dynamic obs")
            print([obstacle.dynX,obstacle.dynY])
            print([obstacle.speedX,obstacle.speedY])
            print(list_vertices[it])
            print([list_vertices[it+1][0]-list_vertices[it][0],list_vertices[it+1][1]-list_vertices[it][1]])
            it-=1
            # list_vertices.insert(0,(list_vertices[it]))
            list_vertices = list_vertices1
            list_node = list_node1
            
        
    it+=1
    
pygame.quit()
quit()