
import sys
import torch
import pygame
from pygame.locals import *

STAR_R = 50
STAR_COLOR = (200,200,200)

OTHERS_R = 10
OTHERS_COLOR = (150,150,150)

BG_COLOR = (0,0,0)
WIDTH = 1500
HEIGHT = 900
FPS = 60

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
        pygame.draw.circle(screen, STAR_COLOR, (round(self.pos[0].item()),round(self.pos[1].item())), self.radius)

# CALCULATE GRAVITATIONAL FORCE = ACC

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

init_pos = torch.tensor([WIDTH/2, HEIGHT/2])
init_vel = torch.tensor([0, 0])
init_acc = torch.tensor([0, 0])

runner = star(init_pos, init_vel, init_acc, STAR_R, STAR_COLOR)

# MAKE OTHER STATIC STARS ACC = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 

    screen.fill(BG_COLOR)


    runner.move()
    runner.check_borders(WIDTH, HEIGHT)
    runner.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)