# physis

*pygame / torch class for particle simulations*

## prequisites

```py
import torch
import pygame
import sys
from pygame.locals import *
```

## particle simulation class

```py
from physis import star, TextObject
```

star particle class for simulations
insert arguments:
- torch.tensor([x,y]) for pos, vel and acc
- scalar for radius,
- (255, 255, 255) RGB tuple for color
- iterate methods every frame

```py
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
        return(- direction / (mag**3))
```
