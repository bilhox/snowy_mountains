import pygame
import pyperclip
import ui_data

from text import *
from pygame.locals import *

class Label():
     
     def __init__(self , pos : tuple , font_size : int , string_parameter):
          
          """
          string_parameter is a dictionnary with all parameters of the string
          Required key : stringValue
          """
          
          self.pos = pos
          self.stringValue = string_parameter["stringValue"]
          self.color = string_parameter["color"] if "color" in string_parameter else [0,0,0]
          
          self.font = pygame.font.Font("./fonts/Readex_Pro/static/ReadexPro-Medium.ttf", font_size )
     
     def event_handler(self , event):
          pass
     
     def change_font(self , font_size : int):
          self.font = pygame.font.Font("./fonts/Readex_Pro/static/ReadexPro-Medium.ttf", font_size )
     
     def display(self , surface):
          
          surface.blit(self.font.render(self.stringValue , True , self.color) , self.pos)


class Entry:
     
     def __init__(self , name : str , pos : tuple , size : tuple , text_color=[0,0,0]):
          
          self.name = name
          
          self.rect = Rect(pos , size)
          self.texture = pygame.Surface(size , SRCALPHA)
          self.texture.fill([58, 42, 142, 0.64*128])
          
          self.stringValue = ""
          self.writing = False
          self.cursor = 0
          self.cursor_displayed = True
          
          self.default_text = "Enter text"
          self.max_lenght = 200
          self.extra_string = ""
          self.text_color = text_color
          
          self.font = pygame.font.Font("./fonts/Readex_Pro/static/ReadexPro-Regular.ttf", 14 )
          
          self.key_pressed = None
          self.timing = 0
          self.interval = [150 , 8 , False]
     
     def event_handler(self , event : pygame.event.Event , entry_zone_offset=[0,0]):
          
          if self.writing and self.key_pressed != None:
               self.timing += 1
               if not self.interval[2]:
                    if (self.timing % self.interval[0]) == 0:
                         self.timing = 0
                         self.interval[2] = True
               elif self.interval[2] and (self.timing % self.interval[1]) == 0:
                    self.timing = 0
                    
                    if self.key_pressed[0] == (K_BACKSPACE or K_DELETE):
                         self.stringValue = self.stringValue[:self.cursor-1]+self.stringValue[self.cursor:] if not self.cursor <= 0 else self.stringValue
                         self.cursor -= 1
                    
                    if self.key_pressed[1] in "abcdefghijklmnopqrstuvwxyz":
                         self.stringValue = self.stringValue[:self.cursor] + self.key_pressed[1] + self.stringValue[self.cursor:]
                         self.cursor += 1
                         
          
          if event.type == MOUSEBUTTONDOWN:
               if self.rect.x + entry_zone_offset[0] < event.pos[0] < self.rect.right + entry_zone_offset[0] and self.rect.y + entry_zone_offset[1] < event.pos[1] < self.rect.bottom + entry_zone_offset[1]:
                    self.writing = True
               else:
                    self.writing = False
          
          elif event.type == KEYDOWN and self.writing == True:
               self.key_pressed = (event.key , event.unicode)
               if event.key == (K_BACKSPACE or K_DELETE):
                    self.stringValue = self.stringValue[:self.cursor-1]+self.stringValue[self.cursor:] if not self.cursor <= 0 else self.stringValue
                    self.cursor -= 1
               elif event.key == K_RETURN:
                    self.writing = False
               elif (event.key == K_v and pygame.key.get_mods() & KMOD_CTRL):
                    pasted = pyperclip.paste()
                    self.stringValue = self.stringValue[:self.cursor]+pasted+self.stringValue[self.cursor:]
                    self.cursor += len(pasted)
               elif event.key == K_RIGHT:
                    self.cursor += 1
               elif event.key == K_LEFT:
                    self.cursor -= 1
               elif event.unicode in " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/\\-_.éàèù" and event.unicode != "" and len(self.stringValue) < self.max_lenght:
                    self.stringValue = self.stringValue[:self.cursor] + event.unicode + self.stringValue[self.cursor:]
                    self.cursor += 1
          
          elif event.type == KEYUP:
               self.key_pressed = None
               self.interval[2] = False
               
          if self.cursor > len(self.stringValue):
                    self.cursor -= 1
          elif 0 > self.cursor:
               self.cursor += 1
     
     def change_background_color(self , color):
          
          self.texture.fill(color)
     
     def display(self , screen):
          
          final_surf = self.texture.copy()
          text_offset = (self.font.size(self.stringValue[:self.cursor]+self.extra_string)[0] + 1 - self.rect.width) if self.font.size(self.stringValue[:self.cursor]+self.extra_string)[0] > self.rect.width else 0
          
          if self.stringValue != "":
               pygame.draw.line(final_surf, self.text_color, (self.font.size(self.stringValue[:self.cursor])[0]  + 1 - text_offset , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2), (self.font.size(self.stringValue[:self.cursor])[0] + 1 - text_offset , self.rect.height // 2 + self.font.size(self.stringValue)[1] // 2), 2) if self.writing else None
               final_surf.blit(self.font.render(self.stringValue+self.extra_string , True , self.text_color) , [1 - text_offset , self.rect.height // 2 - self.font.size(self.stringValue)[1] // 2])
          else:
               text_size = self.font.size(self.default_text)
               final_surf.blit(self.font.render(self.default_text , True , self.text_color) , [self.rect.width // 2 - text_size[0] // 2 , self.rect.height // 2 - text_size[1] // 2])
          screen.blit(final_surf , [self.rect.x , self.rect.y])

class Button():
     
     def __init__(self , name : str , pos : tuple , size : tuple , stringParameter : dict , target_arguments={}):
          
          self.surf_rect = Rect(pos , size)
          self.event_rect = self.surf_rect.copy()
          self.textures = [pygame.Surface(self.surf_rect.size , SRCALPHA),pygame.Surface(self.surf_rect.size , SRCALPHA),pygame.Surface(self.surf_rect.size , SRCALPHA)]
          
          self.textures[0].fill([58, 42, 142, 0.25*128])
          self.textures[1].fill([58, 42, 142, 0.64*128])
          self.textures[2].fill([58, 42, 142, 0.9*128])
          
          self.target = None
          
          self.align_center = stringParameter["align center"] if "align center" in stringParameter else False
          
          padd_left = stringParameter["padding left"] if "padding left" in stringParameter else 0
          padd_top = stringParameter["padding top"] if "padding top" in stringParameter else 0
          
          self.padding = [padd_left , padd_top]
          self.color = stringParameter["color"] if "color" in stringParameter else [0,0,0]
          self.stringValue = stringParameter["stringvalue"]
          self.name = name
          self.case = 0
          self.target_arguments = target_arguments
          
          self.main_texture = None
          self.logo = None
          
          self.font = Font("./data/fonts/large_font.png" , self.color)
          
          self.load_textures()
     
     def set_fontColor(self , color : list[int , int , int]):
          self.font = Font("./data/fonts/large_font.png" , color)
          self.color = color.copy()
     
     def load_textures(self):
          
          button_key = self.name
          main_texture = None
          logo = None
          if button_key in ui_data.imgs["button"]:
               try:
                    main_texture = pygame.image.load(ui_data.imgs["button"][button_key]["texture"]).convert_alpha()
                    if ui_data.imgs["button"][button_key]["logo"] != "":
                         try:
                              logo = pygame.image.load(ui_data.imgs["button"][button_key]["logo"]).convert_alpha()
                         except:
                              pass
               except:
                    pass
          
          if main_texture == None:
               return
          
          self.main_texture = main_texture
          self.logo = logo
          
          for texture in self.textures:
               texture.blit(main_texture,[0,0])
               if logo != None:
                    texture.blit(logo , [4,4])
          
     def change_background_color(self , colors):
          
          a = 0
          for texture in self.textures:
               texture.fill(colors[a])
               if self.main_texture != None:
                    texture.blit(self.main_texture , [0,0])
                    if self.logo != None:
                         texture.blit(self.logo , [0,0])
               a+=1
               
          
     def event_handler(self , event : pygame.event.Event , button_zone_offset=[0,0]):
               
          if event.type == MOUSEBUTTONDOWN and event.button == 1:
               if self.event_rect.x + button_zone_offset[0] < event.pos[0] < self.event_rect.right + button_zone_offset[0] and self.event_rect.y + button_zone_offset[1] < event.pos[1] < self.event_rect.bottom + button_zone_offset[1]:
                    if self.target_arguments != None and self.target != None:
                         self.target(**self.target_arguments) if isinstance(self.target_arguments , dict) else self.target(self.target_arguments)
                    elif self.target != None:
                         self.target()
                    self.case = 2
          elif event.type == MOUSEBUTTONUP and event.button == 1:
               if self.event_rect.x + button_zone_offset[0] < event.pos[0] < self.event_rect.right + button_zone_offset[0] and self.event_rect.y + button_zone_offset[1] < event.pos[1] < self.event_rect.bottom + button_zone_offset[1]:
                    self.case = 1
          elif event.type == MOUSEMOTION:
               if self.event_rect.x + button_zone_offset[0] < event.pos[0] < self.event_rect.right + button_zone_offset[0] and self.event_rect.y + button_zone_offset[1] < event.pos[1] < self.event_rect.bottom + button_zone_offset[1]:
                    self.case = 1
               else:
                    self.case = 0
                    
     
     def display(self , screen):
          
          final_texture = self.textures[self.case].copy()
          if self.align_center or (self.padding[0] == 0 and self.padding[1] == 0):
               self.font.render(self.stringValue , final_texture , [self.surf_rect.width // 2 - self.font.width(self.stringValue) // 2 , self.surf_rect.height // 2 - self.font.line_height // 2])
          else:
               x_dist = self.padding[0] if self.padding[0] != 0 else self.surf_rect.width // 2 - self.font.width(self.stringValue) // 2
               y_dist = self.padding[1] if self.padding[1] != 0 else self.surf_rect.height // 2 - self.font.line_height // 2
               
               self.font.render(self.stringValue , final_texture , [x_dist , y_dist])
          screen.blit(final_texture , [self.surf_rect.x , self.surf_rect.y])

class Selector(Button):
     
     def __init__(self, name : str, pos : tuple , size : tuple , stringParameter : dict , value):
          super().__init__(name , pos , size , stringParameter , None)
          
          self.font = pygame.font.Font("./fonts/Readex_Pro/static/ReadexPro-Medium.ttf" , 12)
          
          self.selected = False
          self.value = value
     
     def event_handler(self, event: pygame.event.Event , button_zone_offset=[0, 0]):
          if event.type == MOUSEBUTTONDOWN and event.button == 1:
               true_rect = Rect([self.surf_rect.x+button_zone_offset[0],self.surf_rect.y+button_zone_offset[1]],self.surf_rect.size)
               if true_rect.collidepoint(event.pos):
                    if (self.value and self.target) != None:
                         self.target(self.value)
                    self.selected = True
               else:
                    self.selected = False
                    self.case = 0
                    
          
          if self.selected:
               self.case = 2
          else:
               self.case = 0   