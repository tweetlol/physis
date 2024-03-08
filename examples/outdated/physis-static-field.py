
import sys
import torch
import pygame
import random
from pygame.locals import *


class star(object):
    def __init__(self, pos, vel, acc, radius, color):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.radius = radius
        self.color = color

    def move(self):
        self.pos += self.vel
        self.vel += self.acc

    def check_borders(self, width, height):
        if self.pos[0] - self.radius <= 0:
            self.vel[0] *= -1 
        elif self.pos[0] + self.radius >= width:
            self.vel[0] *= -1

        if self.pos[1] - self.radius <= 0:
            self.vel[1] *= -1
        elif self.pos[1] + self.radius >= height:
            self.vel[1] *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0].item(),self.pos[1].item()), self.radius)
# CALCULATE GRAVITATIONAL FORCE = ACC FROM STAR AT POS_OTHER
    def calculate_acc_due_to(self, exerting): # INSERT EXERTING STAR AS ARG2
        direction = self.pos - exerting.pos
        mag = direction.norm()
        return(- G * direction / (mag**3))
        
class TextObject(object):
    def __init__(self, text, font_style, color, location):
        self.text = str(text)
        self.font_style = font_style
        self.color = color
        self.location = location
        self.image = None

    def update(self):
        self.image = self.font_style.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.image, self.location)

# UI CONSTANTS
## STARS
STAR_R = 7
STAR_COLOR = (200,200,200)
TEXT_COLOR = (0,255,0)
OTHERS_R = 10
OTHERS_COLOR = (150,150,150)
## SCREEN
BG_COLOR = (0,0,0)
WIDTH = 1500
HEIGHT = 900
FONT_SIZE = 20
FONT_STYLE = 'Arial'
## ENGINE
TENSOR_TYPE = torch.float64
FPS = 20
G = 10 # SETS GRAVITATION INTERACTION STRENGHT

# ENGINE INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font_style = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)

# INITIAL CONDITIONS
green_pos = torch.tensor([WIDTH/2 + 100, HEIGHT/2], dtype=TENSOR_TYPE)
green_vel = torch.tensor([0, 0.2], dtype=TENSOR_TYPE)
green_acc = torch.tensor([0, 0], dtype=TENSOR_TYPE)

# CELESTIAL POPULATION
green = star(green_pos, green_vel, green_acc, STAR_R, (0,255,0))

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

# MAKE OTHER STATIC STARS ACC = 0?
STARS = []
AMOUNT = 100
for i in range(AMOUNT):
    spawn = star(
        torch.tensor([random.uniform(0,WIDTH), random.uniform(0,HEIGHT)], dtype=TENSOR_TYPE), # RANDOM POSITIONS
        torch.tensor([0, 0], dtype=TENSOR_TYPE), # NO VELOCTIIES
        torch.tensor([0, 0], dtype=TENSOR_TYPE), # NO ACCELERATIONS
        5,OTHERS_COLOR # RADIUS, COLOR
        )
    STARS.append(spawn)

# RUN THE ENGINE 
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

    for item in STARS:
        green.acc += green.calculate_acc_due_to(item)
        item.draw(screen)

# GREEN
    green.move()
    green.check_borders(WIDTH, HEIGHT)
    green.draw(screen)
    ## CALCULATE ACCELERATION DUE TO EVERYONE
    green.acc = torch.tensor([0,0], dtype=TENSOR_TYPE)



    TEXT_OBJECTS[0] = TextObject(f"R_X = {green.pos.tolist()[0]}", font_style, (55,155,55), (10, 10))
    TEXT_OBJECTS[1] = TextObject(f"R_Y = {green.pos.tolist()[1]}", font_style, (55,155,55), (10, 30))
    TEXT_OBJECTS[2] = TextObject(f"V_X = {green.vel.tolist()[0]}", font_style, (55,155,55), (10, 50))
    TEXT_OBJECTS[3] = TextObject(f"V_Y = {green.vel.tolist()[1]}", font_style, (55,155,55), (10, 70))

    pygame.display.flip()
    clock.tick(FPS)