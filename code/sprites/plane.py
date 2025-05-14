from settings import *
from os.path import join
from os import walk

class Plane(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.direction = 0
        self.frame_index = 0
        
        self.__init_image(scale_factor)
        self.__init_rect()
        self.__init_pos()
        self.__init_mask()
        self.__init_audio()
    
    def update(self, dt):
        self.__apply_gravity(dt)
        self.__animate(dt)
        self.__rotate()
        
    def jump(self):
        self.direction = -JUMP_SIZE
        self.jump_sound.play()
        
    def __init_image(self, scale_factor):
        self.__load_frames(scale_factor)
        self.image = self.frames[self.frame_index]
    
    def __init_rect(self):
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
    
    def __init_pos(self):
        self.pos = pygame.math.Vector2(self.rect.topleft)
    
    def __init_mask(self):
        self.mask = pygame.mask.from_surface(self.image)
    
    def __init_audio(self):
        self.jump_sound = pygame.mixer.Sound(join('sounds', 'jump.wav'))
        self.jump_sound.set_volume(0.1)
        
    def __load_frames(self, scale_factor):
        self.frames = []
        for folder_path, _, file_names in walk(join('graphics', 'plane')):
            for file_name in file_names:
                full_path = join(folder_path, file_name)
                image = pygame.image.load(full_path).convert_alpha()
                scaled_image = pygame.transform.scale(image, pygame.math.Vector2(image.get_size()) * scale_factor)
                self.frames.append(scaled_image)
        
    def __apply_gravity(self, dt):
        self.direction += GRAVITY_SPEED * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)
    
    def __animate(self, dt):
        self.frame_index += PLANE_ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
    def __rotate(self):
        self.image = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.__init_mask()