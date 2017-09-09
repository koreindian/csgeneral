#Game beginning

import sys, os, pygame, math
import console as cmd_console

pygame.init()


#
# The Game Engine manages all global state (ex. paused, game_over, tick clock)
#
class Game_Engine:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen_height = 900
        self.screen_width = 720
        self.paused = False
        self.game_over = False

        self.generic_font = pygame.font.SysFont('Courier', 30)

def main():
    engine = Game_Engine()
    screen = pygame.display.set_mode((engine.screen_width, engine.screen_height))
    console = cmd_console.Console(engine)

    magi = Magician()
    npc_magi = Enemy_Magician()

    bullet_list = []
    enemies_list = [npc_magi]
    enemy_bullet_list = []

    while 1:
        engine.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if console.open:                         #Console input processing
                console.process_event(event, engine)
            else:                                    #Regular game input processing
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        magi.shooting = True    
                    if event.key == pygame.K_r:
                        pass
                        #if game_over:
                        #    game_over = False
                        #    magi.health = 100    
                    if event.key == pygame.K_p:
                        engine.paused = not engine.paused
                    if event.key == pygame.K_BACKQUOTE: #Enter console mode
                        console.open = True
                    if event.key == pygame.K_UP or \
                       event.key == pygame.K_RIGHT or \
                       event.key == pygame.K_DOWN or \
                       event.key == pygame.K_LEFT:
                        magi.movement_direction = event.key
                if event.type == pygame.KEYUP:
                    if magi.movement_direction == event.key:
                        magi.movement_direction = None
                    if event.key == pygame.K_SPACE:
                        magi.shooting = False 
        
        console.update()

        if engine.game_over:
            screen.fill((0,0,0))
            game_over_text_surface = engine.generic_font.render('Game Over', False, (255,0,0))
            screen.blit(game_over_text_surface, (engine.screen_width // 2, engine.screen_height // 2))

        elif not engine.paused:

            #################################
            # Player Update
            #################################

            ### All of this needs to be refactored into update functions
            magi.update(engine)

            if magi.shooting:
                bullet_list += magi.triple_shoot()

            #print('bullets:',  bullet_list)
            for bullet in bullet_list:
                bullet.update()
                if not screen.get_rect().colliderect(bullet.rect):
                    bullet_list.remove(bullet)

                for enemy in enemies_list:
                    if pygame.sprite.collide_rect(bullet, enemy):
                        enemy.health -= bullet.damage
                        bullet_list.remove(bullet)

            #################################
            # Enemy update
            #################################
            for enemy in enemies_list:
                enemy.update(enemy_bullet_list, engine)
                if enemy.health <= 0:
                    enemies_list.remove(enemy)

            for bullet in enemy_bullet_list:
                bullet.update()
                if bullet.deletion_criteria_met(screen.get_rect()):
                    enemy_bullet_list.remove(bullet)

                if pygame.sprite.collide_rect(bullet, magi):
                    magi.health -= bullet.damage
                    enemy_bullet_list.remove(bullet)
                    

        #################################
        # Draw Screen
        #################################
        screen.fill((0,0,0))
        pygame.sprite.RenderPlain(magi).draw(screen)

        for enemy in enemies_list:
            pygame.sprite.RenderPlain(enemy).draw(screen)

        for bullet in bullet_list:
            screen.blit(bullet.image, bullet.rect)

        for bullet in enemy_bullet_list:
            screen.blit(bullet.image, bullet.rect)
         
        player_health_text_surface = engine.generic_font.render('Health: ' + str(magi.health), False, (255,0,0))
        screen.blit(player_health_text_surface, (0,0))

        console.draw(screen)
        pygame.display.flip()


def load_image(name):
    fullname = os.path.join('data/', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    return image, image.get_rect()

#Rectangle collision detection
#Note: just for practice. In real code use pygame.sprite.collide_rect(left,right)
def is_collision(sprite1, sprite2):
    rect1 = sprite1.rect
    rect2 = sprite2.rect

    if (rect1.x < rect2.x + rect2.w and \
        rect1.x + rect1.w > rect2.x and \
        rect1.y < rect2.y + rect2.h and \
        rect1.y + rect1.h > rect2.y):
        return True
    else:
        return False  
    

class Magician(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ship_generic1transparent.png')
        self.rect.topleft = (360,800)

        self.movement_direction = None
        self.movement_factor = 8
        self.movement_factor_shooting_reduction = 3
        self.shooting = False

        self.health = 100

    def update(self, game_engine):
        if self.health <= 0:
            game_engine.game_over = True
            return

        movement_amount = (self.movement_factor - self.movement_factor_shooting_reduction ) if self.shooting \
                           else self.movement_factor
        if self.movement_direction:
            if self.movement_direction == pygame.K_UP and \
               self.rect.top > 0:
                    self.rect.move_ip(0, -1 * movement_amount)
            if self.movement_direction == pygame.K_LEFT and \
               self.rect.left > 0:
                    self.rect.move_ip(-1 * movement_amount, 0)
            if self.movement_direction == pygame.K_RIGHT and \
               self.rect.right < game_engine.screen_width:
                    self.rect.move_ip(movement_amount, 0)
            if self.movement_direction == pygame.K_DOWN and \
               self.rect.bottom < game_engine.screen_height:
                    self.rect.move_ip(0, movement_amount)

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
        b1 = Bullet ((self.rect.center[0] - 20, self.rect.center[1]), 0, -25)
        b2 = Bullet ((self.rect.center[0] + 20, self.rect.center[1]), 0, -25)
        b3 = Bullet (self.rect.center, 0, -25)
        return [b1,b2,b3]

class Enemy_Magician(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('ship_generic2transparent.png')
        self.rect.topleft = (360,50)

        self.movement_direction = 0  #1 for right, -1 for left, 0 for still
        self.movement_factor = 5

        self.shoot_counter = 0
        self.shoot_interval = 10

        self.health = 100

    def update(self, enemy_bullet_list, game_engine):
        if self.rect.right >= game_engine.screen_width:
            self.movement_direction = -1
        if self.rect.left <= 0:
            self.movement_direction = 1
    
        self.rect.move_ip(self.movement_direction * self.movement_factor, 0)
        
        if self.shoot_counter % self.shoot_interval == 0:
            enemy_bullet_list += self.shoot()
            #enemy_bullet_list += self.radial_shot(8)
            #enemy_bullet_list += self.spiral_shot(43,5)
            self.shoot_counter = 1
        else:
            self.shoot_counter += 1
        

    #Returns list of bullets
    def shoot(self):
        #b = Bullet (self.rect.center, 0, 10)
        #gb1 = Gravity_Bullet(self.rect.center, 9, -4, 0, 0.1)
        #gb2 = Gravity_Bullet(self.rect.center, -2, -4, 0, 0.1)
        #iv = Inverse_Bullet((400,800), self.rect.center)
        #iv.init_velocities(120)
        #return [b, gb1, gb2]
        return self.radial_shot_inverse(20)

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
        #print(vx,vy)
        return [b]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, parent_center, vx=0, vy=0, dmg=1):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bullet_generic_transparent.png')
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
    def deletion_criteria_met(self, screen_rect):
        return not screen_rect.colliderect(self.rect)
    

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
        print("(" + str(x0) + "," + str(y0) + ")")
        self.realx = x0
        self.realy = y0
 
    def deletion_criteria_met(self, screen_rect):
        return self.tpoint_hitbox.colliderect(self.rect) 
        
if __name__ == '__main__':
    main()


