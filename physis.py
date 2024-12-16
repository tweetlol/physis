
import sys
import torch
import pygame
import random
from pygame.locals import *

# INSERT torch.tesnor([x,y], dtype=float64) OBJECTS AS (POS, VEL, ACC)
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

    def calculate_acc_due_to(self, exerting): # INSERT EXERTING STAR AS ARG2
        direction = self.pos - exerting.pos
        mag = direction.norm()
        return(- direction / (mag**3))
        

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


class particle(object):
    def __init__(self, pos, vel, acc, charge, mass, radius, color):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.radius = radius
        self.color = color
        self.charge = charge
        self.mass = mass

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

    def calculate_acc_due_to(self, exerting): # INSERT EXERTING STAR AS ARG2
        direction = self.pos - exerting.pos
        mag = direction.norm()
        grav = - (direction * exerting.mass) / mag**3
        el = (direction * self.charge * exerting.charge) / (self.mass * mag**3)
        return(grav + el)
        