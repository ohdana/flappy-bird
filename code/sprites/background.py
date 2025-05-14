from settings import *
from os.path import join

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.__init_image(scale_factor)
        self.__init_rect()
        self.__init_pos()
       
    def update(self, dt):
        self.__move_left(dt)
    
    def __move_left(self, dt):
        self.pos.x -= BACKGROUND_SPEED * dt
        self.__loop_image()
        self.rect.x = round(self.pos.x)
            
    def __loop_image(self):
        if self.rect.centerx <= 0:
            self.pos.x = 0
    
    def __init_image(self, scale_factor):
        surf = pygame.image.load(join('graphics', 'environment', 'background.png')).convert()
        
        scaled_height = surf.get_height() * scale_factor
        scaled_width = surf.get_width() * scale_factor
        scaled_surf = pygame.transform.scale(surf, (scaled_width, scaled_height))

        self.image = pygame.Surface((scaled_width * 2, scaled_height))
        self.image.blit(scaled_surf, (0,0))
        self.image.blit(scaled_surf, (scaled_width,0))
        
    def __init_rect(self):
        self.rect = self.image.get_rect(topleft = (0,0))
    
    def __init_pos(self):
        self.pos = pygame.math.Vector2(self.rect.topleft)