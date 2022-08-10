import pygame 
from settings import *
from tile import Tile
from player import Player
from support import *
from random import randint
from debug import debug
from weapon import Weapon

class Level:
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        self.player = None
        
        self.create_map()
        
    def create_map(self):
        
        layouts = {
            'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('./map/map_Grass.csv'),
            'object': import_csv_layout('./map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('./graphics/grass'),
            'objects': import_folder('./graphics/objects'),
        }
        
        for style, layout in layouts.items():
            for row_idx, row in enumerate(layout):
                for col_idx, col in enumerate(row):
                    if col != '-1':
                        x, y = TILESIZE * col_idx, TILESIZE * row_idx
                        
                        if style == 'boundary':
                            # create boundary tile
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                            
                        if style == 'grass':
                            # create grass tile
                            random_img = graphics['grass'][randint(0, len(graphics['grass']) - 1)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', surface=random_img)
                            
                        
                        if style == 'object':
                            # create object tile
                            surface = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surface=surface)
                            
                        
                    
                    
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites, self.create_attack())
                   
    def create_attack(self):
        if self.player:
            Weapon(self.player, self.visible_sprites)      
        
    def run(self):
        # update and draw the game object
        self.visible_sprites.custom_draw(self.player)
        debug(self.player.status)
        self.visible_sprites.update()
        
        

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        # general setup
        super().__init__()
        
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        # creating floor 
        self.floor_surface = pygame.image.load('./graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))
        

    def custom_draw(self, player):
        
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        # drawing the floor_surface
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)
        
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
