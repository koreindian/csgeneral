import math
import sys
import os
import pygame
import random
import time

import console as cmd_console
import pairs_utils

os.environ['SDL_VIDEO_CENTERED'] = '1'

def main():
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    
    engine = GameEngine()
    screen = engine.screen
    entity_mgr = EntityManager(engine)
    sound_bank = SoundBank()
    console = cmd_console.Console(engine)
        
    while 1:
        engine.clock.tick(60)
        process_input(entity_mgr, console, engine)
        engine.update()
        console.update()
        
        if not engine.game_over:
            if not engine.paused or engine.paused_manual_frame_tick:
                entity_mgr.update(engine, sound_bank)
                engine.paused_manual_frame_tick = False
           
            sound_bank.update(engine)

            entity_mgr.draw(engine)
            engine.draw(entity_mgr)

        else:
            engine.draw(entity_mgr)

        console.draw(screen)
        pygame.display.flip()

def global_restart(engine, entity_mgr):
    engine.restart()
    entity_mgr.restart(engine)

def process_input(entity_mgr, console, engine):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if console.open:
            #Console input processing
            console.process_event(event, engine, entity_mgr)
        else:
            #Regular game input processing
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    entity_mgr.grid.on_left_click(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == engine.restart_trigger[0]:
                    global_restart(engine, entity_mgr)
                elif event.key == engine.pause_trigger[0]:
                    engine.paused = not engine.paused
                elif event.key == pygame.K_BACKQUOTE:
                    console.open = True
            elif event.type == pygame.KEYUP:
                if engine.paused:
                    if event.key == pygame.K_f:
                        engine.paused_manual_frame_tick = True

class SoundBank:
    def __init__(self):
        #Channels:
        #    0 = Bg
        #    1 = Player
        pygame.mixer.set_num_channels(8)

        #player_collision_path = os.path.join('data/', 'player_collision.wav')
        #self.c1 = pygame.mixer.Sound(player_collision_path)
        #enemy_collision_path = os.path.join('data/', 'enemy_collision.wav')
        #self.c2 = pygame.mixer.Sound(enemy_collision_path)
        #wc_path = os.path.join('data/', 'wall_collision.wav')
        #self.c3 = pygame.mixer.Sound(wc_path)

        #player_score_path = os.path.join('data/', 'player_score.wav')
        #self.s1 = pygame.mixer.Sound(player_score_path)
        #enemy_score_path = os.path.join('data/', 'enemy_score.wav')
        #self.s2 = pygame.mixer.Sound(enemy_score_path)

        self.music_paused = False

    def play_level1_music(self):
        pass
        #pygame.mixer.music.load(self.bgm_interstellar_path)
        #pygame.mixer.music.set_volume(0.1)
        #pygame.mixer.music.play(0)

    def player_collide(self):
        player_channel1 = pygame.mixer.Channel(1)
        player_channel1.play(self.c1)

    def update(self, game_engine):
        if game_engine.paused:
            pygame.mixer.music.pause()
            self.music_paused = True
        else:
            if self.music_paused:
                pygame.mixer.music.unpause()
                self.music_paused = False

# The Game Engine manages all global state (ex. paused, game_over, tick clock)
class GameEngine:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen_height = 720
        self.screen_width = 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.paused = False
        #Variable to move one frame forward while in paused mode
        self.paused_manual_frame_tick = False
        
        self.game_over = False

        #Number of frames since game began
        self.total_frames = 0
        #Excludes paused and game-over frames
        self.total_frames_played = 0
        self.started_time = time.time()
        self.current_time = time.time()
        self.elapsed_time = 0

        self.generic_font = pygame.font.SysFont('Courier', 30)

        # Function to [key, arcade stick button index] mapping
        self.restart_trigger = [pygame.K_r, 4]
        self.pause_trigger   = [pygame.K_p, 5]

    def restart(self):
        self.total_frames = 0
        self.total_frames_played = 0
        self.started_time = time.time()
        self.current_time = time.time()
        self.elapsed_time = 0
        self.player_score = 0
        self.game_over = False
                
    def update(self):
        self.total_frames += 1

        if (not self.paused or self.paused_manual_frame_tick) \
           and not self.game_over:
            self.total_frames_played += 1

        self.current_time = time.time()
        self.elapsed_time = self.current_time - self.started_time
        
    def get_FPS(self):
        return format(self.total_frames / max(1, self.elapsed_time), '.2f')

    def draw(self, entity_mgr):
        red = (255,0,0)
        font = self.generic_font
        screen = self.screen

        if self.game_over:
            screen.fill((0,0,0))
            game_over = self.generic_font.render('Game Over', False, (255,0,0))
            screen.blit(game_over, 
                        (self.screen_width // 2 - game_over.get_width() // 2,
                        self.screen_height // 2 - game_over.get_height() // 2))
        else:
            if self.paused:
                paused = font.render('Paused', False, red)
                screen.blit(paused, (self.screen_width // 2  - paused.get_width()  // 2,
                                     self.screen_height // 2 - paused.get_height() // 2))        
            
            FPS = font.render('FPS: ' + str(self.get_FPS()), False, red)
            screen.blit(FPS, (self.screen_width - FPS.get_width(), 0))
 
            time = font.render('Time: ' + str(self.total_frames_played), False, red)
            screen.blit(time, (self.screen_width - time.get_width(), font.get_height()))

class EntityManager:
    def __init__(self, engine):
        #self.background = Background('background_concept_1.jpg', engine)
        self.grid = Card_Grid(engine)

    def restart(self, engine):
        #self.background = Background('background_concept_1.jpg', engine)
        self.grid = Card_Grid(engine)

    def update(self, engine, sound_bank): 
        #self.background.update()
        self.grid.update()
        for row in self.grid.cards:
            for card in row:
                if card:
                    card.update()

    def draw(self, engine):
        screen = engine.screen
        screen.fill((0,0,0))
        #self.background.draw(engine)
        self.grid.draw(engine)

class Background():
    def __init__(self, filename, engine):
        self.image, self.rect = pairs_utils.load_image(filename)
        self.rect.top = 0

    def update(self):
        return

    def draw(self, engine):
        screen = engine.screen
        screen.blit(self.image, self.rect)

class Card_Grid():
    def __init__(self, engine):
        self.grid_width = engine.screen_width
        self.grid_height = engine.screen_height

        self.num_cards_width = 4
        self.num_cards_height = 3

        self.card_width  = self.grid_width // self.num_cards_width
        self.card_height = self.grid_height // self.num_cards_height

        self.cards = [[None] * self.num_cards_width for x in range(self.num_cards_height)]

        card1 = Card(self, 0, 0, '')
        card2 = Card(self, 0, 1, '')

        self.cards[0][0] = card1
        self.cards[1][0] = card2

    def update(self):
        #print('Update')
        #for row in self.cards:
        #    for card in row:
        #        if card:
        #            print(card.state)
        pass

    def on_left_click(self, click_event):
        pos = click_event.pos

        for row in self.cards:
            for card in row:
                if card and card.rect.collidepoint(pos[0], pos[1]):
                    if card.state == 'DOWN':
                        card.state = 'UP'
                    elif card.state == 'UP':
                        card.state = 'DOWN'


    def draw(self, engine):
        for row in self.cards:
            for card in row:
                if card:
                    card.draw(engine)

class Card():
    def __init__(self, grid, x, y, filename):
        self.back_image = None #pairs_utils.load_image(filename)
        self.front_image = None

        self.rect = pygame.Rect(x * grid.card_width,
                                y * grid.card_height,
                                grid.card_width,
                                grid.card_height)
        #States:
        # 1. DOWN      - Totally face down
        # 2. UP        - Totally face up    
        # 3. FLIP_DOWN - Flipping face down
        # 4. FLIP_UP   - Flipping face up
        self.state = 'DOWN'

        self.flip_counter = 0
        self.flip_time = 5


    def update(self):
        if self.state == 'FLIP_UP':
            if self.flip_counter == self.flip_time:
                self.start = 'UP'
                self.flip_counter = 0
            else:
                self.flip_counter += 1

        if self.state == 'FLIP_DOWN':
            if self.flip_counter == self.flip_time:
                self.start = 'DOWN'
                self.flip_counter = 0
            else:
                self.flip_counter += 1

    def draw(self, engine):
        screen = engine.screen

        if self.state == 'DOWN':
            pygame.draw.rect(screen, (255,0,0), self.rect, 0)
        if self.state == 'UP':
            pygame.draw.rect(screen, (0,255,0), self.rect, 0)
        
if __name__ == '__main__':
    main()
