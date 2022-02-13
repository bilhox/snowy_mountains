import pygame

from pygame.locals import *
from math import *
from random import *
from unclassed_functions import *

def circle_surf(size, color):
     surf = pygame.Surface((size * 2 + 2, size * 2 + 2))
     pygame.draw.circle(surf, color, (size + 1, size + 1), size)
     return surf

def blit_center(target_surf, surf, loc):
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2))

def blit_center_add(target_surf, surf, loc):
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2), special_flags=pygame.BLEND_RGBA_ADD)

class Circle_explosions():
     
     def __init__(self , pos , color=[20 , 230 , 12]):
          
          self.startpoint = pos
          self.cooldown = 20
          self.color = color
          self.circles = []
          self.max_circles = 10
          self.radius = 100
          self.timer = 0
          self.speed_coef = 3.25
          self.angle = 0
          self.circle_height = 30
          self.vector = [15,15]
          self.visible = False
     
     def update(self):
          if self.visible:
               self.timer += 1
               self.angle += 5
          else:
               self.timer = 0
               self.angle = 0
               if len(self.circles) != 0:
                    self.circles = []
     
     def display(self , surface , scroll):
          
          if self.visible:
               if (self.timer % self.cooldown) == 0:
                    if len(self.circles) <= self.max_circles:
                         circle = {"pos":self.startpoint.copy() , "timer":0 , "size":10 , "start_width":self.circle_height , "width":0}
                         self.circles.append(circle)
                    else:
                         self.circles.pop(0)
                         
               
               for c in self.circles:
                    c["timer"] += 1
                    c["size"] = int(c["timer"]*self.speed_coef)
                    x = self.vector[0]*cos(radians(self.angle))-self.vector[1]*sin(radians(self.angle))+self.startpoint[0]
                    y = self.vector[0]*sin(radians(self.angle))+self.vector[1]*cos(radians(self.angle))+self.startpoint[1]
                    x = ceil(x) if x % 1 >= 0.5 else floor(x)
                    y = ceil(y) if y % 1 >= 0.5 else floor(y)
                    c["pos"] = [x , y]
                    c["width"] = int(c["start_width"]*(1-(c["size"] / self.radius))) if int(c["start_width"]*(1-(c["size"] / self.radius))) > 1 else 1
                    pygame.draw.circle(surface, self.color, [c["pos"][0] - scroll[0],c["pos"][1] - scroll[1]], c["size"], c["width"])
                    
                    if c["size"] > self.radius:
                         self.circles.remove(c)
     

class Particle_system():
     
     def __init__(self , pos , particle_texture : pygame.Surface, color=[20 , 230 , 12] , visible=True):
          self.startpoint = pos
          self.particles = []
          self.particle_size = [1,1]
          self.cooldown = 1
          self.direction = [0 , 1]
          self.speed = 1
          self.color = color
          self.max_particle = 300
          self.min_time = 1
          self.max_time = 100
          self._visible = visible
          self.spawn_coef = 1

          self.particle_texture = particle_texture
          
          if self.particle_texture == None:
               self.particle_texture = pygame.Surface(self.particle_size)
               self.particle_texture.fill(self.color)
          else:
               self.particle_size = particle_texture.get_size()
     @property
     def visible(self):
          return self._visible
     
     @visible.setter
     def visible(self , case):
          self._visible = case
          if not self._visible:
               self.timer = 0
               if len(self.particles) != 0:
                    self.particles = []
     
     def get_visible(self , scroll):
          
          particles = []
          
          for particle in self.particles:
               p_rect = Rect([particle["pos"][0] - scroll[0] , particle["pos"][1] - scroll[1]] , self.particle_size)
               if not isOutOfScreen([300 , 200],p_rect):
                    particles.append(particle)
          
          return particles
          
     
     def update(self , game_timer):          
          if (int(game_timer) % self.cooldown) == 0:
               if len(self.particles) <= self.max_particle:
                    for i in range(self.spawn_coef):
                         particle = {"pos":self.startpoint.copy() , "timer":0 , "max_time":randint(self.min_time,self.max_time) , "speed":self.speed}
                         self.particles.append(particle)
          
          for p in self.particles:
               p["timer"] += 1
               p["pos"][1] -= self.direction[1] * p["speed"]
               p["pos"][0] += self.direction[0] * p["speed"]
               if p["timer"] > p["max_time"]:
                    self.particles.remove(p)    
                    
     
     def display(self , surface , scroll=[0,0]):
              
               
          for p in self.get_visible(scroll):
               surface.blit(self.particle_texture , [int(p["pos"][0]) - scroll[0],int(p["pos"][1]) - scroll[1]])   


class Zone_psystem(Particle_system):
     
     def __init__(self , zone : Rect , texture : pygame.Surface):
          super().__init__([zone.x , zone.y] , texture)
          self.rect = zone.copy()
          if texture == None:
               self.particle_texture = pygame.Surface(self.particle_size)
               self.particle_texture.fill([100, 201, 217])
     
     def update(self , game_timer : int):
          self.startpoint = [randint(self.rect.x , self.rect.x + self.rect.w),randint(self.rect.y , self.rect.y + self.rect.h)]
          super().update(game_timer)