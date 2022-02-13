import pygame
from animation import AnimationManager
import time

from math import *
from physics import Rect_Collider
from pygame.locals import *
from unclassed_functions import *

ENTITY_LAYER = 0

class Entity:
     
     def __init__(self , pos : list[int , int], size : list[int , int] , anim_Manager : AnimationManager = None):
          
          self.pos = pos
          self.size = size
          self.velocity = [0,0]
          self.movement = [0,0]
          self.gravity = 0.23
          self.colliding = True
          self.visible = True
          self.flip = False
          self.pos_chunk = [0,0]
          self.anim_Manager = anim_Manager
          self.active_animation = None
          self.textures = {}
          self.textures["default"] = pygame.Surface(self.size)
          self.textures["default"].fill([20 , 185 , 12])
          self.current_texture = self.textures["default"]
          
          self.collider = Rect_Collider(self.pos.copy() , self.size.copy())
          if self.anim_Manager != None and "idle" in self.anim_Manager.animations.keys():
               self.set_action("idle")
     
     @property
     def rect(self):
          
          return Rect(int(self.pos[0]) , int(self.pos[1]) , self.size[0] , self.size[1])
     
     def add_texture(self , id , path):
          img = pygame.image.load(path).convert_alpha()
          self.textures[id] = img
     
     def set_pos(self , pos : list[int , int]):
          
          self.pos = pos
          self.collider.pos = pos
     
     def set_action(self , id):
          
          if self.anim_Manager != None:
               
               if self.active_animation == None or self.active_animation.data.id != id:
                    self.active_animation = self.anim_Manager.get(id)
     
     def update(self , dt , scroll : list[int , int]):
          
          self.pos_chunk = [int(self.pos[0] // 128) , int(self.pos[1] // 128)]
          
          if not isOutOfScreen([350 , 250],Rect([self.rect.x - scroll[0],self.rect.y - scroll[1]],self.rect.size)):
               self.visible = True
          else:
               self.visible = False
               
          if self.visible:
               
               if self.active_animation != None:
                    self.active_animation.play(dt)
               
               dt *= 60
               self.velocity[1] = min(self.velocity[1] + self.gravity * dt , 5)
               velocity_bis = self.velocity.copy()
               
               velocity_bis[0] *= min(dt , 3)
               velocity_bis[1] = min(velocity_bis[1] * dt , 8)    
               self.movement = velocity_bis
          
               
     def update_after_moved(self):
          if self.visible:
               if self.collider.collided_sides["bottom"] or self.collider.collided_sides["top"]:
                    self.velocity[1] = 0       
     
     def collide(self , colliders : list[pygame.Rect]):
          
          return self.rect.collidelistall(colliders)
               

     def event_handler(self , event : pygame.event.Event):
          pass

     def move(self , colliders):
               
          if self.visible:
               self.collider.move(colliders , self.movement.copy())
               # self.pos[0] += self.movement[0]
               # c_tab = list(colliders.values())
               # collided = self.collide(c_tab)
               # collided_sides = {"left":False , "right":False , "top":False , "bottom":False}
               # for c in collided:
               #      if self.movement[0] > 0:
               #           self.pos[0] = c_tab[c].left - self.size[0]
               #           collided_sides["right"] = True
               #      elif self.movement[0] < 0:
               #           self.pos[0] = c_tab[c].right
               #           collided_sides["left"] = True
                         
               # self.pos[1] += self.movement[1]
               # collided = self.collide(c_tab)
               
               # for c in collided:
               #      if self.movement[1] > 0:
               #           self.pos[1] = c_tab[c].top - self.size[1]
               #           collided_sides["bottom"] = True
               #      elif self.movement[1] < 0:
               #           self.pos[1] = c_tab[c].bottom
               #           collided_sides["top"] = True
               self.pos = self.collider.pos.copy()
               
               self.update_after_moved()
     
     def display(self , surface : pygame.Surface, scroll):
          
          rect = self.rect
          true_rect = Rect([rect.x-scroll[0] , rect.y-scroll[1]],self.rect.size) 
          
          if self.visible:
               if self.active_animation != None:
                    self.active_animation.render(surface , [true_rect.x , true_rect.y] , self.flip)
               else:
                    surface.blit(pygame.transform.flip(self.current_texture, self.flip, False) , [true_rect.x , true_rect.y])
          
          

class Player(Entity):
     
     def __init__(self , pos , size , able_to_move=True , anim_Manager : AnimationManager = None):
          
          super().__init__(pos , size , anim_Manager)
          self.life = 3
          self.speed = 2.25
          self.run_speed = 3
          self.texture_size = size
          self.sneak_speed = 0.75
          self.is_sneaking = False
          self.base_jump_height = 5.75
          self.jump_height = self.base_jump_height
          self.jump_height_running = 6.15
          self.air_timer = 0
          self.grounding = False
          self.centered = True
          self._able_to_move = able_to_move
          self.jumping_sound = pygame.mixer.Sound("./data/sfx/jump_02.wav")
          self.jumping_sound.set_volume(0.5)
          self.dash_duration = 0.1
          self.last_dash = 0
          self.dash_amount = 10
          self.dashing = False
          self.side = "right"
          self.trail = True

          # self.texture = pygame.Surface([self.size[0]+4 , self.size[1]+2])
          # self.texture.fill([230 , 45 , 12])
          
          self.key_pressed = {"right":False,"left":False ,"sneak":False,"run":False}
          self.collided_sides = {"left":False , "right":False , "top":False , "bottom":False}
     
     @property
     def able_to_move(self):
          return self._able_to_move
     
     @able_to_move.setter
     def able_to_move(self , case):
          self._able_to_move = case
          if not case:
               for key in self.key_pressed:
                    self.key_pressed[key] = False
     
     # @property
     # def rect(self):
     #      if self.is_sneaking:
     #           return Rect(int(self.pos[0]) , int(self.pos[1] + self.size[1] / 2) , self.size[0] , int(self.size[1] / 2))
     #      else:
     #           return Rect(int(self.pos[0]) , int(self.pos[1]) , self.size[0] , self.size[1])
     
     def update(self , dt):
          
          self.air_timer += 1
          
          if self.active_animation != None:
               self.active_animation.play(dt)
          
          # self.pos_chunk = [int(self.pos[0] // 128) , int(self.pos[1] // 128)]
          dt *= 60
          self.velocity[1] = min(self.velocity[1] + self.gravity * dt , 8)
          
          velocity_bis = self.velocity.copy()
          
          if self.key_pressed["sneak"]:
               self.is_sneaking = True
          else:
               self.is_sneaking = False

          if self.able_to_move and not self.is_sneaking:
               if self.key_pressed["right"]:
                    self.flip = False
                    velocity_bis[0] += self.speed if not self.key_pressed["run"] else self.run_speed
               if self.key_pressed["left"]:
                    self.flip = True
                    velocity_bis[0] -= self.speed if not self.key_pressed["run"] else self.run_speed
          elif self.able_to_move and self.is_sneaking:
               if self.key_pressed["right"]:
                    self.flip = False
                    velocity_bis[0] += self.sneak_speed
               if self.key_pressed["left"]:
                    self.flip = True
                    velocity_bis[0] -= self.sneak_speed
          
          velocity_bis[0] *= dt
          # velocity_bis[1] *= dt
          # velocity_bis[1] = min(velocity_bis[1],8)
          self.movement = velocity_bis
          
          try:
               if self.air_timer > 4:
                    self.active_animation = None
                    if self.velocity[1] < 0:
                         self.current_texture = self.textures["jumping"]
               elif self.movement[0] != 0:
                    self.set_action("running")
               else:
                    self.set_action("idle")
          except:
               raise FileNotFoundError("Textures for player are missing !")
          
          
     
     def update_after_moved(self):
          super().update_after_moved()
          if self.collider.collided_sides["bottom"]:
               self.air_timer = 0
               self.grounding = True
     
     def event_handler(self , event : pygame.event.Event):
          
          if event.type == KEYDOWN:
               if event.key == K_LEFT:
                    self.key_pressed["left"] = True
                    self.side = "left"
               if event.key == K_RIGHT:
                    self.key_pressed["right"] = True
                    self.side = "right"
               if event.key == K_DOWN:
                    self.key_pressed["sneak"] = True
               if event.key == K_s and self.air_timer <= 3:
                    self.key_pressed["run"] = True
                    self.jump_height = self.jump_height_running
               if event.key == K_UP:
                    if self.air_timer <= 3:
                         # self.side = "up"
                         self.jumping_sound.play()
                         self.velocity[1] = -(self.jump_height)
               if event.key == K_d:
                    if not self.dashing:
                         self.dashing = True
                         self.last_dash = time.time()
          elif event.type == KEYUP:
               if event.key == K_LEFT:
                    self.key_pressed["left"] = False
               if event.key == K_RIGHT:
                    self.key_pressed["right"] = False
               if event.key == K_DOWN:
                    self.key_pressed["sneak"] = False
               if event.key == K_s:
                    self.key_pressed["run"] = False
                    self.jump_height = self.base_jump_height

     def display(self , surface , scroll):
          
          s_pos = [self.rect.x-scroll[0] , self.rect.y-scroll[1]]
          
          if self.active_animation != None:
               if self.centered:
                    pos = [(s_pos[0] + self.size[0] // 2) - self.texture_size[0] // 2 , (s_pos[1] + self.size[1] // 2) - self.texture_size[1] // 2]
                    self.texture_size = self.active_animation.render(surface , pos , self.flip)
               else:
                    self.texture_size = self.active_animation.render(surface , s_pos , self.flip)
          else:
               self.texture_size = self.current_texture.get_size()
               if self.centered:
                    pos = [(s_pos[0] + self.size[0] // 2) - self.texture_size[0] // 2 , (s_pos[1] + self.size[1] // 2) - self.texture_size[1] // 2]
                    surface.blit(pygame.transform.flip(self.current_texture, self.flip, False) , pos)
               else:
                    surface.blit(pygame.transform.flip(self.current_texture, self.flip, False) , s_pos)

class Mob(Entity):
     
     def __init__(self , pos , size):
          super().__init__(pos , size)
          # Which direction is moving
          self.side = "right"
          # speed
          self.speed = 0.5
     
     # def move(self , colliders):
               
     #      if self.visible:
     #           self.pos[0] += self.movement[0]
     #           c_tab = list(colliders.values())
     #           collided = self.collide(c_tab)
     #           collided_sides = {"left":False , "right":False , "top":False , "bottom":False}
     #           for c in collided:
     #                if self.movement[0] > 0:
     #                     self.pos[0] = c_tab[c].left - self.size[0]
     #                     collided_sides["right"] = True
     #                elif self.movement[0] < 0:
     #                     self.pos[0] = c_tab[c].right
     #                     collided_sides["left"] = True
                         
     #           self.pos[1] += self.movement[1]
     #           collided = self.collide(c_tab)

     #           for c in collided:
     #                if self.movement[1] > 0:
     #                     self.pos[1] = c_tab[c].top - self.size[1]
     #                     collided_sides["bottom"] = True
     #                elif self.movement[1] < 0:
     #                     self.pos[1] = c_tab[c].bottom
     #                     collided_sides["top"] = True
                    
     #           self.collided_sides = collided_sides
     #           self.update_after_moved()
               
     #           temp_y = (self.pos[1] + self.size[1]) // 16
     #           if not f"{self.pos[0] // 16}-{temp_y}" in colliders and self.movement[0] < 0:
     #                self.side = "right"
     #           elif not f"{(self.pos[0] + self.size[1]) // 16}-{temp_y}" in colliders  and self.movement[0] > 0:
     #                self.side = "left"
     
     def update(self , dt , scroll):
          
          self.pos_chunk = [int(self.pos[0] // 128) , int(self.pos[1] // 128)]
          
          # See if mob need to be loaded
          if not isOutOfRange(Rect([self.pos[0] - scroll[0],self.pos[1] - scroll[1]],self.rect.size)):
               self.visible = True
          else:
               self.visible = False
          
          if self.visible:    
               
               dt *= 60
               self.velocity[1] = min(self.velocity[1] + self.gravity * dt , 5)
               
               velocity_bis = self.velocity.copy()
               if self.side == "left":
                    velocity_bis[0] -= self.speed
               elif self.side == "right":
                    velocity_bis[0] += self.speed
                    
               velocity_bis[0] *= min(dt , 3)
               
               # if self.collided_sides["right"]:
               #      self.side = "left"
               # elif self.collided_sides["left"]:
               #      self.side = "right"
                    
               velocity_bis[1] *= dt
               velocity_bis[1] = min(velocity_bis[1],8)            
               self.movement = velocity_bis
