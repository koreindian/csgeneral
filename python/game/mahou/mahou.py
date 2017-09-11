#Game beginning

import sys, os, pygame, math, time
import console as cmd_console
import mahou_utils
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


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

        if self.paused:
            paused = font.render('Paused', False, red)
            screen.blit(paused, (self.screen_width // 2  - paused.get_width()  // 2, \
                                 self.screen_height // 2 - paused.get_height() // 2))        
        
        player_health = font.render('Health: ' + str(entity_mgr.player_ship.health), False, red)
        screen.blit(player_health, (0,0))

        FPS = font.render('FPS: ' + str(self.get_FPS()), False, red)
        screen.blit(FPS, (self.screen_width - FPS.get_width(), 0))
 

class Event_Manager:
    def __init__(self):
        self.level = 0

    def update(self, game_engine, entity_manager):
        if   self.level == 1: self.update_lvl1(game_engine, entity_manager)
        elif self.level == 2: self.update_lvl2(game_engine, entity_manager)    

    def update_lvl1(self, engine, entity_mgr): 
        time = engine.total_frames_played

        if time == 1:
            entity_mgr.create_enemy_ship(360, 300)
        if time == 180:
            entity_mgr.create_enemy_ship(180, 300)
            entity_mgr.create_enemy_ship(540, 300)
        if time == 360:
            entity_mgr.create_enemy_ship(144, 300)
            entity_mgr.create_enemy_ship(288, 300)
            entity_mgr.create_enemy_ship(432, 300)

    def update_lvl2(self, engine, entity_mgr):
        return
 
class Entity_Manager:
    def __init__(self, engine):
        self.player_ship = Player_Ship()
        self.enemy_ship_list = []
        self.player_bullet_list = []
        self.enemy_bullet_list = []
        self.background = Background("background_concept_1.jpg", engine)

    def restart(self):
        self.player_ship = Player_Ship()
        self.enemy_ship_list = []
        self.player_bullet_list = []
        self.enemy_bullet_list = []
        self.background = Background("background_concept_1.jpg")
        
    def create_enemy_ship(self, x_spawn, y_spawn, shoot_interval=10):
        ship = Enemy_Ship(x_spawn, y_spawn, shoot_interval)
        self.enemy_ship_list += [ship]
        return ship

    def update(self, game_engine):
        #Update Cycle: Update bullet positions, Update Ship Positions and Apply Damage, Delete all deletion candidates
        for bullet in self.player_bullet_list:
            bullet.update()
        for bullet in self.enemy_bullet_list:
            bullet.update()
        
        self.background.update()
        self.player_ship.update(self.player_bullet_list, self.enemy_bullet_list, game_engine)
        for ship in self.enemy_ship_list:
            ship.update(self, game_engine)

        self.player_bullet_list = [bullet for bullet in self.player_bullet_list \
                                   if not bullet.deletion_criteria_met(game_engine.screen.get_rect(), self.enemy_ship_list)]
        self.enemy_bullet_list = [bullet for bullet in self.enemy_bullet_list \
                                   if not bullet.deletion_criteria_met(game_engine.screen.get_rect(), [self.player_ship])]
        self.enemy_ship_list = [ship for ship in self.enemy_ship_list if not ship.deletion_criteria_met()]

    def draw(self, screen):
        screen.fill((0,0,0))
        self.background.draw(screen)
        pygame.sprite.RenderPlain(self.player_ship).draw(screen)

        for enemy in self.enemy_ship_list:
            pygame.sprite.RenderPlain(enemy).draw(screen)

        for bullet in self.player_bullet_list:
            screen.blit(bullet.image, bullet.rect)
        
        for bullet in self.enemy_bullet_list:
            screen.blit(bullet.image, bullet.rect)

def main():
    engine = Game_Engine()
    screen = engine.screen
    entity_mgr = Entity_Manager(engine)
    event_mgr = Event_Manager()
    event_mgr.level = 1
    console = cmd_console.Console(engine)

    magi = entity_mgr.player_ship

    while 1:
        engine.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if console.open:                         #Console input processing
                console.process_event(event, engine)
            else:                                    #Regular game input processing
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        magi.shooting = True    
                    if event.key == pygame.K_r:
                        engine.restart()
                        entity_mgr.restart()
                        magi = entity_mgr.player_ship    
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
                event_mgr.update(engine, entity_mgr)
                entity_mgr.update(engine)
                engine.paused_manual_frame_tick = False
           
            entity_mgr.draw(engine.screen)
            engine.draw(entity_mgr)

        else:
            screen.fill((0,0,0))
            game_over_text_surface = engine.generic_font.render('Game Over', False, (255,0,0))
            screen.blit(game_over_text_surface, (engine.screen_width // 2 - game_over_text_surface.get_width() // 2, \
                                                 engine.screen_height // 2 - game_over_text_surface.get_height() // 2))

        console.draw(screen)
        pygame.display.flip()

    
class Background():
    def __init__(self, name, engine):
        self.image, self.rect = mahou_utils.load_image(name)
        self.rect.top = engine.screen_height - self.image.get_height()
        print (self.rect)
        self.scroll_speed = 1
        self.scroll_acceleration = 0

    def update(self):
        self.scroll_speed += self.scroll_acceleration
        self.rect.move_ip(0, self.scroll_speed)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        

class Player_Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = mahou_utils.load_image('ship_generic1_transparent.png')
        self.rect.topleft = (360,800)

        self.movement_direction = None
        self.movement_direction_diag = False #If moving diagonally, don't update direction from keydown event
        self.movement_factor = 8
        self.movement_factor_shooting_reduction = 3
        self.shooting = False

        self.health = 100

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

    def update(self, player_bullet_list, enemy_bullet_list, game_engine):
        if self.health <= 0:
            game_engine.game_over = True
            return

        movement_amount = (self.movement_factor - self.movement_factor_shooting_reduction ) if self.shooting \
                           else self.movement_factor

        #TODO: Can move slightly outside of frame inappropriately.
        if self.movement_direction:
            if self.movement_direction == 'UP' and self.rect.top > 0:
                    self.rect.move_ip(0, -1 * movement_amount)
            elif self.movement_direction == 'LEFT' and self.rect.left > 0:
                    self.rect.move_ip(-1 * movement_amount, 0)
            elif self.movement_direction == 'RIGHT' and self.rect.right < game_engine.screen_width:
                    self.rect.move_ip(movement_amount, 0)
            elif self.movement_direction == 'DOWN' and self.rect.bottom < game_engine.screen_height:
                    self.rect.move_ip(0, movement_amount)
            elif self.movement_direction == 'UP_LEFT':
                    x = -1 * math.cos(math.pi / 4) * movement_amount
                    y = -1 * math.sin(math.pi / 4) * movement_amount
                    
                    if self.rect.top > 0 and self.rect.left > 0:
                        self.rect.move_ip(x,y)
                    elif self.rect.top > 0 and not self.rect.left > 0:
                        self.rect.move_ip(0,-1 * movement_amount)
                    elif not self.rect.top > 0 and self.rect.left > 0:
                        self.rect.move_ip(-1 * movement_amount,0)

            elif self.movement_direction == 'UP_RIGHT':
                    x = math.cos(math.pi / 4) * movement_amount
                    y = -1 * math.sin(math.pi / 4) * movement_amount
                 
                    if self.rect.top > 0 and self.rect.right < game_engine.screen_width:
                        self.rect.move_ip(x,y)
                    elif self.rect.top > 0 and not self.rect.right < game_engine.screen_width:
                        self.rect.move_ip(0,-1 * movement_amount)
                    elif not self.rect.top > 0 and self.rect.right < game_engine.screen_width:
                        self.rect.move_ip(movement_amount,0)

            elif self.movement_direction == 'DOWN_LEFT':
                    x = -1 * math.cos(math.pi / 4) * movement_amount
                    y = math.sin(math.pi / 4) * movement_amount
                    
                    if self.rect.bottom < game_engine.screen_height and self.rect.left > 0:
                        self.rect.move_ip(x,y)
                    elif self.rect.bottom < game_engine.screen_height and not self.rect.left > 0:
                        self.rect.move_ip(0,movement_amount)
                    elif not self.rect.bottom < game_engine.screen_height and self.rect.left > 0:
                        self.rect.move_ip(-1 * movement_amount,0)

            elif self.movement_direction == 'DOWN_RIGHT':
                    x = math.cos(math.pi / 4) * movement_amount
                    y = math.sin(math.pi / 4) * movement_amount
                    
                    if self.rect.bottom < game_engine.screen_height and self.rect.right < game_engine.screen_width:
                        self.rect.move_ip(x,y)
                    elif self.rect.bottom < game_engine.screen_height and not self.rect.right < game_engine.screen_width:
                        self.rect.move_ip(0,movement_amount)
                    elif not self.rect.bottom < game_engine.screen_height and self.rect.right < game_engine.screen_width:
                        self.rect.move_ip(movement_amount,0)

        for bullet in enemy_bullet_list:
            if pygame.sprite.collide_rect(bullet, self):
                self.health -= bullet.damage

        if self.shooting:
            player_bullet_list += self.triple_shoot()

    #Returns list of bullets
    def shoot(self):
        b = Bullet (self.rect.center, 0, -25)
        return [b]

    def triple_shoot_cone(self):
        b1 = Bullet (self.rect.center, -5, -25)
        b2 = Bullet (self.rect.center, 0, -25)
        b3 = Bullet (self.rect.center, 5, -25)
        return [b1,b2,b3]

    def triple_shoot(self):
        b1 = Bullet ((self.rect.center[0] - 100, self.rect.center[1]), 0, -25)
        b2 = Bullet ((self.rect.center[0] + 100, self.rect.center[1]), 0, -25)
        b3 = Bullet (self.rect.center, 0, -25)
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

    def update(self, entity_mgr, game_engine):
        if self.rect.right >= game_engine.screen_width:
            self.movement_direction = -1
        if self.rect.left <= 0:
            self.movement_direction = 1
    
        self.rect.move_ip(self.movement_direction * self.movement_factor, 0)
       
        #Rotate image to follow player
        x_diff = entity_mgr.player_ship.rect.center[0] - self.rect.center[0]
        y_diff = entity_mgr.player_ship.rect.center[1] - self.rect.center[1]

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

        entity_mgr.enemy_bullet_list += self.shoot(entity_mgr.player_ship)

    def deletion_criteria_met(self):
        return self.health <= 0

    #Returns list of bullets
    def shoot(self, player_ship):
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
            ts = self.targeted_shot(player_ship)
            bullets += ts
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1
        
        return bullets

    def targeted_shot (self, player_ship):
        velocity = 5
        x_source = self.rect.center[0]
        y_source = self.rect.center[1]
        x_target = player_ship.rect.center[0]
        y_target = player_ship.rect.center[1]

        vx = vy = 0

        x = x_target - x_source
        y = y_target - y_source

        if x == 0:
            vx = 0
            vy = velocity
        elif y == 0:
            vx = velocity
            vy = 0
        else:
            theta = math.atan(abs(y/x))
            vx = math.cos(theta) * velocity if x > 0 else -1 * math.cos(theta) * velocity
            vy = math.sin(theta) * velocity if y > 0 else -1 * math.sin(theta) * velocity
 
        b = Bullet(self.rect.center, vx, vy, dmg=1)
        return [b]
 
    def radial_shot(self, num_bullets):
        output = []
        velocity = 20
        for i in range(num_bullets):
            theta = (2 * math.pi) * (i / num_bullets)
            vx = velocity * round(math.sin(theta), 10)
            vy = velocity * round(math.cos(theta), 10)
            b = Bullet(self.rect.center, vx, vy)
            output.append(b)
        return output

    def radial_shot_inverse(self, num_bullets):
        output = []
        velocity = 5
        for i in range(num_bullets):
            theta = (2 * math.pi) * (i / num_bullets)
            vxi = -1 * velocity * round(math.sin(theta), 10)
            vyi = -1 * velocity * round(math.cos(theta), 10)
            b = Inverse_Bullet((0,0), self.rect.center, vx=vxi, vy=vyi)
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
        b = Bullet(self.rect.center, vx, vy, dmg=5)
        return [b]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, parent_center, vx=0, vy=0, dmg=1):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = mahou_utils.load_image('bullet_generic_transparent.png')
        self.rect.center = parent_center
        self.velocity_vertical = vy
        self.velocity_horizontal = vx
        
        #Velocities will likely be fractions of pixels, so track the real x and y
        #separately from the bullet sprite's rectangle coordinates
        self.realx = self.rect.x
        self.realy = self.rect.y

        self.damage = dmg

    def update(self):
        self.realx += self.velocity_horizontal
        self.realy += self.velocity_vertical

        self.rect.move_ip(self.realx - self.rect.x, self.realy - self.rect.y)

    #Returns true if bullet should be removed from the game engine's bullet tracking lists
    #Different bullets have different deletion criteria
    def deletion_criteria_met(self, screen_rect, opponent_ships):
        if not screen_rect.colliderect(self.rect):
            return True

        for ship in opponent_ships:
            if pygame.sprite.collide_rect(ship, self):
                return True

        return False
    

class Gravity_Bullet(Bullet):
    def __init__(self, parent_center, vx=0, vy=0, ax=0, ay=0, dmg=1):
        Bullet.__init__(self, parent_center, vx, vy, dmg)
        self.acceleration_vertical = ay
        self.acceleration_horizontal = ax

    def update(self):
        self.velocity_vertical += self.acceleration_vertical
        self.velocity_horizontal += self.acceleration_horizontal 
        self.realx += self.velocity_horizontal
        self.realy += self.velocity_vertical
       
        self.rect.move_ip(self.realx - self.rect.x, self.realy - self.rect.y)


#Bullets which start off screen, and terminate at a point on the screen
class Inverse_Bullet(Gravity_Bullet):
    def __init__(self, spawn_point, terminating_point, vx=0, vy=0, ax=0, ay=0, dmg=1):
        Gravity_Bullet.__init__(self, spawn_point, vx, vy, ax, ay, dmg)
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


