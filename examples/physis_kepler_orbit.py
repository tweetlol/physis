
import sys
import torch
import pygame
from pygame.locals import *

from physis import star, TextObject

# CONSTANTS
## STARS
STAR_R = 5
## SCREEN
BG_COLOR = (0,0,0)
WIDTH = 1900
HEIGHT = 900
FONT_SIZE = 20
FONT_STYLE = 'Arial'
## ENGINE
TENSOR_TYPE = torch.float64
FPS = 300
G = 1 # SETS GRAVITATION INTERACTION STRENGHT

# ENGINE INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)

# INITIAL CONDITIONS
green_pos = torch.tensor([WIDTH/2 + 200, HEIGHT/2], dtype=TENSOR_TYPE)
green_vel = torch.tensor([0, 0.03], dtype=TENSOR_TYPE)
green_acc = torch.tensor([0, 0], dtype=TENSOR_TYPE)

init_pos = torch.tensor([WIDTH/2 - 200, HEIGHT/2], dtype=TENSOR_TYPE)
init_vel = torch.tensor([0, -0.03], dtype=TENSOR_TYPE)
init_acc = torch.tensor([0, 0], dtype=TENSOR_TYPE)

# CELESTIAL POPULATION
green = star(green_pos, green_vel, green_acc, STAR_R, (55,200,55))
red = star(init_pos, init_vel, init_acc, STAR_R, (200,55,55))

# TEXT OBJECTS
TEXT_OBJECTS = []
# STATIC definitions here, change the content of list and draw later
red_textX = TextObject(f"X = {red.pos.tolist()[0]}", font_style, (200,0,0), (10, 10))
red_textY = TextObject(f"Y = {red.pos.tolist()[1]}", font_style, (200,0,0), (10, 30))
TEXT_OBJECTS.append(red_textX)
TEXT_OBJECTS.append(red_textY)

green_textX = TextObject(f"X = {green.pos.tolist()[0]}", font_style, (55,200,55), (10, 50))
green_textY = TextObject(f"Y = {green.pos.tolist()[1]}", font_style, (55,200,55), (10, 70))
TEXT_OBJECTS.append(green_textX)
TEXT_OBJECTS.append(green_textY)

r_text = TextObject(f"R = {(green.pos - red.pos).norm()}", font_style , (170,170,50), (10, 90))
TEXT_OBJECTS.append(r_text)

################################ RUN THE ENGINE ##################################
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

# RED
    red.acc = G * red.calculate_acc_due_to(green)
    red.move()
    red.acc = torch.tensor([0,0], dtype=TENSOR_TYPE)
    red.check_borders(WIDTH, HEIGHT)
    red.draw(screen)
    TEXT_OBJECTS[0] = TextObject(f"X = {round(red.pos.tolist()[0])}", font_style, (200,55,55), (10, 10))
    TEXT_OBJECTS[1] = TextObject(f"Y = {round(red.pos.tolist()[1])}", font_style, (200,55,55), (10, 30))

# GREEN
    green.acc = G * green.calculate_acc_due_to(red)
    green.move()
    green.acc = torch.tensor([0,0], dtype=TENSOR_TYPE)
    green.check_borders(WIDTH, HEIGHT)
    green.draw(screen)
    TEXT_OBJECTS[2] = TextObject(f"X = {round(green.pos.tolist()[0])}", font_style, (55,155,55), (10, 50))
    TEXT_OBJECTS[3] = TextObject(f"Y = {round(green.pos.tolist()[1])}", font_style, (55,155,55), (10, 70))

    TEXT_OBJECTS[4] = TextObject(f"R = {round((green.pos - red.pos).norm().item())}", font_style , (170,170,50), (10, 90))

    pygame.display.flip()
    clock.tick(FPS)