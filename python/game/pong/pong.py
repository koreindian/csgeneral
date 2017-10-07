import math
import sys
import os
import pygame
import random
import time

import console as cmd_console
import pong_utils

os.environ['SDL_VIDEO_CENTERED'] = '1'

def main():
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    
    engine = GameEngine()
    screen = engine.screen
    entity_mgr = EntityManager(engine)
    camera = Camera(engine, entity_mgr)
    sound_bank = SoundBank()
    console = cmd_console.Console(engine)
    
    pygame.joystick.init()
    joystick = None
    if pygame.joystick.get_count() == 1:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        
    while 1:
        engine.clock.tick(60)
        process_input(entity_mgr, console, engine, camera, joystick)
        engine.update()
        console.update()
        
        if not engine.game_over:
            if not engine.paused or engine.paused_manual_frame_tick:
                entity_mgr.update(engine, camera, sound_bank)
                camera.update()
                engine.paused_manual_frame_tick = False
           
            sound_bank.update(engine)

            entity_mgr.draw(engine, camera)
            engine.draw(entity_mgr)

        else:
            engine.draw(entity_mgr)

        console.draw(screen)
        pygame.display.flip()

def global_restart(engine, entity_mgr, camera):
    engine.restart()
    entity_mgr.restart(engine)
    camera.restart(engine, entity_mgr)

def process_input(entity_mgr, console, engine, camera, joystick):
    player = entity_mgr.player

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if console.open:
            #Console input processing
            console.process_event(event, engine, entity_mgr)
        else:
            #Regular game input processing
            if event.type == pygame.JOYHATMOTION:
                player.determine_direction(joystick_mode=True, joystick=joystick)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == engine.restart_trigger[1]:
                    global_restart(engine, entity_mgr, camera)
                elif event.button == engine.pause_trigger[1]:
                    engine.paused = not engine.paused
            elif event.type == pygame.KEYDOWN:
                if event.key == engine.restart_trigger[0]:
                    global_restart(engine, entity_mgr, camera)
                elif event.key == engine.pause_trigger[0]:
                    engine.paused = not engine.paused
                elif event.key == pygame.K_BACKQUOTE:
                    console.open = True
                elif event.key == pygame.K_UP or \
                     event.key == pygame.K_DOWN:
                        player.determine_direction()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or \
                   event.key == pygame.K_DOWN:
                        player.determine_direction()
                if engine.paused:
                    if event.key == pygame.K_f:
                        engine.paused_manual_frame_tick = True

class SoundBank:
    def __init__(self):
        #Channels:
        #    0 = Bg
        #    1 = Player
        pygame.mixer.set_num_channels(8)

        player_collision_path = os.path.join('data/', 'player_collision.wav')
        self.c1 = pygame.mixer.Sound(player_collision_path)
        enemy_collision_path = os.path.join('data/', 'enemy_collision.wav')
        self.c2 = pygame.mixer.Sound(enemy_collision_path)
        wc_path = os.path.join('data/', 'wall_collision.wav')
        self.c3 = pygame.mixer.Sound(wc_path)

        player_score_path = os.path.join('data/', 'player_score.wav')
        self.s1 = pygame.mixer.Sound(player_score_path)
        enemy_score_path = os.path.join('data/', 'enemy_score.wav')
        self.s2 = pygame.mixer.Sound(enemy_score_path)

        self.music_paused = False

    def play_level1_music(self):
        pass
        #pygame.mixer.music.load(self.bgm_interstellar_path)
        #pygame.mixer.music.set_volume(0.1)
        #pygame.mixer.music.play(0)

    def player_collide(self):
        player_channel1 = pygame.mixer.Channel(1)
        player_channel1.play(self.c1)
    
    def enemy_collide(self):
        player_channel1 = pygame.mixer.Channel(1)
        player_channel1.play(self.c2)

    def wall_collide(self):
        player_channel2 = pygame.mixer.Channel(2)
        player_channel2.play(self.c3)

    def player_score(self):
        player_channel1 = pygame.mixer.Channel(1)
        player_channel1.play(self.s1)

    def enemy_score(self):
        player_channel1 = pygame.mixer.Channel(1)
        self.c3.set_volume(0.4)
        player_channel1.play(self.s2)

    def update(self, game_engine):
        if game_engine.paused:
            pygame.mixer.music.pause()
            self.music_paused = True
        else:
            if self.music_paused:
                pygame.mixer.music.unpause()
                self.music_paused = False

