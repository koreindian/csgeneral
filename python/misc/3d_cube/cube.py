import math
import sys
import os
import pygame
import random
import time 

os.environ['SDL_VIDEO_CENTERED'] = '1'

def main():
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    
    engine = GameEngine()
    screen = engine.screen
    
    x = WireFrame()
    x.add_points( [(0,0,0), (1,2,3), (3,2,1)] )
    x.add_lines( [(1,2)] )


    while 1:
        engine.clock.tick(60)
        process_input(engine)
        engine.update()
        c = engine.cube

        if not engine.paused or engine.paused_manual_frame_tick:
            c.update(0.01)
            engine.paused_manual_frame_tick = False
        
        background = pygame.Surface((engine.screen_width, engine.screen_height))
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        
        c.draw(engine)
        engine.draw()

        pygame.display.flip()

def global_restart(engine):
    engine.restart()

def process_input(engine):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == engine.restart_trigger[0]:
                global_restart(engine)
            elif event.key == engine.pause_trigger[0]:
                engine.paused = not engine.paused
        elif event.type == pygame.KEYUP:
            if engine.paused:
                if event.key == pygame.K_f:
                    engine.paused_manual_frame_tick = True

# The Game Engine manages all global state (ex. paused, game_over, tick clock)
class GameEngine:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.screen_height = 400
        self.screen_width = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.paused = False
        #Variable to move one frame forward while in paused mode
        self.paused_manual_frame_tick = False
        
        #Number of frames since game began
        self.total_frames = 0
        #Excludes paused and game-over frames
        self.total_frames_played = 0
        self.started_time = time.time()
        self.current_time = time.time()
        self.elapsed_time = 0

        self.generic_font = pygame.font.SysFont('Courier', 16)

        # Function to [key, arcade stick button index] mapping
        self.restart_trigger = [pygame.K_r, 4]
        self.pause_trigger   = [pygame.K_p, 5]

        self.cube = Cube(100, (50, 50, 0))

    def restart(self):
        self.total_frames = 0
        self.total_frames_played = 0
        self.started_time = time.time()
        self.current_time = time.time()
        self.elapsed_time = 0
        self.cube = Cube(100, (50, 50, 0))
                
    def update(self):
        self.total_frames += 1

        if (not self.paused or self.paused_manual_frame_tick):
            self.total_frames_played += 1

        self.current_time = time.time()
        self.elapsed_time = self.current_time - self.started_time

        
    def get_FPS(self):
        return format(self.total_frames / max(1, self.elapsed_time), '.2f')

    def draw(self):
        red = (255,0,0)
        font = self.generic_font
        screen = self.screen

        if self.paused:
            paused = font.render('Paused', False, red)
            screen.blit(paused, (self.screen_width // 2  - paused.get_width()  // 2,
                                 self.screen_height // 2 - paused.get_height() // 2))        
        
        FPS = font.render('FPS: ' + str(self.get_FPS()), False, red)
        screen.blit(FPS, (self.screen_width - FPS.get_width(), 0))
 
        time = font.render('Time: ' + str(self.total_frames_played), False, red)
        screen.blit(time, (self.screen_width - time.get_width(), font.get_height()))

class Point:
    def __init__(self, p):
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]

class Line:
    #Defined by two 3-tuples of coordinates
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class WireFrame:
    def __init__(self):
        self.points = []
        self.lines  = []

    def add_points(self, point_list):
        for point in point_list:
            p = Point(point)
            self.points.append(p)
    
    def add_lines(self, point_index_list):
        for (p1_i, p2_i) in point_index_list:
            self.lines.append( Line(self.points[p1_i], self.points[p2_i]) )

    def print(self):
        print(self.points)
        print(self.lines)

class Cube(WireFrame):
    def __init__(self, size, origin):
        WireFrame.__init__(self)
        self.add_points( [(x,y,z) for x in (origin[0], origin[0] + size) 
                                  for y in (origin[1], origin[1] + size) 
                                  for z in (origin[2], origin[2] + size)] )

        self.add_lines( [(0,1), (0,2), (0,4), (1,3), (1,5), (2,3), (2,6), 
                         (3,7), (4,5), (4,6), (5,7), (6,7)] )

    def find_center(self):
        num_points = len(self.points)
        x_mean = sum([p.x for p in self.points]) / num_points
        y_mean = sum([p.y for p in self.points]) / num_points
        z_mean = sum([p.z for p in self.points]) / num_points
        return (x_mean, y_mean, z_mean)

    def update(self, rot_theta):
        self.rotate_x(rot_theta)
        self.rotate_y(rot_theta)
        self.rotate_z(rot_theta)
    
    def rotate_x(self, rot_theta):    
        center = self.find_center()
        for p in self.points:
            #Convert to polar coordinates
            d     = math.hypot( p.y - center[1], p.z - center[2])
            theta = math.atan2( p.y - center[1], p.z - center[2]) + rot_theta
            #Convert back to cartesian coordinates
            p.z = center[2] + d * math.cos(theta)
            p.y = center[1] + d * math.sin(theta)
            
    def rotate_y(self, rot_theta):    
        center = self.find_center()
        for p in self.points:
            #Convert to polar coordinates
            d     = math.hypot( p.x - center[0], p.z - center[2])
            theta = math.atan2( p.x - center[0], p.z - center[2]) + rot_theta
            #Convert back to cartesian coordinates
            p.z = center[2] + d * math.cos(theta)
            p.x = center[0] + d * math.sin(theta)

    def rotate_z(self, rot_theta):    
        center = self.find_center()
        for p in self.points:
            #Convert to polar coordinates
            d     = math.hypot( p.y - center[1], p.x - center[0])
            theta = math.atan2( p.y - center[1], p.x - center[0]) + rot_theta
            #Convert back to cartesian coordinates
            p.x = center[0] + d * math.cos(theta)
            p.y = center[1] + d * math.sin(theta)
   
    def draw(self, engine):
        screen = engine.screen

        point_color = (136,  99, 191)
        point_radius = 4
        line_color  = ( 22,  34,  51)
        line_width = 3

        for line in self.lines:
            pygame.draw.line(screen, line_color, 
                             (line.p1.x, line.p1.y), 
                             (line.p2.x, line.p2.y), 
                             line_width)

        for point in self.points:
            pygame.draw.circle(screen, point_color, (round(point.x), round(point.y)), point_radius)

        center = self.find_center()
        pygame.draw.circle(screen, point_color, (round(center[0]), round(center[1])), point_radius)
 

if __name__ == '__main__':
    main()
