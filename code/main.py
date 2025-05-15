from os.path import join
from settings import *
from sprites.background import BG
from sprites.ground import Ground
from sprites.plane import Plane
from sprites.obstacle import Obstacle

class Game:
    def __init__(self):
        pygame.init()
        
        self.__init_game_window()
        self.__init_clock()
        self.__init_sprites()
        self.__init_scaling()
        self.__init_scenery()
        self.__init_plane()
        self.__init_timer()
        self.__init_font()
        self.__init_menu()
        self.__init_audio()
        self.__init_score()
    
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
                    if self.active:
                    	self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                    
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)

            # game logic 
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.__display_score()
            
            if self.active:
                self.__check_for_collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)
            
            pygame.display.update()
            self.clock.tick(FRAMERATE)
        
    def __check_for_collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask)\
        or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if isinstance(sprite, Obstacle):
                	sprite.kill()
            self.active = False
            self.plane.kill()
            
    def __display_score(self):
        if self.active:
        	self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
        	y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + self.menu_rect.height / 1.5
        
        score_surf = self.font.render(f'{self.score}', True, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)
        
    def __init_game_window(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.active = True
        
    def __init_clock(self):
        self.clock = pygame.time.Clock()
        
    def __init_sprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
    def __init_scaling(self):
        bg_height = pygame.image.load(join('graphics', 'environment', 'background.png')).get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height
        
    def __init_scenery(self):
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        
    def __init_plane(self):
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
        
    def __init_timer(self):
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)
        
    def __init_font(self):
        font_path = join('graphics', 'font', 'BD_Cartoon_Shout.ttf')
        self.font = pygame.font.Font(font_path, 30)
    
    def __init_menu(self):
        self.menu_surf = pygame.image.load(join('graphics', 'ui', 'menu.png')).convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        
    def __init_audio(self):
        self.music = pygame.mixer.Sound(join('sounds', 'music.wav'))
        self.music.set_volume(0.1)
        self.music.play(loops = -1)
        
    def __init_score(self):
        self.score = 0
        self.start_offset = 0

if __name__ == '__main__':
    game = Game()
    game.run()