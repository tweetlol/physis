# physis

 pygame / torch class for particle simulations

## prequisites

```py
import torch
import pygame
import sys
from pygame.locals import *
```

## particle simulation class

```py
from physis import particle
```

particle class for simulations

insert arguments:
- torch.tensor([x,y]) for pos, vel and acc
- scalar for charge, mass, radius,
- (255, 255, 255) RGB tuple for color
  
iterate methods every frame

more in examples
