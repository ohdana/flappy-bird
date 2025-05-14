from settings import *
from os.path import join
from random import choice, randint

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.__init_orientation()
        self.__init_image(scale_factor)
        self.__init_rect()
        self.__init_pos()
        self.__init_mask()
         
    def update(self, dt):
        self.__move_left(dt)
        
        is_out_of_sight = self.__check_if_out_of_sight()
        if is_out_of_sight:
            self.kill()
            
    def __move_left(self, dt):
        self.pos.x -= OBSTACLE_SPEED * dt
        self.rect.x = round(self.pos.x)
    
    def __init_orientation(self):
        self.orientation = choice(ORIENTATION_TYPES)
    
    def __init_image(self, scale_factor):
        surf = self.__get_image_surf()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
        
        if self.orientation == 'down':
            self.image = pygame.transform.flip(self.image, False, True)
    
    def __init_rect(self):
        x = WINDOW_WIDTH + randint(40, 100)
        
        if self.orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            y = randint(-50, -10)
            self.rect = self.image.get_rect(midtop = (x, y))
        
    def __init_pos(self):
        self.pos = pygame.math.Vector2(self.rect.topleft)
    
    def __init_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
        
    def __get_image_surf(self):
        random_image_name = choice(OBSTACLE_FILENAMES)
        loaded_image = pygame.image.load(join('graphics', 'obstacles', random_image_name)).convert_alpha()
        
        return loaded_image
            
    def __check_if_out_of_sight(self):
        return self.rect.right <= 0