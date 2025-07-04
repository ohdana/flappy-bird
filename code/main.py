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
        self.__init_timer()
        self.__init_font()
        self.__init_menu()
        self.__init_audio()
        self.__init_score()
        self.__start_new_game()
    
    def run(self):
        self.__init_prev_frame_time()
        while True:
            self.__check_for_events()
            self.__handle_user_input()
            self.__redraw_game_window()
            
            if self.is_active:
                self.__check_for_collisions()
            else:
                self.__show_menu()
            
            self.__handle_frame_tick()
            
    def __check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__handle_quit()
                    
            if event.type == self.obstacle_timer:
                self.__handle_obstacle_timer()
                
    def __handle_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.__handle_space_pressed()
            
    def __handle_frame_tick(self):
        pygame.display.update()
        self.clock.tick(FRAMERATE)
            
    def __handle_obstacle_timer(self):
        if self.is_active:
            self.__create_new_obstacle()
    
    def __handle_quit(self):
        pygame.quit()
        sys.exit()
            
    def __create_new_obstacle(self):
        Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor)
            
    def __show_menu(self):
        self.display_surface.blit(self.menu_surf, self.menu_rect)
    
    def __redraw_game_window(self):
        self.display_surface.fill('black')
        dt = time.time() - self.prev_frame_time
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)
        self.__display_score()
        self.__display_lives()
        self.prev_frame_time = time.time()
            
    def __handle_space_pressed(self):
        if self.is_active:
            self.plane.jump()
        else:
            self.__start_new_game()
    
    def __start_new_game(self):
        self.__init_plane()
        self.is_active = True
        self.start_offset = pygame.time.get_ticks()
        self.lives = N_OF_LIVES
        
    def __check_for_collisions(self):
        collided_sprites = pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask)
        if collided_sprites or self.plane.rect.top <= 0:
            if not self.collision_handled:
                for sprite in collided_sprites:
                    if isinstance(sprite, Obstacle):
                    	sprite.kill()
                self.__handle_lost_life()
                self.collision_handled = True
        else:
            self.collision_handled = False
            
    def __handle_lost_life(self):
        self.lives -= 1
        
        is_out_of_lives = self.lives == 0
        if is_out_of_lives:
            self.__end_game()
        else:
            self.plane.kill()
            self.__init_plane()
            
    def __end_game(self):
        self.is_active = False
        self.plane.kill()
            
    def __display_score(self):
        if self.is_active:
        	self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
        	y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + self.menu_rect.height / 1.5
        
        score_surf = self.font.render(f'{self.score}', True, 'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)
        
    def __display_lives(self):
        if self.is_active:
            heart_active_surf = pygame.image.load(join('graphics', 'heart', 'heart_active.png')).convert_alpha()
            heart_dead_surf = pygame.image.load(join('graphics', 'heart', 'heart_dead.png')).convert_alpha()
            heart_width = heart_active_surf.get_width()
            
            lives_panel_width = heart_width * N_OF_LIVES
            lives_panel_height = heart_active_surf.get_height()
            lives_surf = pygame.Surface((lives_panel_width, lives_panel_height), pygame.SRCALPHA)
            for i in range(self.lives):
                x = i * heart_width
                heart_rect = heart_active_surf.get_rect(topleft = (i * heart_width, 0))
                lives_surf.blit(heart_active_surf, heart_rect)
                
            for i in range(N_OF_LIVES - self.lives):
                heart_rect = heart_dead_surf.get_rect(topleft = (heart_width * (self.lives + i), 0))
                lives_surf.blit(heart_dead_surf, heart_rect)
                
            lives_rect = lives_surf.get_rect(topright = (WINDOW_WIDTH - 10, 10))
            self.display_surface.blit(lives_surf, lives_rect)
        
    def __init_prev_frame_time(self):
        self.prev_frame_time = time.time()
        
    def __init_game_window(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        
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

if __name__ == '__main__':
    game = Game()
    game.run()