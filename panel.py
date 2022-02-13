import pygame
import scrollbar
import ui_data

from ui import *
from pygame.locals import *

class SList():
     
     def __init__(self , pos , size , scrollbar_side=False):
          
          self.rect = Rect([pos[0] , pos[1]] , size)
          
          self.color = [0,0,0]
          
          self.scrollbar = scrollbar.Scrollbar(self , scrollbar_side)
          
          self.true_surface = pygame.Surface(self.rect.size)
     
     def update(self):
          
          self.scrollbar.update()
          
     def event_handler(self , event , zone_offset=[0,0]):
          
          self.scrollbar.event_handler(event , [zone_offset[0],zone_offset[1]])
     
     def display(self , surface):
          
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill([13, 0, 94])
          
          final_surface.blit(self.true_surface , [0 , self.scrollbar.ts_diff]) if not self.scrollbar.side else final_surface.blit(self.true_surface , [self.scrollbar.ts_diff , 0])
          
          self.scrollbar.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

class Selector_list(SList):
     
     def __init__(self , pos , size , scrollbar_side=False):
          
          super().__init__(pos , size , scrollbar_side)
          
          self.selectors = []
          self.selector_size = 20
     
     def update(self):
          super().update()
     
     def event_handler(self, event , offset=[0,0]):
          super().event_handler(event , offset)
          true_rect = Rect([self.rect.x+offset[0] , self.rect.y+offset[1]],self.rect.size)
          if event.type == (MOUSEBUTTONDOWN or MOUSEBUTTONUP) and not true_rect.collidepoint(event.pos):
               return
          for selector in self.selectors:
               selector.event_handler(event , [self.rect.x+offset[0] , self.rect.y+offset[1]+self.scrollbar.ts_diff] if not self.scrollbar.side else [self.rect.x+offset[0]+self.scrollbar.ts_diff , self.rect.y+offset[1]])
               

     def display(self, surface):
          
          tsh = len(self.selectors) * self.selector_size
          
          true_surface = pygame.Surface([self.rect.width , tsh])
          true_surface.fill(self.color)
          
          for index , selector in enumerate(self.selectors):
               if not self.scrollbar.side:
                    selector.rect.y = index * self.selector_size
               else:
                    selector.rect.x = index * self.selector_size
               selector.display(true_surface)
          
          self.true_surface = true_surface
               
          final_surface = pygame.Surface(self.rect.size)
          final_surface.fill(self.color)
          
          if not self.scrollbar.scrollbar_hid:
               final_surface.blit(self.true_surface , [0 , self.scrollbar.ts_diff]) if not self.scrollbar.side else final_surface.blit(self.true_surface , [self.scrollbar.ts_diff , 0])
               self.scrollbar.display(final_surface)
          else:
               self.scrollbar.ts_diff = 0
               final_surface.blit(self.true_surface , [0 , 0])
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])
               
class UI_panel():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          self.components = {}
          
          self.texture = pygame.Surface(self.rect.size)
          self.texture.fill([26, 31, 56])
     
     def event_handler(self , event : pygame.event.Event , offset=[0,0]):
          
          for component in self.components.values():
               component.event_handler(event , [self.rect.x+offset[0] , self.rect.y+offset[1]])
     
     def display(self , surface):
          
          final_surface = self.texture.copy()
          
          for component in self.components.values():
               component.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

class Settings_bar(UI_panel):
     
     def __init__(self, pos, size):
          super().__init__(pos, size)
     
     def load_textures(self):
          colors = [[255, 166, 71, 0.25*128],[255, 166, 71, 0.64*128],[255, 166, 71, 0.9*128]]
          
          for component in self.components.values():
               if isinstance(component , Button):
                    component.change_background_color(colors)
     

class UI_panel_with_selectors():
     
     def __init__(self , pos , size):
          
          self.rect = Rect(pos , size)
          self.selectors = []
          self.panels = {}
          
          self.texture = pygame.Surface(self.rect.size)
          self.texture.fill([37, 44, 79])
          
          self.actual_panel = None
          
     def create_panel(self , name : str):
          selector = Button(name,[len(self.selectors)*100,0],[100 , 30],{"stringvalue":name,"align center":True , "color":[255 , 255 , 255]} , target_arguments=name)
          selector.target = self.set_panel
          self.selectors.append(selector)
          self.panels[name] = UI_panel([0 , 30] , [self.rect.width , self.rect.height - 30])
     
     def load_textures(self):
          
          for panel_name , panel in self.panels.items():
               
               for name , component in panel.components.items():
                    
                    if isinstance(component , Button):
                         pass
          
     
     def set_panel(self , name):
          self.actual_panel = self.panels[name]
     
     def event_handler(self , event : pygame.event.Event):
          
          for selector in self.selectors:
               selector.event_handler(event , [self.rect.x , self.rect.y])
          
          if self.actual_panel is not None:     
               self.actual_panel.event_handler(event , [self.rect.x , self.rect.y])
               
     def display(self , surface):
          
          final_surface = self.texture.copy()
          
          for selector in self.selectors:
               selector.display(final_surface)
          
          if self.actual_panel is not None:
               self.actual_panel.display(final_surface)
          
          surface.blit(final_surface , [self.rect.x , self.rect.y])

     