#Game beginning

import sys, os, pygame, math, time, random
import console as cmd_console
import mahou_utils
os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    
    engine = Game_Engine()
    screen = engine.screen
    entity_mgr = Entity_Manager(engine)
    event_mgr = Event_Manager()
    event_mgr.level = 1
    camera = Camera(engine, entity_mgr)
    sound_bank = Sound_Bank()

    console = cmd_console.Console(engine)

    while 1:
        engine.clock.tick(60)
        magi = entity_mgr.player_ship
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if console.open:                         #Console input processing
                console.process_event(event, engine, entity_mgr)
            else:                                    #Regular game input processing
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        magi.shooting = True    
                    if event.key == pygame.K_r:
                        engine.restart()
                        entity_mgr.restart(engine)
                        camera.restart(engine, entity_mgr)
                    if event.key == pygame.K_p:
                        engine.paused = not engine.paused
                    if event.key == pygame.K_BACKQUOTE: #Enter console mode
                        console.open = True
                    if (event.key == pygame.K_UP or \
                       event.key == pygame.K_RIGHT or \
                       event.key == pygame.K_DOWN or \
                       event.key == pygame.K_LEFT ) and \
                       not magi.movement_direction_diag: #Do not update direction on press if already moving diagonally
                            magi.determine_direction()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or \
                       event.key == pygame.K_RIGHT or \
                       event.key == pygame.K_DOWN or \
                       event.key == pygame.K_LEFT:
                            magi.determine_direction()
                    if event.key == pygame.K_z:
                        magi.shooting = False 
                    if engine.paused:
                        if event.key == pygame.K_f:
                            engine.paused_manual_frame_tick = True
                        
        engine.update()
        console.update()
        
        if not engine.game_over:
            if not engine.paused or engine.paused_manual_frame_tick:
                event_mgr.update(engine, entity_mgr, sound_bank)
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

