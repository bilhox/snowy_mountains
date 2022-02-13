import pygame

from math import *
from pygame.locals import *

class Rect_Collider():
     
     def __init__(self , pos , size):
          
          self.pos = pos
          self.size = size
          self.collided_sides = {"left":False,"right":False,"up":False,"bottom":False}
     
     def set_pos(self , pos):
          self.rect.x , self.rect.y = pos[0] , pos[1]
     
     @property
     def rect(self):
          return Rect(self.pos[0] // 1, self.pos[1] // 1 , self.size[0] , self.size[1])
     
     def collide(self , colliders_list : list[pygame.Rect]):
          
          colliders = []
          
          for collider in colliders_list:
               if collider.colliderect(self.rect):
                    colliders.append(collider)
          
          return colliders
     
     def move(self , colliders , movement):
               
          self.pos[0] += movement[0]
          collided_sides = {"left":False , "right":False , "top":False , "bottom":False}
          collided = self.collide(colliders)
          for c in collided:
               if movement[0] > 0:
                    self.pos[0] = c.left - self.size[0]
                    collided_sides["right"] = True
               elif movement[0] < 0:
                    self.pos[0] = c.right
                    collided_sides["left"] = True
                    
          self.pos[1] += movement[1]
          collided = self.collide(colliders)
          
          for c in collided:
               if movement[1] > 0:
                    self.pos[1] = c.top - self.size[1]
                    collided_sides["bottom"] = True
               elif movement[1] < 0:
                    self.pos[1] = c.bottom
                    collided_sides["top"] = True
          
          self.collided_sides = collided_sides