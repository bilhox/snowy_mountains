import pygame
import os 

from xml.etree.ElementTree import *
from pygame.locals import *
from unclassed_functions import *
from particles import *

PIC_TRAP_TILE_ID = 41

class TileMap:
     
     def __init__(self , ts_path , map_path):
          
          self.tiles = {}
          self.ts_path = ts_path
          self.size = []
          self.map_path = map_path
          self.change_zones = []
          self.texts = []
          self.colliders = {}
          self.camera_properties = {}
          
          ts_parser = parse(ts_path)
          for tile in ts_parser.getroot().findall("tile"):
               path = tile.find("image").get("source")
               path = path.replace(".." , "./data")
               img = pygame.image.load(path).convert_alpha()
               self.tiles[str(int(tile.get("id"))+1)] = img
          
          self.layers = {}
          
          map_parser = parse(map_path)
          self.size = [int(map_parser.getroot().get("width"))*16 , int(map_parser.getroot().get("height"))*16]
          for n , layer in enumerate(map_parser.findall("layer")):
               map_data = layer.find("data")
               map_text = map_data.text.split("\n")
               
               if layer.get("name") == "colliders":
                    map_tab = []
                    for line in map_text:
                         if not line == "":
                              linebis = line.split(",")
                              l = []
                              for value in linebis:
                                   if not value == "":
                                        l.append(value)
                              map_tab.append(l)
                    yBis = 0
                    for h in range(0,(self.size[1]//16)//8):
                         xBis = 0
                         for w in range(0,(self.size[0]//16)//8):
                              chunk = {}
                              chunk["rect"] = Rect([w*16*8,h*16*8],[8*16,8*16])
                              colliders = []
                              for y in range(h*8,h*8+8):
                                   for x in range(w*8,w*8+8):
                                        if map_tab[y][x] != "0":
                                             colliders.append(Rect([x*16 , y*16],[16,16]))
                              chunk["data"] = colliders
                              self.colliders[f"chunk_{xBis},{yBis}"] = chunk
                              xBis+=1
                         yBis+=1
               
               elif layer.get("name") == "torches":
                    map_tab = []
                    for line in map_text:
                         if not line == "":
                              linebis = line.split(",")
                              l = []
                              for value in linebis:
                                   if not value == "":
                                        l.append(value)
                              map_tab.append(l)
                              
                    chunks = {}
                    a = 0
                    for h in range(0,(self.size[1]//16)//8):
                         for w in range(0,(self.size[0]//16)//8):
                              chunk = {}
                              chunk["rect"] = Rect([w*16*8,h*16*8],[8*16,8*16])
                              torches = []
                              for y in range(h*8,h*8+8):
                                   for x in range(w*8,w*8+8):
                                        if map_tab[y][x] != "0":
                                             torch = Torch([x*16 , y*16])
                                             torch.layer = n
                                             torch.particle_system.particle_size = [1,1]
                                             torch.particle_system.max_speed = [0.1 , 1]
                                             torch.particle_system.max_time = 20
                                             torch.particle_system.spawn_coef = 1
                                             torches.append(torch) 
                              chunk["data"] = torches
                              chunks[f"chunk_{a}"] = chunk
                              a+=1
                                   
                    self.layers[layer.get("name")] = {"special_type":"torches","chunks":chunks}         
               else:
                    map_tab = []
                    for line in map_text:
                         if not line == "":
                              linebis = line.split(",")
                              l = []
                              for value in linebis:
                                   if not value == "":
                                        l.append(value)
                              map_tab.append(l)
                              
                    chunks = {}
                    a = 0
                    for h in range(0,(self.size[1]//16)//8):
                         for w in range(0,(self.size[0]//16)//8):
                              chunk = {}
                              chunk["rect"] = Rect([w*16*8,h*16*8],[8*16,8*16])
                              tile_list = []
                              for y in range(h*8,h*8+8):
                                   for x in range(w*8,w*8+8):
                                        if map_tab[y][x] != "0":
                                             tile_list.append(Tile([x*16 , y*16] , self.tiles[str(map_tab[y][x])]))
                              chunk["data"] = tile_list
                              chunks[f"chunk_{a}"] = chunk
                              a+=1
                    
                    self.layers[layer.get("name")] = {"special_type":"","chunks":chunks}
          
          for object_layer in map_parser.findall("objectgroup"):
               
               for object in object_layer.findall("object"):
                    
                    if object.get("type") == "change_zone":
                         properties = {}
                         for property in object.find("properties").findall("property"):
                              properties[property.get("name")] = property.get("value")
                         
                         zone = Rect(float(object.get("x")) // 1 , float(object.get("y")) // 1 , float(object.get("width")) // 1 , float(object.get("height")) // 1)
                         spawnpoint = properties["spawnpoint"].split(",")
                         spawnpoint = [float(spawnpoint[0])*16 , float(spawnpoint[1])*16]
                         self.change_zones.append( {"zone":zone , "next_map":properties["next_map"] , "spawnpoint":spawnpoint} )
                    
                    if object.get("type") == "text":
                         properties = {}
                         for property in object.find("properties").findall("property"):
                              properties[property.get("name")] = property.get("value")
                         
                         self.texts.append([
                              properties["text"],
                              [int(object.get("x")) , int(object.get("y"))]
                         ])

          for property in map_parser.find("properties").findall("property"):
               
               if property.get("name").split("_")[0] == "camera":
                    
                    if property.get("type") == "int":
                         self.camera_properties[property.get("name").split("_")[1]] = int(property.get("value"))
     
     def get_colliders(self , scroll):
          
          colliders = []
          
          for chunk in self.colliders.values():
               # print(Rect([chunk["rect"].x - scroll[0],chunk["rect"].y - scroll[1]],chunk["rect"].size))
               if not isOutOfRange(Rect([chunk["rect"].x - scroll[0],chunk["rect"].y - scroll[1]],chunk["rect"].size)):
                    for collider in chunk["data"]:
                         colliders.append(collider)
          
          return colliders
                         
class Map_Manager():
     
     def __init__(self , directory_path : str , ts_path : str):
          
          self.maps = {}
          
          for file in os.listdir(directory_path):
               map = TileMap(ts_path , directory_path+"/"+file)
               self.maps[os.path.splitext(file)[0]] = map
          
          self.current_map_id = ""


class Tile:
     
     def __init__(self , pos , img , type=None):
          self.x = pos[0]
          self.y = pos[1]
          self.img = img
          self.type = type

class Torch():
     
     tile_number = 33
     
     def __init__(self , pos):
          
          self.pos = pos
          self.layer = 1
          self.texture = pygame.image.load("./data/tiles/torch.png")
          self.particle_system = Particle_system([self.pos[0]+8 , self.pos[1]+4],color=[214, 79, 51])
          self.torch_sin = 1
     
     def update(self , game_time):
          self.particle_system.update()
          self.torch_sin = sin((self.pos[1] % 100 + 200) / 300 * game_time * 0.01)
     
     def display(self , surface , scroll):
     
          surface.blit(self.texture , [self.pos[0]-scroll[0],self.pos[1]-scroll[1]])
          blit_center_add(surface, circle_surf(10 + (self.torch_sin + 3) * 8.5, (4 + (self.torch_sin + 4) * 0.3, 4 + (self.torch_sin + 4) * 0.5, 4 + (self.torch_sin + 4) * 0.9)), (self.pos[0] - scroll[0] + 6, self.pos[1] - scroll[1] + 4))
          blit_center_add(surface, circle_surf(9 + (self.torch_sin + 3) * 4, (8 + (self.torch_sin * 1.3 + 4) * 0.3, 8 + (self.torch_sin + 4) * 0.5, 8 + (self.torch_sin + 4) * 0.9)), (self.pos[0] - scroll[0] + 6, self.pos[1] - scroll[1] + 4))
          self.particle_system.display(surface , scroll)

class Collider:
     
     rect : Rect
     tile_pos : list[int , int]
               