class Sound_Bank:
    def __init__(self):
        #Channels:
        #    0 = Bg
        #    1 = Player
        pygame.mixer.set_num_channels(8)
        gunshot1_path = os.path.join('data/', 'gunshot1.wav')
        self.gunshot1 = pygame.mixer.Sound(gunshot1_path)
        
        self.bgm_interstellar_path = os.path.join('data/', 'Death M.D. - Interstellar Slide.mp3')

        self.music_paused = False

    def play_level1_music(self):
        pygame.mixer.music.load(self.bgm_interstellar_path)
        pygame.mixer.music.play(0)

    def player_shoot(self):
        player_channel1 = pygame.mixer.Channel(1)
        player_channel1.play(self.gunshot1)

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
        self.camera_worldy = entity_mgr.background.image.get_height() - engine.screen_height
        self.camera_vx = 0
        self.camera_vy = -1

    def update(self):
        self.camera_worldx += self.camera_vx
        self.camera_worldy += self.camera_vy
        #print("Camera: (" +str(self.camera_worldx) + "," + str(self.camera_worldy)+ ")")

    def restart(self, engine, entity_mgr):
        self.camera_worldx = 0 
        self.camera_worldy = entity_mgr.background.image.get_height() - engine.screen_height
        self.camera_vx = 0
        self.camera_vy = -1

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
#
# The Game Engine manages all global state (ex. paused, game_over, tick clock)
#
class Game_Engine:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen_height = 900
        self.screen_width = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.paused = False
        self.paused_manual_frame_tick = False #Variable to move one frame forward while in paused mode
        
        self.player_lives = 2
        self.player_continues = 0
        self.game_over = False

            
        self.total_frames = 0 #Number of frames since game began
        self.total_frames_played = 0 #Excludes paused and game-over frames
        self.started_time = time.time()
        self.current_time = time.time()
        self.elapsed_time = 0

        self.generic_font = pygame.font.SysFont('Courier', 30)


    def restart(self):
        self.total_frames = 0
        self.total_frames_played = 0
        self.started_time = time.time()
        self.current_time = time.time()
        self.elapsed_time = 0
        self.player_lives = 2
        self.player_continues = 0
        self.game_over = False
                

    def update(self):
        self.total_frames += 1

        if (not self.paused or self.paused_manual_frame_tick) and not self.game_over:
            self.total_frames_played += 1

        self.current_time = time.time()
        self.elapsed_time = self.current_time - self.started_time
        
    def get_FPS(self):
        return format(self.total_frames / self.elapsed_time, '.2f')

    def draw(self, entity_mgr):
        red = (255,0,0)
        font = self.generic_font
        screen = self.screen

        if self.game_over:
            screen.fill((0,0,0))
            game_over_text_surface = self.generic_font.render('Game Over', False, (255,0,0))
            screen.blit(game_over_text_surface, (self.screen_width // 2 - game_over_text_surface.get_width() // 2, \
                                                 self.screen_height // 2 - game_over_text_surface.get_height() // 2))
        else:
            if self.paused:
                paused = font.render('Paused', False, red)
                screen.blit(paused, (self.screen_width // 2  - paused.get_width()  // 2, \
                                     self.screen_height // 2 - paused.get_height() // 2))        
            
            player_health = font.render('Health: ' + str(entity_mgr.player_ship.health), False, red)
            screen.blit(player_health, (0,0))

            player_lives = font.render("Lives: " + str(self.player_lives), False, red)
            screen.blit(player_lives, (0, font.get_height())) 

            FPS = font.render('FPS: ' + str(self.get_FPS()), False, red)
            screen.blit(FPS, (self.screen_width - FPS.get_width(), 0))
 
            time = font.render('Time: ' + str(self.total_frames_played), False, red)
            screen.blit(time, (self.screen_width - time.get_width(), font.get_height()))

class Event_Manager:
    def __init__(self):
        self.level = 0

    def update(self, game_engine, entity_manager, sound_bank):
        if   self.level == 1: self.update_lvl1(game_engine, entity_manager, sound_bank)
        elif self.level == 2: self.update_lvl2(game_engine, entity_manager, sound_bank)    

    def update_lvl1(self, engine, entity_mgr, sound_bank):
        time = engine.total_frames_played
        bg = entity_mgr.background
        level_height = bg.rect.height
        level_width = bg.rect.width
        
        tsi = 200
        tv = 1

        if time == 1:
            sound_bank.play_level1_music()
            entity_mgr.create_enemy_tank1((700, level_height - 600), (-100, level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((700, level_height - 700), (-100, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((700, level_height - 800), (-100, level_height - 600), tv, tsi)
                                                                                                       
            entity_mgr.create_enemy_tank1((600, level_height - 600), (-200, level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((600, level_height - 700), (-200, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((600, level_height - 800), (-200, level_height - 600), tv, tsi)
                                                                                                       
            entity_mgr.create_enemy_tank1((500, level_height - 600), (-300, level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((500, level_height - 700), (-300, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((500, level_height - 800), (-300, level_height - 600), tv, tsi)
                                                                                                       
            entity_mgr.create_enemy_tank1((400, level_height - 600), (-400, level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((400, level_height - 700), (-400, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((400, level_height - 800), (-400, level_height - 600), tv, tsi)
                                                                                                       
            entity_mgr.create_enemy_tank1((300, level_height - 600), (-500, level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((300, level_height - 700), (-500, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((300, level_height - 800), (-500, level_height - 600), tv, tsi)
                                                                                                       
            entity_mgr.create_enemy_tank1((200, level_height - 600), (-600, level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((200, level_height - 700), (-600, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((200, level_height - 800), (-600, level_height - 600), tv, tsi)
        if time == 300:
            entity_mgr.create_enemy_ship1(180, level_height - 1200)
            entity_mgr.create_enemy_ship1(540, level_height - 1200)
        if time == 400:
            entity_mgr.create_enemy_ship2(360, level_height - 1400)
            
            entity_mgr.create_enemy_tank1((100, level_height - 1500), (100, level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((100, level_height - 1600), (100, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((100, level_height - 1700), (100, level_height - 600), tv, tsi)
            
            entity_mgr.create_enemy_tank1((level_width - 100, level_height - 1500), \
                                          (level_width - 100 , level_height - 400), tv, tsi)
            entity_mgr.create_enemy_tank1((level_width - 100, level_height - 1600), \
                                          (level_width - 100, level_height - 500), tv, tsi)
            entity_mgr.create_enemy_tank1((level_width - 100, level_height - 1700), \
                                          (level_width - 100, level_height - 600), tv, tsi)
        if time == 470:
            entity_mgr.create_enemy_ship2(360, level_height - 1500)
        if time == 540:
            entity_mgr.create_enemy_ship2(360, level_height - 1600)

    def update_lvl2(self, engine, entity_mgr):
        return
 
class Entity_Manager:
    def __init__(self, engine):
        self.player_ship = Player_Ship()
        self.enemy_ship_list = []
        self.player_bullet_list = []
        self.enemy_bullet_list = []
        self.background = Background("background_concept_1.jpg", engine)

        self.display_hitboxes = True

    def restart(self, engine):
        self.player_ship = Player_Ship()
        self.enemy_ship_list = []
        self.player_bullet_list = []
        self.enemy_bullet_list = []
        self.background = Background("background_concept_1.jpg", engine)
        
    def create_enemy_ship(self, x_spawn, y_spawn, shoot_interval=10):
        ship = Enemy_Ship(x_spawn, y_spawn, shoot_interval)
        self.enemy_ship_list += [ship]
        return ship

    def create_enemy_ship1(self, x_spawn, y_spawn):
        ship = Enemy_Ship1(x_spawn, y_spawn)
        self.enemy_ship_list += [ship]
        return ship

    def create_enemy_ship2(self, x_spawn, y_spawn):
        ship = Enemy_Ship2(x_spawn, y_spawn)
        self.enemy_ship_list += [ship]
        return ship

    def create_enemy_tank1(self, source_coords, dest_coords, velocity, shoot_interval):
        tank = Tank1(source_coords, dest_coords, velocity, shoot_interval)
        self.enemy_ship_list += [tank]
        return tank

    def update(self, game_engine, camera, sound_bank):
        #Update Cycle: Update bullet positions, Update Ship Positions and Apply Damage, Delete all deletion candidates
        for bullet in self.player_bullet_list:
            bullet.update()
        for bullet in self.enemy_bullet_list:
            bullet.update()
        
        self.background.update()
        self.player_ship.update(self.player_bullet_list, self.enemy_bullet_list, game_engine, self, camera, sound_bank)
        for ship in self.enemy_ship_list:
            ship.update(self, game_engine, camera)

        self.player_bullet_list = [bullet for bullet in self.player_bullet_list \
                                   if not bullet.deletion_criteria_met(game_engine.screen.get_rect(), \
                                                                       self.enemy_ship_list, self, camera)]
        self.enemy_bullet_list = [bullet for bullet in self.enemy_bullet_list \
                                   if not bullet.deletion_criteria_met(game_engine.screen.get_rect(), \
                                                                       [self.player_ship], self, camera)]
        self.enemy_ship_list = [ship for ship in self.enemy_ship_list if not ship.deletion_criteria_met()]

    def draw(self, game_engine, camera):
        screen = game_engine.screen
        screen.fill((0,0,0))
        self.background.draw(game_engine, camera)
        
        self.player_ship.draw(screen, self.display_hitboxes)

        for enemy in self.enemy_ship_list:
            enemy.draw(screen, camera, self.display_hitboxes)

        for bullet in self.player_bullet_list:
            bullet.draw(screen, camera, self.display_hitboxes)
        
        for bullet in self.enemy_bullet_list:
            bullet.draw(screen, camera, self.display_hitboxes)

class Background():
    def __init__(self, name, engine):
        self.image, self.rect = mahou_utils.load_image(name)
        self.rect.top = 0 #engine.screen_height - self.image.get_height()

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

class Player_Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #The player is always in Camera coordinates, and never in World coordinates
        self.image, self.rect = mahou_utils.load_image('ship_generic1_transparent.png')
        self.rect.topleft = (360,800)
        self.hitbox_width = 10
        self.hitbox_height = 10
        self.hitbox = self.rect.copy()
        self.hitbox.inflate_ip(-1 * (self.rect.width - self.hitbox_width), \
                               -1 * (self.rect.height - self.hitbox_height) )

        self.movement_direction = None
        self.movement_direction_diag = False #If moving diagonally, don't update direction from keydown event
        self.movement_factor = 8
        self.movement_factor_shooting_reduction = 3

        self.shooting = False
        self.shoot_counter = 0
        self.shoot_interval = 4


        self.health = 1

        self.shoot_function = self.shoot_br_wide

    def determine_direction(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] and pressed[pygame.K_LEFT]:
            self.movement_direction = "UP_LEFT"
            self.direction_diag = True
        elif pressed[pygame.K_UP] and pressed[pygame.K_RIGHT]:
            self.movement_direction = "UP_RIGHT"
            self.direction_diag = True
        elif pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT]:
            self.movement_direction = "DOWN_LEFT"
            self.direction_diag = True
        elif pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT]:
            self.movement_direction = "DOWN_RIGHT"
            self.direction_diag = True
        elif pressed[pygame.K_UP]:
            self.movement_direction = "UP"
            self.direction_diag = False
        elif pressed[pygame.K_LEFT]:
            self.movement_direction = "LEFT"
            self.direction_diag = False
        elif pressed[pygame.K_RIGHT]:
            self.movement_direction = "RIGHT"
            self.direction_diag = False
        elif pressed[pygame.K_DOWN]:
            self.movement_direction = "DOWN"
            self.direction_diag = False
        else:
            self.movement_direction = None
            self.direction_diag = False

    def move(self, x,y):
        self.rect.move_ip(x,y)
        self.hitbox.move_ip(x,y)

    def update(self, player_bullet_list, enemy_bullet_list, game_engine, entity_mgr, camera, sound_bank):
        if self.health <= 0:
            if game_engine.player_lives > 0:
                game_engine.player_lives -= 1
                entity_mgr.player_ship = Player_Ship()
            else: 
                game_engine.game_over = True
            return

        movement_amount = (self.movement_factor - self.movement_factor_shooting_reduction ) if self.shooting \
                           else self.movement_factor

        #TODO: Can move slightly outside of screen inappropriately.
        if self.movement_direction:
            if self.movement_direction == 'UP' and self.rect.top > 0:
                    self.move(0, -1 * movement_amount)
            elif self.movement_direction == 'LEFT' and self.rect.left > 0:
                    self.move(-1 * movement_amount, 0)
            elif self.movement_direction == 'RIGHT' and self.rect.right < game_engine.screen_width:
                    self.move(movement_amount, 0)
            elif self.movement_direction == 'DOWN' and self.rect.bottom < game_engine.screen_height:
                    self.move(0, movement_amount)
            elif self.movement_direction == 'UP_LEFT':
                    x = -1 * math.cos(math.pi / 4) * movement_amount
                    y = -1 * math.sin(math.pi / 4) * movement_amount
                    
                    if self.rect.top > 0 and self.rect.left > 0:
                        self.move(x,y)
                    elif self.rect.top > 0 and not self.rect.left > 0:
                        self.move(0,-1 * movement_amount)
                    elif not self.rect.top > 0 and self.rect.left > 0:
                        self.move(-1 * movement_amount,0)

            elif self.movement_direction == 'UP_RIGHT':
                    x = math.cos(math.pi / 4) * movement_amount
                    y = -1 * math.sin(math.pi / 4) * movement_amount
                 
                    if self.rect.top > 0 and self.rect.right < game_engine.screen_width:
                        self.move(x,y)
                    elif self.rect.top > 0 and not self.rect.right < game_engine.screen_width:
                        self.move(0,-1 * movement_amount)
                    elif not self.rect.top > 0 and self.rect.right < game_engine.screen_width:
                        self.move(movement_amount,0)

            elif self.movement_direction == 'DOWN_LEFT':
                    x = -1 * math.cos(math.pi / 4) * movement_amount
                    y = math.sin(math.pi / 4) * movement_amount
                    
                    if self.rect.bottom < game_engine.screen_height and self.rect.left > 0:
                        self.move(x,y)
                    elif self.rect.bottom < game_engine.screen_height and not self.rect.left > 0:
                        self.move(0,movement_amount)
                    elif not self.rect.bottom < game_engine.screen_height and self.rect.left > 0:
                        self.move(-1 * movement_amount,0)

            elif self.movement_direction == 'DOWN_RIGHT':
                    x = math.cos(math.pi / 4) * movement_amount
                    y = math.sin(math.pi / 4) * movement_amount
                    
                    if self.rect.bottom < game_engine.screen_height and self.rect.right < game_engine.screen_width:
                        self.move(x,y)
                    elif self.rect.bottom < game_engine.screen_height and not self.rect.right < game_engine.screen_width:
                        self.move(0,movement_amount)
                    elif not self.rect.bottom < game_engine.screen_height and self.rect.right < game_engine.screen_width:
                        self.move(movement_amount,0)

        #Calculate bullet collisions.
        #Need to translate hitbox into world coordinates
        camera.rect_c2w(self.hitbox)
        for bullet in enemy_bullet_list:
            if self.hitbox.colliderect(bullet.hitbox):
                self.health -= bullet.damage
        camera.rect_w2c(self.hitbox)

        if self.shooting:
            player_bullet_list += self.shoot(camera, sound_bank)
        else:
            self.shoot_counter = 0

    def draw(self, screen, display_hitbox):
        #All coordinates already in camera view
        screen.blit(self.image, self.rect)

        if display_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)

    #Returns list of bullets
    def shoot(self, camera, sound_bank):
        bullets = []
        if self.shoot_counter % self.shoot_interval == 0:
            bullets += self.shoot_function(camera)
            sound_bank.player_shoot()
        
        self.shoot_counter += 1
        return bullets

    def shoot_linear(self, camera):
        wc = camera.c2w(self.rect.center) 
        b = Bullet (wc, 0, -25)
        return [b]

    def shoot_br_wide(self, camera):
        wc = camera.c2w(self.rect.center)
        vy = -80
        b1 = Bullet ((wc[0] -100, wc[1]), 0, vy)
        b2 = Bullet ((wc[0] -75 , wc[1]), 0, vy)
        b3 = Bullet ((wc[0] -50 , wc[1]), 0, vy)
        b4 = Bullet ((wc[0] -25 , wc[1]), 0, vy)
        b5 = Bullet ((wc[0]     , wc[1]), 0, vy)
        b6 = Bullet ((wc[0] +25 , wc[1]), 0, vy)
        b7 = Bullet ((wc[0] +50 , wc[1]), 0, vy)
        b8 = Bullet ((wc[0] +75 , wc[1]), 0, vy)
        b9 = Bullet ((wc[0] +100, wc[1]), 0, vy)
        return [b1,b2,b3,b4,b5,b6,b7,b8,b9]

    def triple_shoot_cone(self, camera):
        wc = camera.c2w(self.rect.center) 
        b1 = Bullet (wc, -5, -25)
        b2 = Bullet (wc, 0, -25)
        b3 = Bullet (wc, 5, -25)
        return [b1,b2,b3]

    def triple_shoot(self, camera):
        wc = camera.c2w(self.rect.center)
        b1 = Bullet ((wc[0] - 100, wc[1]), 0, -25)
        b2 = Bullet ((wc[0] + 100, wc[1]), 0, -25)
        b3 = Bullet (wc, 0, -25)
        return [b1,b2,b3]

class Enemy_Ship(pygame.sprite.Sprite):
    def __init__(self, x_spawn, y_spawn, shoot_interval=180):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = mahou_utils.load_image('ship_generic2_transparent.png')
        self.image_original = self.image #Keep this for rotations
        self.rect.center = (x_spawn, y_spawn)

        self.movement_direction = 0  #1 for right, -1 for left, 0 for still
        self.movement_factor = 5

        self.shoot_counter = 0
        self.shoot_interval = shoot_interval

        self.health = 100
        
        self.hitbox = self.rect.copy()
        self.hitbox.inflate_ip(10,10)

        self.player_tracking = True

    def update(self, entity_mgr, game_engine, camera):
        camera.rect_w2c(self.rect)
        if self.rect.right >= game_engine.screen_width:
            self.movement_direction = -1
        if self.rect.left <= 0:
            self.movement_direction = 1
    
        camera.rect_c2w(self.rect)
        self.rect.move_ip(self.movement_direction * self.movement_factor, 0)
        self.hitbox.move_ip(self.movement_direction * self.movement_factor, 0)

        #Rotate image to follow player
        if self.player_tracking:
            camera.rect_c2w(entity_mgr.player_ship.rect)
            x_diff = entity_mgr.player_ship.rect.center[0] - self.rect.center[0]
            y_diff = entity_mgr.player_ship.rect.center[1] - self.rect.center[1]
            camera.rect_w2c(entity_mgr.player_ship.rect)
            
            theta_rot = 0
            if x_diff == 0:
                if y_diff >= 0:
                    theta_rot = 0
                else:
                    theta_rot = 180
            elif y_diff == 0:
                if x_diff >= 0:
                    theta_rot = 90
                else:
                    theta_rot = 270
            elif x_diff > 0 and y_diff > 0:
                theta_radians = math.atan(x_diff/y_diff)
                theta_rot = math.degrees(theta_radians)
            elif x_diff > 0 and y_diff < 0:
                theta_radians = math.atan(abs(y_diff)/x_diff)
                theta_rot = math.degrees(theta_radians) + 90
            elif x_diff < 0 and y_diff < 0:
                theta_radians = math.atan(x_diff/y_diff)
                theta_rot = math.degrees(theta_radians) + 180
            elif x_diff < 0 and y_diff > 0:
                theta_radians = math.atan(y_diff/abs(x_diff))
                theta_rot = 270 + math.degrees(theta_radians)

            self.image, self.rect = mahou_utils.rotate_center(self.image_original, self.rect, theta_rot)

        for bullet in entity_mgr.player_bullet_list:
            if pygame.sprite.collide_rect(bullet, self):
                self.health -= bullet.damage

        entity_mgr.enemy_bullet_list += self.shoot(entity_mgr.player_ship, camera)

    def deletion_criteria_met(self):
        return self.health <= 0

    def draw(self, screen, camera, display_hitbox):
        camera.rect_w2c(self.rect)
        camera.rect_w2c(self.hitbox)

        screen.blit(self.image, self.rect)

        if display_hitbox:
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)

        camera.rect_c2w(self.rect)
        camera.rect_c2w(self.hitbox)
        
    #Returns list of bullets
    def shoot(self, player_ship, camera):
        bullets = []
        if self.shoot_counter % self.shoot_interval == 0:
            #b = Bullet (self.rect.center, 0, 10)
            #gb1 = Gravity_Bullet(self.rect.center, 2, -4, 0, 0.1)
            #gb2 = Gravity_Bullet(self.rect.center, -2, -4, 0, 0.1)
            #rb = self.radial_shot_inverse(10)
            #iv = Inverse_Bullet((400,800), self.rect.center)
            #iv.init_velocities(120)
            #bullets += [gb1, gb2]
            #bullets += rb
            ts = self.targeted_shot(player_ship, camera)
            bullets += ts
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1
        
        return bullets

    def targeted_shot (self, player_ship, camera):
        player_wc = camera.c2w(player_ship.rect.center)

        velocity = 5
        x_source = self.rect.center[0]
        y_source = self.rect.center[1]
        x_target = player_wc[0]
        y_target = player_wc[1]

        vx = vy = 0

        x = x_target - x_source
        y = y_target - y_source

        if x == 0:
            vx = 0
            vy = velocity if y > 0 else -1 * velocity
        elif y == 0:
            vx = velocity if x > 0 else -1 * velocity
            vy = 0
        else:
            theta = math.atan(abs(y/x))
            vx = math.cos(theta) * velocity if x > 0 else -1 * math.cos(theta) * velocity
            vy = math.sin(theta) * velocity if y > 0 else -1 * math.sin(theta) * velocity

        #Correct for the camera scrolling
        vx += camera.camera_vx
        vy += camera.camera_vy 

        b = Bullet(self.rect.center, vx, vy, dmg=1, player_bullet=False)
        return [b]
 
    def radial_shot(self, num_bullets):
        output = []
        velocity = 20
        for i in range(num_bullets):
            theta = (2 * math.pi) * (i / num_bullets)
            vx = velocity * round(math.sin(theta), 10)
            vy = velocity * round(math.cos(theta), 10)
            b = Bullet(self.rect.center, vx, vy, player_bullet=False)
            output.append(b)
        return output

    def radial_shot_inverse(self, num_bullets):
        output = []
        velocity = 5
        for i in range(num_bullets):
            theta = (2 * math.pi) * (i / num_bullets)
            vxi = -1 * velocity * round(math.sin(theta), 10)
            vyi = -1 * velocity * round(math.cos(theta), 10)
            b = Inverse_Bullet((0,0), self.rect.center, vx=vxi, vy=vyi, player_bullet=False)
            b.init_spawn_point(120)
            output.append(b)
        return output
    
    def spiral_shot(self, num_bullets_in_cycle, num_circles_in_cycle=1):
        velocity = 5
        if not hasattr(self, 'spiral_shot_cycle_index'):
            self.spiral_shot_cycle_index = 0

        i = self.spiral_shot_cycle_index % num_bullets_in_cycle
        self.spiral_shot_cycle_index += 1
        theta = (2 * math.pi) * (i * num_circles_in_cycle / num_bullets_in_cycle)
        vx = velocity * math.sin(theta)
        vy = velocity * math.cos(theta)
        b = Bullet(self.rect.center, vx, vy, dmg=5, player_bullet=False)
        return [b]

class Enemy_Ship1(Enemy_Ship):
    def __init__(self, x_spawn, y_spawn):
        Enemy_Ship.__init__(self, x_spawn, y_spawn, shoot_interval=3)
        self.image, self.rect = mahou_utils.load_image('plane1_concept.png')
        self.image_original = self.image
        self.rect.center = (x_spawn, y_spawn)        


        self.hitbox = self.rect.copy()
        self.hitbox.inflate_ip(5,5)

        self.health = 50
        self.player_tracking = False

        self.movement_direction = 0

    def shoot(self, player_ship, camera):
        bullets = []
        if self.shoot_counter % self.shoot_interval == 0:
            ts = self.spiral_shot(33, 2)
            bullets += ts
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1
        
        return bullets

class Enemy_Ship2(Enemy_Ship):
    def __init__(self, x_spawn, y_spawn):
        Enemy_Ship.__init__(self, x_spawn, y_spawn, shoot_interval=15)
        self.image, self.rect = mahou_utils.load_image('plane2_concept.png')
        self.image_original = self.image
        self.rect.center = (x_spawn, y_spawn)        

        self.hitbox = self.rect.copy()
        self.hitbox.inflate_ip(5,5)

        self.health = 60
        self.player_tracking = False
        
        self.movement_direction = 1

    def shoot(self, player_ship, camera):
        bullets = []
        if self.shoot_counter % self.shoot_interval == 0:
            gb1 = Gravity_Bullet(self.rect.center, 2, -4, 0, 0.1, player_bullet=False)
            gb2 = Gravity_Bullet(self.rect.center, -2, -4, 0, 0.1, player_bullet=False)
            bullets += [gb1, gb2]
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1
        
        return bullets


class Tank1(Enemy_Ship):
    def __init__(self, source_coords, dest_coords, velocity, shoot_interval):
        Enemy_Ship.__init__(self, source_coords[0], source_coords[1], shoot_interval)

        self.source_coords = source_coords
        self.dest_coords = dest_coords

        self.base_image, self.base_rect = mahou_utils.load_image('tank2_base.png')
        self.base_rect.center = source_coords
        self.base_realx = self.base_rect.center[0]
        self.base_realy = self.base_rect.center[1]

        self.turret_image, self.turret_rect = mahou_utils.load_image('tank2_turret.png')
        self.turret_image_original = self.turret_image
        self.turret_rect.center = source_coords
        self.turret_realx = self.turret_rect.center[0]
        self.turret_realy = self.turret_rect.center[1]

        movement_theta = mahou_utils.determine_angle(source_coords, dest_coords)
        x_diff = dest_coords[0] - source_coords[0]
        y_diff = dest_coords[1] - source_coords[1]
        self.base_image, self.base_rect = mahou_utils.rotate_center(self.base_image, \
                                                                    self.base_rect, \
                                                                    math.degrees(movement_theta))

        self.rect = self.base_rect
        self.hitbox = self.rect.copy()
        self.hitbox.inflate_ip(10,10)

        self.health = 15

        self.velocity = velocity

        self.shoot_counter = random.randint(0, self.shoot_interval)

        if x_diff == 0:
            self.vx = 0
            self.vy = self.velocity if y_diff > 0 else -1 * self.velocity
        elif y_diff == 0:
            self.vx = self.velocity if x_diff > 0 else -1 * self.velocity
            self.vy = 0
        else:
            theta = math.atan(abs(y_diff/x_diff))
            self.vx = math.cos(theta) * self.velocity if x_diff > 0 else -1 * math.cos(theta) * self.velocity
            self.vy = math.sin(theta) * self.velocity if y_diff > 0 else -1 * math.sin(theta) * self.velocity

    def update(self, entity_mgr, game_engine, camera):
        self.base_realx += self.vx
        self.base_realy += self.vy
        self.turret_realx += self.vx
        self.turret_realy += self.vy

        self.hitbox.move_ip(self.base_realx - self.base_rect.center[0], self.base_realy - self.base_rect.center[1])
        self.base_rect.move_ip(self.base_realx - self.base_rect.center[0], self.base_realy - self.base_rect.center[1])
        self.turret_rect.move_ip(self.turret_realx - self.turret_rect.center[0], self.turret_realy - self.turret_rect.center[1])
        self.rect = self.base_rect

        turret_player_theta = mahou_utils.determine_angle(self.turret_rect.center, \
                                                          camera.c2w(entity_mgr.player_ship.rect.center))
        self.turret_image, self.turret_rect = mahou_utils.rotate_center(self.turret_image_original, \
                                                                        self.turret_rect, \
                                                                        math.degrees(turret_player_theta))

        for bullet in entity_mgr.player_bullet_list:
            if self.hitbox.colliderect(bullet.hitbox):
                self.health -= bullet.damage

        entity_mgr.enemy_bullet_list += self.shoot(entity_mgr.player_ship, camera)

    def deletion_criteria_met(self):
        tolerance = 1
        if self.health <= 0:
            return True
        if abs(self.base_rect.center[0] - self.dest_coords[0]) < tolerance and \
           abs(self.base_rect.center[1] - self.dest_coords[1]) < tolerance:
            return True

        return False

    def draw(self, screen, camera,  display_hitbox):
        camera.rect_w2c(self.base_rect)
        camera.rect_w2c(self.turret_rect)
        
        screen.blit(self.base_image, self.base_rect)
        screen.blit(self.turret_image, self.turret_rect)
            
        if display_hitbox:
            camera.rect_w2c(self.hitbox)
            pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)
            camera.rect_c2w(self.hitbox)

        camera.rect_c2w(self.base_rect)
        camera.rect_c2w(self.turret_rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, parent_center, vx=0, vy=0, dmg=1, player_bullet=True):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = mahou_utils.load_image('bullet_generic_transparent.png')
        self.rect.center = parent_center
        self.velocity_vertical = vy
        self.velocity_horizontal = vx
        self.hitbox = self.rect.copy()
        if player_bullet:
            self.hitbox.inflate_ip(30,30)
        else:
            self.hitbox.inflate_ip(-10,-10)
        
        #Velocities will likely be fractions of pixels, so track the real x and y
        #separately from the bullet sprite's rectangle coordinates
        self.realx = self.rect.x
        self.realy = self.rect.y

        self.damage = dmg

    def update(self):
        self.realx += self.velocity_horizontal
        self.realy += self.velocity_vertical

        self.hitbox.move_ip(self.realx - self.rect.x, self.realy - self.rect.y)
        self.rect.move_ip(self.realx - self.rect.x, self.realy - self.rect.y)

    #Returns true if bullet should be removed from the game engine's bullet tracking lists
    #Different bullets have different deletion criteria
    def deletion_criteria_met(self, screen_rect, opponent_ships, entity_mgr, camera):
        #Convert to camera coordinates, as both the player ship and the screen are in that system
        camera.rect_w2c(self.rect)
        camera.rect_w2c(self.hitbox)

        if not screen_rect.colliderect(self.rect):
            camera.rect_c2w(self.rect)
            camera.rect_c2w(self.hitbox)
            return True

        for ship in opponent_ships:
            if ship != entity_mgr.player_ship:
                #Convert to camera coordinates
                camera.rect_w2c(ship.hitbox)
                if ship.hitbox.colliderect(self.hitbox):
                    camera.rect_c2w(self.rect)
                    camera.rect_c2w(self.hitbox)
                    camera.rect_c2w(ship.hitbox)
                    return True 
                camera.rect_c2w(ship.hitbox)

            elif ship.hitbox.colliderect(self.hitbox):
                camera.rect_c2w(self.rect)
                camera.rect_c2w(self.hitbox)
                return True

        camera.rect_c2w(self.rect)
        camera.rect_c2w(self.hitbox)

        return False
    
    def draw(self, screen, camera, display_hitbox):
       camera.rect_w2c(self.rect)
       screen.blit(self.image, self.rect)

       if display_hitbox:
           camera.rect_w2c(self.hitbox)
           pygame.draw.rect(screen, (255,0,0), self.hitbox, 1)   
           camera.rect_c2w(self.hitbox)

       camera.rect_c2w(self.rect)

class Gravity_Bullet(Bullet):
    def __init__(self, parent_center, vx=0, vy=0, ax=0, ay=0, dmg=1, player_bullet=True):
        Bullet.__init__(self, parent_center, vx, vy, dmg, player_bullet)
        self.acceleration_vertical = ay
        self.acceleration_horizontal = ax

    def update(self):
        self.velocity_vertical += self.acceleration_vertical
        self.velocity_horizontal += self.acceleration_horizontal 
        self.realx += self.velocity_horizontal
        self.realy += self.velocity_vertical
       
        self.hitbox.move_ip(self.realx - self.rect.x, self.realy - self.rect.y)
        self.rect.move_ip(self.realx - self.rect.x, self.realy - self.rect.y)


#Bullets which start off screen, and terminate at a point on the screen
class Inverse_Bullet(Gravity_Bullet):
    def __init__(self, spawn_point, terminating_point, vx=0, vy=0, ax=0, ay=0, dmg=1, player_bullet=True):
        Gravity_Bullet.__init__(self, spawn_point, vx, vy, ax, ay, dmg, player_bullet)
        self.tpoint = terminating_point
        self.tpoint_hitbox = pygame.Rect((self.tpoint[0], self.tpoint[1]), \
                                         (self.rect.width, self.rect.height))

    #Given spawn point, time, acceleration, and terminating point, determine the velocities
    def init_velocities(self, t):
        #x = x0 + vx * t + 1/2 ax t^2
        #vx = (x - x0 - 1/2 ax t^2) / t
        
        assert not t==0

        x = self.tpoint[0]
        y = self.tpoint[1]
        x0 = self.rect.center[0]
        y0 = self.rect.center[1]
        ax = self.acceleration_horizontal
        ay = self.acceleration_vertical
        self.velocity_horizontal = (x - x0 - 0.5 * ax * (t**2)) / t  
        self.velocity_vertical = (y - y0 - 0.5 * ay * (t**2)) / t

    #Given, time, velocity, acceleration, and terminating point, determine the spawn point
    def init_spawn_point(self, t):
        #x = x0 + vx * t + 1/2 ax t^2
        #x0 = x - vx * t - 1/2 ax t^2
        
        assert not t==0

        x = self.tpoint[0]
        y = self.tpoint[1]
        ax = self.acceleration_horizontal
        ay = self.acceleration_vertical
        vx = self.velocity_horizontal  
        vy = self.velocity_vertical

        x0 = x - vx * t - 0.5 * ax * (t ** 2)
        y0 = y - vy * t - 0.5 * ay * (t ** 2)
        self.realx = x0
        self.realy = y0
 
    def deletion_criteria_met(self, screen_rect, opponent_ships):
        tolerance = 0.02
        xdiff = abs(self.realx - self.tpoint[0])
        ydiff = abs(self.realy - self.tpoint[1])
        return xdiff < tolerance and ydiff < tolerance
        #return self.tpoint_hitbox.colliderect(self.rect) 
        
if __name__ == '__main__':
    main()


