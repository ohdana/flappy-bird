from settings import *
from os.path import join

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'
        
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