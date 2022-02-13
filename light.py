import pygame

from pygame.locals import *
from math import *

class Light():
     
     def __init__(self , pos , color=[255,255,255]):
          
          self.max_radius = 30
          self.min_radius = 20

          self.texture = pygame.Surface([self.max_radius*2,self.max_radius*2] , SRCALPHA)
          
          
          