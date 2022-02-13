import pygame

from pygame.locals import *

class Scrollbar:
     
     def __init__(self , panel , side=False):
          
          self.panel_ref = panel
          self.side = side
          
          if not side:
               self.scroll_rect = Rect([self.panel_ref.rect.width - 20 , 0],[20 , self.panel_ref.rect.height])
               self.bar_rect = Rect([self.scroll_rect.x , self.scroll_rect.y] , [20 , 50])
          else:
               self.scroll_rect = Rect([0 , self.panel_ref.rect.height - 20],[self.panel_ref.rect.width , 20])
               self.bar_rect = Rect([self.scroll_rect.x , self.scroll_rect.y] , [50 , 20])
     
          self.on_bar = False
          self.mouse_diff = 0
          
          #y true surface difference
          self.ts_diff = 0
          self.change = 0
          
          self.scrollbar_hid = False
     
     def update(self):
          
          self.ts_diff += self.change
          
          if not self.side:
          
               ptsh = self.panel_ref.true_surface.get_rect().height
               height_diff = ptsh - self.scroll_rect.height
               
               if height_diff <= 0:
                    self.scrollbar_hid = True
                    return
               else:
                    self.scrollbar_hid = False
               
               if self.ts_diff > 0:
                    self.ts_diff = 0
               elif self.ts_diff + ptsh < self.panel_ref.rect.height:
                    self.ts_diff = height_diff
               
               self.bar_rect.height = int(self.scroll_rect.height / (ptsh / self.scroll_rect.height))
               
               bar_half_lenght = self.bar_rect.height / 2
               scroll_length = self.scroll_rect.height - self.bar_rect.height
               
               if self.on_bar:
                    mouse_pos = pygame.mouse.get_pos()
                    self.bar_rect.y = mouse_pos[1] - self.mouse_diff
                    
                    if self.bar_rect.y < self.scroll_rect.y:
                         self.bar_rect.y = 0
                    elif self.bar_rect.bottom > self.scroll_rect.height:
                         self.bar_rect.bottom = self.scroll_rect.height
                    
                    self.ts_diff = int((height_diff / scroll_length) * (self.bar_rect.centery - bar_half_lenght) * -1)
               else:
                    self.bar_rect.centery =  scroll_length / (height_diff * 1.0) * (self.ts_diff * -1) + bar_half_lenght
          
          else:
               # panel_true_surface_height
               ptsw = self.panel_ref.true_surface.get_rect().width
               width_diff = ptsw - self.scroll_rect.width
               
               if width_diff <= 0:
                    self.scrollbar_hid = True
                    return
               else:
                    self.scrollbar_hid = False
               
               if self.ts_diff > 0:
                    self.ts_diff = 0
               elif self.ts_diff + ptsw < self.panel_ref.rect.width:
                    self.ts_diff = width_diff
               
               self.bar_rect.width = int(self.scroll_rect.width / (ptsw / self.scroll_rect.width))
               
               bar_half_length = self.bar_rect.width / 2
               scroll_length = self.scroll_rect.width - self.bar_rect.width
               
               if self.on_bar:
                    mouse_pos = pygame.mouse.get_pos()
                    self.bar_rect.x = mouse_pos[0] - self.mouse_diff
                    
                    if self.bar_rect.x < self.scroll_rect.x:
                         self.bar_rect.x = 0
                    elif self.bar_rect.right > self.scroll_rect.width:
                         self.bar_rect.right = self.scroll_rect.width
                    
                    self.ts_diff = int((width_diff / scroll_length) * (self.bar_rect.centerx - bar_half_length) * -1)
               else:
                    self.bar_rect.centerx =  scroll_length / (width_diff * 1.0) * (self.ts_diff * -1) + bar_half_length
               
     
     def event_handler(self , event , zone_offset=[0,0]):
          
          if not self.scrollbar_hid: 
               if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                         true_coord = Rect([self.bar_rect.x+self.panel_ref.rect.x+zone_offset[0] , self.bar_rect.y+self.panel_ref.rect.y+zone_offset[1]] , self.bar_rect.size)
                         if true_coord.collidepoint(event.pos):
                              self.on_bar = True
                              self.mouse_diff = event.pos[0] - self.bar_rect.left if self.side else event.pos[1] - self.bar_rect.top
               if event.type == MOUSEBUTTONUP:
                    self.on_bar = False
          
          # if event.type == KEYDOWN:
          #      if event.key == K_UP:
          #           self.change_y = 5
          #      elif event.key == K_DOWN:
          #           self.change_y = -5
                
          # if event.type == KEYUP:
          #      if event.key == K_UP:
          #           self.change_y = 0
          #      elif event.key == K_DOWN:
          #           self.change_y = 0
     
     def display(self , surface):
          
          scroll_surface = pygame.Surface(self.scroll_rect.size , SRCALPHA)
          scroll_surface.fill([255 , 255 , 255 , 10])
          
          if not self.scrollbar_hid:
               bar_surface = pygame.Surface(self.bar_rect.size , SRCALPHA)
               bar_surface.fill([230 , 230 , 230 , 100])
               
               surface.blit(scroll_surface , [self.scroll_rect.x , self.scroll_rect.y])
               surface.blit(bar_surface , [self.bar_rect.x , self.bar_rect.y])
          else:
               surface.blit(scroll_surface , [self.scroll_rect.x , self.scroll_rect.y])