class Camera:
    def __init__(self, engine, entity_mgr):
        self.camera_worldx = 0 
        self.camera_worldy = 0
                             #entity_mgr.background.image.get_height() \
                             #- engine.screen_height
        self.camera_vx = 0
        self.camera_vy = 0

    def update(self):
        self.camera_worldx += self.camera_vx
        self.camera_worldy += self.camera_vy

    def restart(self, engine, entity_mgr):
        self.camera_worldx = 0 
        self.camera_worldy = 0
                             #entity_mgr.background.image.get_height() \
                             #- engine.screen_height
        self.camera_vx = 0
        self.camera_vy = 0

    #World to Camera coordinates
    def w2c(self, coords):
        x = coords[0]
        y = coords[1]
        return (x - self.camera_worldx, y - self.camera_worldy)

    def rect_w2c(self, rect):
        rect.x -= self.camera_worldx
        rect.y -= self.camera_worldy

    def c2w(self, coords):
        x = coords[0]
        y = coords[1]
        return (self.camera_worldx + x , self.camera_worldy + y)
        
    def rect_c2w(self, rect):
        rect.x += self.camera_worldx
        rect.y += self.camera_worldy

# The Game Engine manages all global state (ex. paused, game_over, tick clock)
class GameEngine:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen_height = 480
        self.screen_width = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.paused = False
        #Variable to move one frame forward while in paused mode
        self.paused_manual_frame_tick = False
        
        self.game_over = False

        self.player_score = 0
        self.enemy_score = 0

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
        self.enemy_score = 0
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
            game_over_text_surface = self.generic_font.render(
                                          'Game Over', False, (255,0,0))
            screen.blit(game_over_text_surface, 
                        (self.screen_width // 2 - game_over_text_surface.get_width() // 2,
                        self.screen_height // 2 - game_over_text_surface.get_height() // 2))
        else:
            if self.paused:
                paused = font.render('Paused', False, red)
                screen.blit(paused, (self.screen_width // 2  - paused.get_width()  // 2, \
                                     self.screen_height // 2 - paused.get_height() // 2))        
            
            FPS = font.render('FPS: ' + str(self.get_FPS()), False, red)
            screen.blit(FPS, (self.screen_width - FPS.get_width(), 0))
 
            time = font.render('Time: ' + str(self.total_frames_played), False, red)
            screen.blit(time, (self.screen_width - time.get_width(), font.get_height()))


            score = font.render(str(self.player_score) + ':' + str(self.enemy_score), 
                                False, red)

            screen.blit(score, (self.screen_width // 2 - score.get_width() // 2,
                                self.screen_height - score.get_height()))

 
class EntityManager:
    def __init__(self, engine):
        self.player = Player(engine)
        self.enemy = Enemy(engine)
        self.ball = Ball(engine)
        self.invis_ball = None
        #self.background = Background('background_concept_1.jpg', engine)

        self.display_hitboxes = True

    def restart(self, engine):
        self.player = Player(engine)
        self.enemy = Enemy(engine)
        self.ball = Ball(engine)
        self.invis_ball = None
        #self.background = Background('background_concept_1.jpg', engine)

    def update(self, engine, camera, sound_bank): 
        #self.background.update()
        self.player.update(engine, camera)
        self.enemy.update(engine, self, camera)
        self.ball.update(engine, self, camera, sound_bank)

        if self.invis_ball:
            self.invis_ball.update(engine, self, camera)

    def draw(self, engine, camera):
        screen = engine.screen
        screen.fill((0,0,0))
        #self.background.draw(engine, camera)
        
        self.player.draw(screen, camera, self.display_hitboxes)
        self.enemy.draw(screen, camera, self.display_hitboxes)
        self.ball.draw(screen, camera, self.display_hitboxes)
        
        if self.invis_ball:
            self.invis_ball.draw(screen, camera, self.display_hitboxes)

class Background():
    def __init__(self, name, engine):
        self.image, self.rect = pong_utils.load_image(name)
        self.rect.top = 0

    def update(self):
        #No updating to world coordinates of background, so nothing happens here
        #self.scroll_speed += self.scroll_acceleration
        #self.rect.move_ip(0, self.scroll_speed)
        return

    def draw(self, engine, camera):
        screen = engine.screen

        camera.rect_w2c(self.rect)
        screen.blit(self.image, self.rect)
        camera.rect_c2w(self.rect)        

class Ball():
    def __init__(self, engine):
        self.real_x = engine.screen_width // 2
        self.real_y = engine.screen_height // 2
        self.radius = 10
        self.color = (255, 0 , 0)

        self.rect = pygame.Rect(0, 0, self.radius * 2 + 1, self.radius * 2 + 1)
        self.rect.center = (self.real_x, self.real_y)
        self.hitbox = self.rect.copy()
        
        self.vx = -10
        self.vy = random.randint(-5,5)

        self.bounce_counter = 0

    def draw(self, screen, camera, display_hitbox):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)

        if display_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)

    def update(self, engine, entity_mgr, camera, sound_bank):
        if self.hitbox.left <= 0:
            engine.enemy_score += 1
            entity_mgr.ball = Ball(engine)
            entity_mgr.invis_ball = None
            sound_bank.enemy_score()
        if self.hitbox.right >= engine.screen_width:
            engine.player_score += 1
            entity_mgr.ball = Ball(engine)
            entity_mgr.invis_ball = None
            sound_bank.player_score()

        if self.bounce_counter > 3:
            if self.hitbox.top <= 0 or self.hitbox.bottom >= engine.screen_height:
                self.vy *= -1
                self.bounce_counter = 0
                sound_bank.wall_collide()

            if entity_mgr.player.hitbox.colliderect(self.hitbox):
                self.vx *= -1
                entity_mgr.invis_ball = Invis_Ball(engine, self.rect.center, self.vx, self.vy)
                self.bounce_counter = 0
                sound_bank.player_collide()

            if entity_mgr.enemy.hitbox.colliderect(self.hitbox):
                self.vx *= -1
                if entity_mgr.invis_ball:
                    entity_mgr.invis_ball = None
                self.bounce_counter = 0
                sound_bank.enemy_collide()
        
        self.real_x += self.vx
        self.real_y += self.vy      
        self.rect.move_ip(self.real_x - self.rect.center[0], 
                          self.real_y - self.rect.center[1])
        self.hitbox.move_ip(self.real_x - self.hitbox.center[0], 
                            self.real_y - self.hitbox.center[1])
        self.bounce_counter += 1

class Invis_Ball():
    #Used for enemy AI
    def __init__(self, engine, source_coords, parent_vx, parent_vy):
        Ball.__init__(self, engine)
        self.real_x = source_coords[0]
        self.real_y = source_coords[1]
        self.vx = math.sqrt(2) * parent_vx
        self.vy = math.sqrt(2) * parent_vy
        self.rect.center = source_coords
        self.hitbox = self.rect.copy()

        self.bounce_counter = 0 #to prevent gratutious collisions

    def draw(self, screen, camera, display_hitbox):
        pygame.draw.circle(screen, (0,255,0), self.rect.center, self.radius, 0)

        if display_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)


    def update(self, engine, entity_mgr, camera):
        if self.hitbox.top <= 0 or self.hitbox.bottom >= engine.screen_height:
            if self.bounce_counter > 2:
                self.vy *= -1
                self.bounce_counter = 0

        if self.hitbox.right > entity_mgr.enemy.hitbox.right:
            self.vx = 0
            self.vy = 0
        
        self.real_x += self.vx
        self.real_y += self.vy 

        self.rect.move_ip(self.real_x - self.rect.center[0], 
                          self.real_y - self.rect.center[1])
        self.hitbox.move_ip(self.real_x - self.hitbox.center[0], 
                            self.real_y - self.hitbox.center[1])

        self.bounce_counter += 1

class Player():
    def __init__(self, engine):
        self.centerx = 60
        self.centery = engine.screen_height // 2
        self.height = 90
        self.width = 15
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.centerx, self.centery)

        self.hitbox = self.rect.copy()

        self.movement_direction = None
        self.movement_factor = 8

    def determine_direction(self, joystick_mode=False, joystick=None):
        if joystick_mode:
            hat = joystick.get_hat(0)
            if   hat[1] == 0:
                self.movement_direction = None
            elif hat[1] == 1:
                self.movement_direction = "UP"
            elif hat[1] == -1:
                self.movement_direction = "DOWN"
        else:    
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                self.movement_direction = "UP"
            elif pressed[pygame.K_DOWN]:
                self.movement_direction = "DOWN"
            else:
                self.movement_direction = None

    def move(self, x,y):
        self.rect.move_ip(x,y)
        self.hitbox.move_ip(x,y)

    def update(self, game_engine, camera):
        if self.movement_direction == 'UP' and self.rect.top > 0:
                y_move = -1 * self.movement_factor
                if self.rect.top + y_move < 0:
                    y_move = -1 * self.rect.top
                self.move(0, y_move)
        elif self.movement_direction == 'DOWN' \
             and self.rect.bottom < game_engine.screen_height:
                y_move = self.movement_factor
                if self.rect.bottom + y_move > game_engine.screen_height:
                    y_move = game_engine.screen_height - self.rect.bottom
                self.move(0, y_move)

    def draw(self, screen, camera, display_hitbox):
        #All coordinates already in camera view
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)

        if display_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)

class Enemy():
    def __init__(self, engine):
        self.centerx = engine.screen_width - 60
        self.centery = engine.screen_height // 2
        self.height = 90
        self.width = 15
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.centerx, self.centery)
        self.hitbox = self.rect.copy()

        self.movement_factor = 3

    def move(self, x,y):
        self.rect.move_ip(x,y)
        self.hitbox.move_ip(x,y)

    def update(self, engine, entity_mgr, camera):
        if entity_mgr.invis_ball:
            if self.rect.center[1] - entity_mgr.invis_ball.rect.center[1] > 3 \
               and self.rect.top > 0:
                self.move(0, -1 * self.movement_factor)
            elif self.rect.center[1] - entity_mgr.invis_ball.rect.center[1] < -3 \
               and self.rect.bottom < engine.screen_height:
                self.move(0, self.movement_factor)

    def draw(self, screen, camera, display_hitbox):
        #All coordinates already in camera view
        pygame.draw.rect(screen, (255,255,255), self.rect, 0)

        if display_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)

if __name__ == '__main__':
    main()
