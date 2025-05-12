import pygame, sys, time
from os.path import join
from settings import *
from sprites import BG, Ground, Plane, Obstacle

class Game:
    def __init__(self):
        
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        # scale factor
        bg_height = pygame.image.load(join('graphics', 'environment', 'background.png')).get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height
        
        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground(self.all_sprites, self.scale_factor)
        
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
        
        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)
  
    def run(self):
        last_time = time.time()
        while True:
            
            # delta time
            dt = time.time() - last_time
            last_time = time.time()
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.plane.jump()
                    
                if event.type == self.obstacle_timer:
                    Obstacle(self.all_sprites, self.scale_factor)

            # game logic 
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            
            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()