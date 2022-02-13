import pygame
import sys
import mapping

from entity import *
from ui import *
from panel import *
from text import *
from pygame.locals import *
from animation import *
from particles import *
from random import *
from unclassed_functions import *
     
pygame.init()
SCREEN_SIZE = [700,500]
DISPLAY_SIZE = [350 , 250]
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snowy mountains")
clock = pygame.time.Clock()
dt = 1

class Camera():
     
     def __init__(self , display_size : list[int , int]):
          
          self.initial_display_size = display_size
          self.display_size = self.initial_display_size.copy()
          self.zoom = 1
          self.display_surface = pygame.Surface(self.display_size , SRCALPHA)
          self.true_scroll = [0,0]
          self.scroll = self.true_scroll.copy()
          self.static = False
          self.white_font = Font("./data/fonts/small_font.png" , [255,255,255])
          self.black_font = Font("./data/fonts/small_font.png" , [0,0,1])
          self.screen_shake = 0
          self.screen_shake_data = {"basexOffset":[0,0],"baseyOffset":[0,0],"xOffset":[0,0],"yOffset":[0,0],"duration":1}
     
     def update(self , dt):
          if self.screen_shake > 0:
               self.screen_shake -= 1 * dt
               self.screen_shake_data["xOffset"][0] += max(self.screen_shake_data["basexOffset"][0] / self.screen_shake_data["duration"] , 0)
               self.screen_shake_data["xOffset"][1] -= max(self.screen_shake_data["basexOffset"][0] / self.screen_shake_data["duration"] , 0)
               self.screen_shake_data["yOffset"][0] += max(self.screen_shake_data["baseyOffset"][0] / self.screen_shake_data["duration"] , 0)
               self.screen_shake_data["yOffset"][1] -= max(self.screen_shake_data["baseyOffset"][0] / self.screen_shake_data["duration"] , 0)
               
     
     def set_zoom(self , zoom : float):
          self.zoom = min(zoom , 2)
          self.display_size = [int(self.initial_display_size[0] / self.zoom) , int(self.initial_display_size[1] / self.zoom)]
     
     def shake(self , duration : float , xOffset : list , yOffset : list):
          self.screen_shake = duration
          self.screen_shake_data["basexOffset"] = xOffset.copy()
          self.screen_shake_data["baseyOffset"] = yOffset.copy()
          self.screen_shake_data["yOffset"] = yOffset.copy()
          self.screen_shake_data["xOffset"] = xOffset.copy()
          self.screen_shake_data["duration"] = duration
     
     def get_scroll(self):
          
          render_offset = [0,0]
          
          if self.screen_shake > 0:
               render_offset[0] = randint(self.screen_shake_data["xOffset"][0] , self.screen_shake_data["xOffset"][1])
               render_offset[1] = randint(self.screen_shake_data["yOffset"][0] , self.screen_shake_data["yOffset"][1])
          
          return [self.scroll[0] + render_offset[0] , self.scroll[1] + render_offset[1]]
     
     def set_scroll(self , scroll : list[int , int]):
          
          self.true_scroll = scroll.copy()
          self.scroll = [int(self.true_scroll[0]) , int(self.true_scroll[1])]
     
     def display(self):
          
          pos = [self.initial_display_size[0] // 2 - self.display_size[0] // 2 , self.initial_display_size[1] // 2 - self.display_size[1] // 2]
          if self.zoom != 1:     
               display_surface = pygame.transform.scale(self.display_surface.subsurface(Rect(pos,self.display_size)) , self.initial_display_size)
               self.black_font.render(f"FPS : {int(clock.get_fps())}" , display_surface , [3 , 3])
               self.white_font.render(f"FPS : {int(clock.get_fps())}" , display_surface , [2 , 2] )
               screen.blit(pygame.transform.scale(display_surface , SCREEN_SIZE),[0,0])
          else:
               self.black_font.render(f"FPS : {int(clock.get_fps())}" , self.display_surface , [3 , 3])
               self.white_font.render(f"FPS : {int(clock.get_fps())}" , self.display_surface , [2 , 2])
               screen.blit(pygame.transform.scale(self.display_surface , SCREEN_SIZE),[0,0])
          
          # render_offset = [0,0]
          
          # if self.screen_shake > 0:
          #      render_offset[0] = randint(self.screen_shake_data["xOffset"][0] , self.screen_shake_data["xOffset"][1])
          #      render_offset[1] = randint(self.screen_shake_data["yOffset"][0] , self.screen_shake_data["yOffset"][1])
          
     
     

camera = Camera(DISPLAY_SIZE)

class Scene:
     
     def start(self):
          pass
     
     def Update(self):
          self.event_handler()
     
     def event_handler(self):
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
     
     def display(self):
          pass

class Game_scene(Scene):
     
     def __init__(self):
          self.white_font = Font("./data/fonts/small_font.png" , [255,255,255])
          self.black_font = Font("./data/fonts/small_font.png" , [0,0,1])
          self.large_font = Font("./data/fonts/large_font.png" , [255,255,255])
          self.entities = []
          self.maxn_entity = 30
          self.spawnpoint = [10*16 , 58*16]

          player_animManager = AnimationManager("./data/animations/player")
          self.player = Player(self.spawnpoint.copy(),[6 , 18],anim_Manager=player_animManager)
          self.player.texture_size = [12 , 18]
          self.player.add_texture("jumping" , "./data/imgs/player/jumping_pos/pos_1.png")
          self.player.add_texture("falling" , "./data/imgs/player/jumping_pos/pos_2.png")

          self.focused_entity = self.player
          self.game_timer = 0
          # player zone which camera not follow
          self.cam_znf = Rect([camera.initial_display_size[0] // 2 - 50 , camera.initial_display_size[1] // 2 - 25],[100 , 50])
          self.mode = 1
          self.dt = 1
          self.map_manager = mapping.Map_Manager("./data/tilemaps" , "./data/tilesets/tileset_1.tsx")
          self.map_manager.current_map_id = "map_1"
          self.change_zone = Rect([57*16 , 57*16],[5*16 , 4*16])
          self.viewmode_keys = {"left":False , "right":False ,"top":False ,"bottom":False}
          self.backgrounds = [
          [pygame.image.load("./data/background.png") , [0.01 , 0.02]],
          [pygame.image.load("./data/mountains.png") , [0.09 , 0.15]],
          ]
          self.music = "./data/musics/snow_about_a_castle.mp3"
          self.dt = 1
          
          self.tt_layer = 1
          self.tutorial_texts = [
               ["Press right and left keys for moving !" , [7 , 58] , [7*16 , 58*16] , "up"],
               ["Press up key for jumping !" , [27 , 51] , [27*16 , 51*16] , "down"]
          ]
          
          snow_particle = pygame.image.load("./data/imgs/snow_particle.png").convert_alpha()
          
          self.snow_psystem = Zone_psystem(Rect([0,0],self.map_manager.maps[self.map_manager.current_map_id].size),snow_particle)
          self.snow_psystem.max_time = 3000
          self.snow_psystem.cooldown = 3
          self.snow_psystem.max_particle = 200
          self.snow_psystem.direction = [0 , -1]
          self.snow_psystem.speed = 0.1
          self.snow_psystem.spawn_coef = 1
          
          self.beginning_zoom = 2
          self.dezooming_coef = 0.1
          self.dezooming = True
          
          self.changing_zone = False
     
     def start(self):
          pygame.mixer.music.load(self.music)
          pygame.mixer.music.play(loops=1000)
          pygame.mixer.music.set_volume(1)
          
          f_rect = self.focused_entity.rect
          
          camera.set_scroll([(f_rect.x - camera.initial_display_size[0] // 2 - f_rect.w // 2) , (f_rect.y - camera.initial_display_size[1] // 2 - f_rect.h // 2)])
          camera.set_zoom(self.beginning_zoom)
     
     def Update(self):
          self.event_handler()
          self.update()
          self.display()
     
     def change_map(self , id , spawn_point):
          self.map_manager.current_map_id = id
          self.player.set_pos(spawn_point)
          self.player.able_to_move = True
          
          map = self.map_manager.maps[self.map_manager.current_map_id]
          
          if map.camera_properties["movement"] == 0:
               camera.static = True
               camera.set_scroll([map.size[0] // 2  - camera.initial_display_size[0] // 2 , map.size[1] // 2 - camera.initial_display_size[1] // 2])
          else:
               camera.static = False
          
     def event_handler(self):
          global current_id
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
               if event.type == KEYDOWN:
                    if event.key == K_z:
                         self.mode = 0 if self.mode == 1 else 1
                         if not self.mode:
                              self.player.able_to_move = False
                         else:
                              self.player.able_to_move = True
                              for key in self.viewmode_keys:
                                   self.viewmode_keys[key] = False
                    if not self.mode:
                         if event.key == K_RIGHT:
                              self.viewmode_keys["right"] = True
                         elif event.key == K_LEFT:
                              self.viewmode_keys["left"] = True
                         if event.key == K_UP:
                              self.viewmode_keys["top"] = True
                         elif event.key == K_DOWN:
                              self.viewmode_keys["bottom"] = True
                    if event.key == K_n:
                         camera.set_zoom(2)
               if event.type == KEYUP:
                    if not self.mode:
                         if event.key == K_RIGHT:
                              self.viewmode_keys["right"] = False
                         elif event.key == K_LEFT:
                              self.viewmode_keys["left"] = False
                         if event.key == K_UP:
                              self.viewmode_keys["top"] = False
                         elif event.key == K_DOWN:
                              self.viewmode_keys["bottom"] = False
                    if event.key == K_p:
                         # print(self.player.rect.x // 16 , self.player.rect.y // 16)
                         camera.shake(1 , [0 , 0] , [-2 , 2])
                    if event.key == K_o:
                         if self.mode:
                              self.player.set_pos(self.spawnpoint.copy())
                    if event.key == K_n:
                         camera.set_zoom(1)
               if self.mode: 
                    self.player.event_handler(event)

     def update(self):
          global dt , transition
          game_map = self.map_manager.maps[self.map_manager.current_map_id]
          self.game_timer += dt
          # self.snow_psystem.update(self.game_timer)
          if transition:
               self.player.able_to_move = False
          else:
               self.player.able_to_move = True
          if self.dezooming and self.game_timer > 2:
               self.beginning_zoom -= self.dezooming_coef
               self.dezooming_coef *= 0.92
               if self.beginning_zoom < 1:
                    camera.set_zoom(1)
                    self.dezooming = False
               else:
                    camera.set_zoom(self.beginning_zoom)
          #camera
          if not self.mode:
               if self.viewmode_keys["right"]:
                    camera.true_scroll[0] += 2
               elif self.viewmode_keys["left"]:
                    camera.true_scroll[0] -= 2
               if self.viewmode_keys["top"]:
                    camera.true_scroll[1] -= 2
               elif self.viewmode_keys["bottom"]:
                    camera.true_scroll[1] += 2
               
          
          # entity updates
          self.player.update(dt)
          for entity in self.entities:
               entity.update(dt , camera.scroll)
               
          if self.mode:
               self.player.move(game_map.get_colliders(camera.scroll)) 
               for entity in self.entities:
                    entity.move(game_map.get_colliders(camera.scroll))
          
          for tutorial_text in self.tutorial_texts:
               
               if tutorial_text[3] == "up":
                    if tutorial_text[2][1] < tutorial_text[1][1]*16 - 3:
                         tutorial_text[3] = "down"
                    else:
                         tutorial_text[2][1] -= .25
               elif tutorial_text[3] == "down":
                    if tutorial_text[2][1] > tutorial_text[1][1]*16 + 3:
                         tutorial_text[3] = "up"
                    else:
                         tutorial_text[2][1] += .25
          
          if not camera.static:
               f_rect = self.focused_entity.rect
               entity_center = [f_rect.centerx - camera.scroll[0] , f_rect.centery - camera.scroll[1]]
               true_scroll = camera.true_scroll.copy()
               # true_scroll[0] += ((f_rect.x - f_rect.x % 16) - true_scroll[0] - (camera.initial_display_size[0] // 2 - f_rect.size[0] / 2 )) / 20
               # true_scroll[1] += ((f_rect.y - f_rect.y % 16) - true_scroll[1] - (camera.initial_display_size[1] // 2 - f_rect.size[1] / 2 )) / 20
               if self.mode:
                    if entity_center[0] > self.cam_znf.x + self.cam_znf.w:
                         true_scroll[0] += (entity_center[0] - (self.cam_znf.x + self.cam_znf.w))
                    elif entity_center[0] < self.cam_znf.x:
                         true_scroll[0] -= (self.cam_znf.x - entity_center[0])
                    if entity_center[1] > self.cam_znf.y + self.cam_znf.h:
                         true_scroll[1] += (entity_center[1] - (self.cam_znf.y + self.cam_znf.h))
                    elif entity_center[1] < self.cam_znf.y:
                         true_scroll[1] -= (self.cam_znf.y - entity_center[1])
               
               if true_scroll[0] < 0:
                    true_scroll[0] = 0
               elif true_scroll[0] > game_map.size[0] - camera.display_size[0]:
                    true_scroll[0] = game_map.size[0] - camera.display_size[0]
               if true_scroll[1] > game_map.size[1] - camera.display_size[1]:
                    true_scroll[1] = game_map.size[1] - camera.display_size[1]
               elif true_scroll[1] < 0:
                    true_scroll[1] = 0
               
               camera.set_scroll(true_scroll)

          # animate torches
          # for chunk in map.layers["torches"]["chunks"].values():
          #      if not isOutOfScreen(ds_size , Rect([chunk["rect"].x-scroll[0] , chunk["rect"].y-scroll[1]],chunk["rect"].size)):
          #           for torch in chunk["data"]:
          #                torch.update(game_timer)
          if not self.changing_zone:
          
               for area in game_map.change_zones:
                    
                    if self.player.rect.colliderect(area["zone"]):
                         
                         self.player.able_to_move = False
                         self.changing_zone = True
                         make_transition(self.change_map , .25 , .25 , {"id":area["next_map"],"spawn_point":area["spawnpoint"].copy()})
          
          elif self.changing_zone and not transition:
               self.changing_zone = False
          
          # if player fall
          if self.player.pos[1] > game_map.size[1] + 100:
               self.player.set_pos(self.spawnpoint.copy())
          
          # if an entity fall
          for entity in self.entities:
               if entity.rect.y > game_map.size[1]:
                    self.entities.remove(entity)

     def prepare_backgrounds(self):
          # display_surface.fill([139, 201, 232])
          scroll = camera.scroll.copy()
          for background in self.backgrounds:
               x , y = 0,0
               if -int(scroll[0]*background[1][0]) < -100:
                    x = -100
               elif -int(scroll[0]*background[1][0]) > 0:
                    x = 0
               else:
                    x = -int(scroll[0]*background[1][0])
               
               if -int(scroll[1]*background[1][1]) < -100:
                    y = -100
               elif -int(scroll[1]*background[1][1]) > 0:
                    y = 0
               else:
                    y = -int(scroll[1]*background[1][1])
               
               camera.display_surface.blit(background[0] , [x,y])
     
     def display(self):
          self.prepare_backgrounds()
          scroll = camera.get_scroll()
          current_map = self.map_manager.maps[self.map_manager.current_map_id]
          for n , layer in enumerate(current_map.layers.values()):
               for chunk in layer["chunks"].values():
                    if not isOutOfScreen(camera.initial_display_size , Rect([chunk["rect"].x-scroll[0] , chunk["rect"].y-scroll[1]],chunk["rect"].size)):
                         for tile in chunk["data"]:
                              camera.display_surface.blit(tile.img,[tile.x-scroll[0],tile.y-scroll[1]])
               if n == self.tt_layer:
                    for tutorial_text in current_map.texts:
                         pos = [tutorial_text[1][0] - self.white_font.width(tutorial_text[0]) // 2 - scroll[0], tutorial_text[1][1] - self.white_font.line_height // 2 - scroll[1]]
                         self.black_font.render(tutorial_text[0] , camera.display_surface , [pos[0]+1 , pos[1]+1])
                         self.white_font.render(tutorial_text[0],camera.display_surface , pos)
               if n == ENTITY_LAYER:
                    self.player.display(camera.display_surface , scroll)
                    for entity in self.entities:
                         entity.display(camera.display_surface , scroll)
          
          self.snow_psystem.display(camera.display_surface , scroll)

class Menu_scene(Scene):
     
     def __init__(self):
          
          self.play_button = Button(
               "play",
               [DISPLAY_SIZE[0] // 2 - 50 , DISPLAY_SIZE[1] // 2 - 25],
               [100 , 50],
               {
                    "stringvalue":"play",
                    "align center":True,
                    "color":[255 , 255 , 255]
                    },
               {
                    "target":change_scene,"aDt":2,"bDt":2,"target_arguments":{"scene_id":"game"}
               }
          )
          
          self.music = "./data/musics/Snowy Night.mp3"
          self.play_button.font.base_spacing = 3
          self.play_button.event_rect = Rect([self.play_button.surf_rect.x * 2 , self.play_button.surf_rect.y * 2],[self.play_button.surf_rect.w * 2 , self.play_button.surf_rect.h * 2])
          self.play_button.change_background_color([0,0,0])
          self.play_button.target = make_transition
     
     def start(self):
          pygame.mixer.music.load(self.music)
          pygame.mixer.music.play(loops=1000)
          pygame.mixer.music.set_volume(1)
     
     def Update(self):
          
          self.event_handler()
          self.display()
     
     def event_handler(self):
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
               if not transition:
                    self.play_button.event_handler(event)
               
     
     def display(self):
          screen.fill([0,0,0])
          self.play_button.display(camera.display_surface)
          

# def getEntityRects(ignored=None):
#      rects = []
#      for entity in entities:
#           if ignored != None:
#                if entity != ignored:
#                     rects.append(entity.rect)
#           else:
#                rects.append(entity.rect)
     
#      return rects

class Transition_scene(Scene):
     
     def __init__(self , durations , target , target_arguments : dict = {}):
          self.before_duration = durations[0]
          self.after_duration = durations[1]
          self.duration = sum(durations)
          self.timer = 0

          self.alpha = 0
          self.alpha_coefs = [255 / self.before_duration , 255 / self.after_duration]
          self.target_arguments = target_arguments
          self.target = target
          self.func_called = False
          
     def Update(self):
          super().event_handler()
          self.update()
          self.display()
     
     def update(self):
          global dt , transition , transition_ref , current_id
          
          if self.timer > self.before_duration and not self.func_called:
               if self.target_arguments != {}:
                    self.target(**self.target_arguments)
               else:
                    self.target()
               self.func_called = True
          elif self.timer >= self.duration:
               transition = False
               transition_ref = None
          
          if self.timer < self.before_duration:
               self.alpha += self.alpha_coefs[0] * dt
          elif self.before_duration < self.timer:
               self.alpha -= self.alpha_coefs[1] * dt
          
          self.timer += min(dt , 1)
     
     def display(self):
          filter = pygame.Surface(DISPLAY_SIZE , SRCALPHA)
          alpha = min(int(self.alpha) , 255)
          if alpha < 0: alpha = 0
          filter.fill([0,0,0,alpha])
          camera.display_surface.blit(filter , [0,0])

def change_scene(scene_id):
     global current_id
     current_id = scene_id
     scenes[current_id].start()

def make_transition(target , aDt , bDt , target_arguments):
     global transition , transition_ref
     transition = True
     transition_ref = Transition_scene([aDt , bDt] , target , target_arguments)

scenes = {
          "game":Game_scene(),
          "menu":Menu_scene()
     }

transition_ref = None

current_id = "menu"
transition = False

def main():
     global dt
     scenes[current_id].start()
     while True:
          dt = round(clock.tick(80)*0.001 , 4)
          # display_surface.fill([43,58,89])
          scenes[current_id].Update()
          if transition:
               transition_ref.Update() # Event_handler is called in this
          # display_text_debug(screen , clock , dt , player)
          camera.update(dt)
          camera.display()
          pygame.display.flip()
          
if __name__ == "__main__":
     main()
          