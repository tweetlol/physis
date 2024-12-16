
import sys
import torch
import pygame
import random
from pygame.locals import *

from physis import particle


# UI CONSTANTS
## STARS
PARTICLE_R = 5
PROTON_COLOR = (200,0,0)
ELECTRON_COLOR = (0,0,200)
## SCREEN
BG_COLOR = (0,0,0)
WIDTH = 1600
HEIGHT = 900
## ENGINE
TENSOR_TYPE = torch.float64
FPS = 60
## G SETS INTERACTION STRENGHT
G = 1

PARTICLE_COUNT = 1
PARTICLE_SIZE = 5

# ENGINE INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# GENERATE PARTICLES
particles = []
## PROTON-LIKE
for i in range(PARTICLE_COUNT):
    spawn = particle(
        torch.tensor([(WIDTH/2),(HEIGHT/2)], dtype=TENSOR_TYPE),
        torch.tensor([0,0], dtype=TENSOR_TYPE),
        torch.tensor([0,0], dtype=TENSOR_TYPE),
        1, 25, PARTICLE_SIZE, PROTON_COLOR
    )
    particles.append(spawn)

## ELETRON-LIKE
for i in range(PARTICLE_COUNT):
    spawn = particle(
        torch.tensor([(WIDTH/2)+50,(HEIGHT/2)+50], dtype=TENSOR_TYPE),
        torch.tensor([0.3,-0.3], dtype=TENSOR_TYPE),
        torch.tensor([0,0], dtype=TENSOR_TYPE),
        1, 1, PARTICLE_SIZE, ELECTRON_COLOR
    )
    particles.append(spawn)

# RUN THE ENGINE
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 
    screen.fill(BG_COLOR)

    for item in particles:
        for this in particles:
            if this != item:
                this.acc += G * this.calculate_acc_due_to(item)
        item.move()
        item.check_borders(WIDTH, HEIGHT)
        item.draw(screen)
        item.acc = torch.tensor([0,0], dtype=TENSOR_TYPE)

    pygame.display.flip()
    clock.tick(FPS)