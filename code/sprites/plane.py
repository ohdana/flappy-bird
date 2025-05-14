from settings import *
from os.path import join
from os import walk

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
        
        # sound
        self.jump_sound = pygame.mixer.Sound(join('sounds', 'jump.wav'))
        self.jump_sound.set_volume(0.1)
        
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
        self.jump_sound.play()
    
    def animate(self, dt):
        self.frame_index += 10 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)