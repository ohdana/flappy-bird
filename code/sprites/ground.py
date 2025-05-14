from settings import *
from os.path import join

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.__init_image(scale_factor)
        self.__init_rect()
        self.__init_pos()
        self.__init_mask()
        
    def update(self, dt):
        self.__move_left(dt)
            
    def __move_left(self, dt):
        self.pos.x -= GROUND_SPEED * dt
        self.__loop_image()
        self.rect.x = round(self.pos.x)
            
    def __loop_image(self):
        if self.rect.centerx <= 0:
            self.pos.x = 0
    
    def __init_image(self, scale_factor):
        surf = pygame.image.load(join('graphics', 'environment', 'ground.png')).convert_alpha()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
    
    def __init_rect(self):
        self.rect = self.image.get_rect(bottomleft=(0,WINDOW_HEIGHT))
    
    def __init_pos(self):
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
    def __init_mask(self):
        self.mask = pygame.mask.from_surface(self.image)