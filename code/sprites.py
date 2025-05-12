import pygame
from settings import *
from os.path import join
from os import walk
from random import choice, randint

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load(join('graphics', 'environment', 'background.png')).convert()
        
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height))
        
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_width,0))
        
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
    def update(self, dt):
        self.pos.x -= 300 * dt
        
        if self.rect.centerx <= 0:
            self.pos.x = 0
            
        self.rect.x = round(self.pos.x)
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        
        # image
        ground_surf = pygame.image.load(join('graphics', 'environment', 'ground.png')).convert_alpha()
        self.image = pygame.transform.scale(ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
        
        # position
        self.rect = self.image.get_rect(bottomleft=(0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # masks
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.pos.x -= 360 * dt
        
        if self.rect.centerx <= 0:
            self.pos.x = 0
            
        self.rect.x = round(self.pos.x)
        
class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        
        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
        # position
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # movement
        self.gravity = 600
        self.direction = 0
        
        # masks
        self.mask = pygame.mask.from_surface(self.image)
        
    def import_frames(self, scale_factor):
        self.frames = []
        for folder_path, _, file_names in walk(join('graphics', 'plane')):
            for file_name in file_names:
                full_path = join(folder_path, file_name)
                image = pygame.image.load(full_path).convert_alpha()
                scaled_image = pygame.transform.scale(image, pygame.math.Vector2(image.get_size()) * scale_factor)
                self.frames.append(scaled_image)
    
    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()
        
    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
        
    def jump(self):
        self.direction = -400
    
    def animate(self, dt):
        self.frame_index += 10 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        
        orientation = choice(('up', 'down'))
        surf = pygame.image.load(join('graphics', 'obstacles', f'{choice((0,1))}.png')).convert_alpha()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
        
        x = WINDOW_WIDTH + randint(40, 100)
        
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            self.image = pygame.transform.flip(self.image, False, True)
            y = randint(-50, -10)
            self.rect = self.image.get_rect(midtop = (x, y))
        
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # masks
        self.mask = pygame.mask.from_surface(self.image)
         
    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        
        if self.rect.right <= -100:
            self.kill()