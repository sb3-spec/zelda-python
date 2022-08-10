import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack):
        super().__init__(groups)
        
        self.image = pygame.image.load('./graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        
        # graphics setup
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = .15
        
        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 7
        
        # attacks
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.create_attack = create_attack
        
        # magic
        self.casting_spell = False
        self.spell_cooldown = 400
        self.cast_time = 0
        
        self.obstacle_sprites = obstacle_sprites
        
    def import_player_assets(self):
        
        char_path = './graphics/player/'
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': [],
            'left_magic': [], 'right_magic': [], 'up_magic': [], 'down_magic': []
        }
        
        for animation in self.animations.keys():
            path = char_path + animation
            
            self.animations[animation] = import_folder(path)
        
    
    def get_status(self):
        
        # idle status 
        if self.direction.x == 0 and self.direction.y == 0 and \
            not '_idle' in self.status and \
            not self.casting_spell and not self.attacking:
            self.status += '_idle'
                
                
            
        # attacking status
        if self.attacking:
            self.direction.x, self.direction.y = 0, 0
            
            if not 'attack' in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
                    
        elif 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
            
                    
        # magic status
        if self.casting_spell:
            self.direction.x, self.direction.y = 0, 0
            
            if not 'magic' in self.status:
                if '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_magic')
                else:
                    self.status += '_magic'
        elif 'magic' in self.status:
            self.status = self.status.replace('_magic', '')
        
        
    def collision(self, direction):
        if direction == 'horizontal':
            
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom         
        
    def input(self):
        if self.attacking or self.casting_spell:
            return
        keys = pygame.key.get_pressed()
        
        # movement input
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status='up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
            
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
            
        # attack input
        if keys[pygame.K_SPACE]:
            self.create_attack()
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            
        # magic input
        if keys[pygame.K_LCTRL]:
            self.casting_spell = True
            self.cast_time = pygame.time.get_ticks()
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
            
    def cooldowns(self):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time > self.attack_cooldown: self.attacking = False
        if current_time - self.cast_time > self.spell_cooldown: self.casting_spell = False
            
    def animate(self):
        animations = self.animations[self.status]
        
        # increment frame_index by animation speed
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animations):
            self.frame_index = 0
            
        # set the image 
        self.image = animations[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
        
        
    def update(self):
        # udate
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        
        