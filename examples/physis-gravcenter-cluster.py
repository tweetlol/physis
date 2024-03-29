
import sys
import torch
import pygame
import random
from pygame.locals import *

from physis import star, TextObject
# UI CONSTANTS
## STARS
STAR_R = 5
STAR_COLOR = (0,200,0)
TEXT_COLOR = (0,200,0)
STATIC_R = 2
STATIC_COLOR = (255,255,255)
BROWN_R = 5
BROWN_COLOR = (200,120,80)
## SCREEN
BG_COLOR = (0,0,0)
WIDTH = 1900
HEIGHT = 900
FONT_SIZE = 20
FONT_STYLE = 'Arial'
## ENGINE
TENSOR_TYPE = torch.float64
FPS = 60
G = 0.01 # SETS GRAVITATION INTERACTION STRENGHT


BROWN_AMOUNT = 30
STATIC_AMOUNT = 0


# ENGINE INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)

# INITIAL CONDITIONS
green_pos = torch.tensor([WIDTH/2, HEIGHT/2], dtype=TENSOR_TYPE)
green_vel = torch.tensor([0, 0], dtype=TENSOR_TYPE)
green_acc = torch.tensor([0, 0], dtype=TENSOR_TYPE)

# CELESTIAL POPULATION
green = star(green_pos, green_vel, green_acc, STAR_R, STAR_COLOR)

# MAKE OTHER STATIC STARS ACC = 0, d/dt(ACC) = 0
STATIC_STARS = []
for i in range(STATIC_AMOUNT):
    spawn = star(
        torch.tensor([random.uniform(0,WIDTH), random.uniform(0,HEIGHT)], dtype=TENSOR_TYPE), # RANDOM POSITIONS
        torch.tensor([0, 0], dtype=TENSOR_TYPE), # NO VELOCTIIES
        torch.tensor([0, 0], dtype=TENSOR_TYPE), # NO ACCELERATIONS
        STATIC_R,STATIC_COLOR # RADIUS, COLOR
        )
    STATIC_STARS.append(spawn)

# MAKE BROWNIAN MOTION PROOF OF GRAVITY STARS
BROWN_STARS = []
for i in range(BROWN_AMOUNT):
    spawn = star(
        torch.tensor([random.uniform(200,250), random.uniform(HEIGHT/2-50,HEIGHT/2+50)], dtype=TENSOR_TYPE), # RANDOM POSITIONS
        torch.tensor([0.1, random.uniform(-.01,.01)], dtype=TENSOR_TYPE), # NO INITIAL VELOCTIIES
        torch.tensor([0, 0], dtype=TENSOR_TYPE), # NO INITIAL ACCELERATIONS
        BROWN_R,BROWN_COLOR # RADIUS, COLOR
        )
    BROWN_STARS.append(spawn)

# TEXT OBJECTS
TEXT_OBJECTS = []
# STATIC definitions here, change the content of list and draw later
green_textX = TextObject(f"R_X = {green.pos.tolist()[0]}", font_style, (255,0,0), (10, 10))
green_textY = TextObject(f"R_Y = {green.pos.tolist()[1]}", font_style, (255,0,0), (10, 30))
TEXT_OBJECTS.append(green_textX)
TEXT_OBJECTS.append(green_textY)
green_textX = TextObject(f"V_X = {green.vel.tolist()[0]}", font_style, (55,155,55), (10, 50))
green_textY = TextObject(f"V_Y = {green.vel.tolist()[1]}", font_style, (55,155,55), (10, 70))
TEXT_OBJECTS.append(green_textX)
TEXT_OBJECTS.append(green_textY)

########################################## RUN THE ENGINE #############################################
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 

# CORE (view, text)
    screen.fill(BG_COLOR)
    for item in TEXT_OBJECTS:
        item.update()
        item.draw(screen)

# EPIC GUI (skip this part)
    TEXT_OBJECTS[0] = TextObject(f"R_X = {round(green.pos.tolist()[0])}", font_style, (55,155,55), (10, 10))
    TEXT_OBJECTS[1] = TextObject(f"R_Y = {round(green.pos.tolist()[1])}", font_style, (55,155,55), (10, 30))
    TEXT_OBJECTS[2] = TextObject(f"V_X = {round(green.vel.tolist()[0],2)}", font_style, (55,155,55), (10, 50))
    TEXT_OBJECTS[3] = TextObject(f"V_Y = {round(green.vel.tolist()[1],2)}", font_style, (55,155,55), (10, 70))

# STATIC
    for item in STATIC_STARS:
        green.acc += G * green.calculate_acc_due_to(item)
        item.draw(screen)
        for brown in BROWN_STARS:
            brown.acc += G * brown.calculate_acc_due_to(item)

# BROWNS
    for item in BROWN_STARS:
        green.acc += G * green.calculate_acc_due_to(item)
        item.acc += G * 1000 * item.calculate_acc_due_to(green)
        """NO INTERACTION
        for brown in BROWN_STARS: 
            if brown != item:
                brown.acc += G * brown.calculate_acc_due_to(item)
        """
        item.move()
        #item.check_borders(WIDTH, HEIGHT)
        item.draw(screen)
        item.acc = torch.tensor([0,0], dtype=TENSOR_TYPE)

# GREEN
    green.move()
    green.check_borders(WIDTH, HEIGHT)
    green.draw(screen)
    ## CALCULATE ACCELERATION DUE TO EVERYONE
    green.acc = torch.tensor([0,0], dtype=TENSOR_TYPE)


    pygame.display.flip()
    clock.tick(FPS)