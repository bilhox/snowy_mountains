import pygame

from math import *
from pygame.locals import *

def isOutOfScreen(surface_size , rect : Rect):
     
     if -rect.w < rect.x < surface_size[0]:
          if -rect.h < rect.y < surface_size[1]:
               return False
          return True
     return True

def isOutOfRange(rect : Rect):
     if -rect.w - 100 < rect.x < 550:
          if -rect.h - 100 < rect.y < 400:
               return False
          return True
     return True

def display_text_debug(screen , clock , dt , player):
     pass
     screen.blit(pygame.font.Font(None , 20).render(f"FPS : {round(clock.get_fps() , 2)}",True,[255,0,0]),[0,12])