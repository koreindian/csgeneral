#import mahou
import sys, math, time, io
import pygame
import mahou_utils
import mahou

NUMBERS_SPECIAL_KEYS = { 
    pygame.K_TAB         : '\t',
    pygame.K_SPACE       : ' ' ,
    pygame.K_QUOTE       : '\'' ,
    pygame.K_COMMA       : ',' ,
    pygame.K_MINUS       : '-' ,
    pygame.K_PERIOD      : '.' ,
    pygame.K_SLASH       : '/' ,
    pygame.K_0           : '0' ,
    pygame.K_1           : '1' ,
    pygame.K_2           : '2' ,
    pygame.K_3           : '3' ,
    pygame.K_4           : '4' ,
    pygame.K_5           : '5' ,
    pygame.K_6           : '6' ,
    pygame.K_7           : '7' ,
    pygame.K_8           : '8' ,
    pygame.K_9           : '9' ,
    pygame.K_SEMICOLON   : ';' ,
    pygame.K_EQUALS      : '=' ,
    pygame.K_QUESTION    : '?' ,
    pygame.K_LEFTBRACKET : '[' ,
    pygame.K_BACKSLASH   : '\\',
    pygame.K_RIGHTBRACKET: ']' ,
    pygame.K_BACKQUOTE   : '`' , 
}

NUMBERS_SPECIAL_KEYS_SHIFTED = { 
    pygame.K_1  : '!' ,
    pygame.K_2  : '@' ,
    pygame.K_3  : '#' ,
    pygame.K_4  : '$' ,
    pygame.K_5  : '%' ,
    pygame.K_6  : '^' ,
    pygame.K_7  : '&' ,
    pygame.K_8  : '*' ,
    pygame.K_9  : '(' ,
    pygame.K_0  : ')' ,
    pygame.K_MINUS  : '_' ,
    pygame.K_EQUALS : '+' ,
    pygame.K_LEFTBRACKET : '{' ,
    pygame.K_RIGHTBRACKET: '}' ,
    pygame.K_SEMICOLON   : ':' ,
    pygame.K_QUOTE       : '\"' ,
    pygame.K_COMMA       : '<' ,
    pygame.K_PERIOD      : '>' ,
    pygame.K_SLASH       : '?' ,
    pygame.K_BACKSLASH   : '|',
}

ALPHABET = {
    pygame.K_a  : 'a',
    pygame.K_b  : 'b',
    pygame.K_c  : 'c',
    pygame.K_d  : 'd',
    pygame.K_e  : 'e',
    pygame.K_f  : 'f',
    pygame.K_g  : 'g',
    pygame.K_h  : 'h',
    pygame.K_i  : 'i',
    pygame.K_j  : 'j',
    pygame.K_k  : 'k',
    pygame.K_l  : 'l',
    pygame.K_m  : 'm',
    pygame.K_n  : 'n',
    pygame.K_o  : 'o',
    pygame.K_p  : 'p',
    pygame.K_q  : 'q',
    pygame.K_r  : 'r',
    pygame.K_s  : 's',
    pygame.K_t  : 't',
    pygame.K_u  : 'u',
    pygame.K_v  : 'v',
    pygame.K_w  : 'w',
    pygame.K_x  : 'x',
    pygame.K_y  : 'y',
    pygame.K_z  : 'z', 
}


class Console():
    def __init__(self, game_engine):
        self.height = game_engine.screen_height // 2
        self.width = game_engine.screen_width

        self.text_line_height = 20

        self.open = False # If we are in console mode
        self.displayed_height = 0
        self.display_speed = 60 

        self.history = [] #list of strings of all commands written in the command line
        self.history_index = -1
        self.current_command = ''
        self.current_command_cursor = 0

        self.stdout_history = [] #list of command output.

        #Alters event.key -> character mapping. 
        #Acts like shift-lock rather than caps-lock. Consider fixing. 
        self.caps_on = False 

        self.console_font_size = 16
        self.console_font_color = (102, 139, 139) #PaleTurquoise4
        self.console_font = pygame.font.SysFont('Consolas', self.console_font_size)
        self.prompt_text = ">>>"

        self.cursor_char = "|"
        self.cursor_color = (0, 168, 63) #SeaGreen
        self.cursor_blink_cycle = 60 #Number of frames for cursor to alternate displaying/not displaying
        self.cursor_blink_timer = 0 #Counter variable to time the blink cycle

        self.backspace_depressed = False
        self.backspace_depressed_timer = 0
        self.backspace_repeated_deletion_latency = 30 #Number of frames before repeat deletion starts
        self.backspace_repeated_deletion_speed = 3 #Number of frames each deletion in a repeat deletion takes
 
    def update(self):
        if self.open and self.displayed_height < self.height:
            self.displayed_height = min (self.height, self.displayed_height + self.display_speed)
        if not self.open and self.displayed_height > 0:
            self.displayed_height = max (0, self.displayed_height - self.display_speed)
        
        self.cursor_blink_timer = (self.cursor_blink_timer + 1) % self.cursor_blink_cycle

        #For backspaces, initial input is handled during the reading of key events,
        # but repeated deletions are handled in the update function
        if self.backspace_depressed:
            if self.backspace_depressed_timer >= self.backspace_repeated_deletion_latency and \
               self.backspace_depressed_timer % self.backspace_repeated_deletion_speed == 0:
                    self.current_command_remove_char_at_index()
            self.backspace_depressed_timer += 1 

    def draw(self, surface):
        if self.displayed_height > 0:
            blue = 0, 0, 255
            
            #Main Console Display
            console_rect = pygame.Surface((self.width, self.displayed_height))
            console_rect.set_alpha(128)
            console_rect.fill(blue)
            surface.blit(console_rect, (0,0))

            #Command line 
            cline_rect = pygame.Surface((self.width, self.text_line_height))
            cline_rect.set_alpha(200)
            cline_rect.fill(blue)
            
            command_text = self.prompt_text + self.current_command
            current_command_text_surface = self.console_font.render( \
                                               command_text, \
                                               False, \
                                               self.console_font_color)
            
            cursor_width = self.console_font.size('a')[0]
            cursor_height = self.console_font.get_height()
            cursor_rect = pygame.Surface((cursor_width, cursor_height))
            cursor_rect.set_alpha(200)
            cursor_rect.fill(self.get_cursor_color())

            #Blit to surface
            surface.blit(cline_rect, (0,self.displayed_height))
            surface.blit(current_command_text_surface , (0, self.displayed_height))
            surface.blit(cursor_rect, (cursor_width * (self.current_command_cursor + len(self.prompt_text)), \
                                       self.displayed_height))

            #Draw stdout history, but only if console is fully drawn
            if self.displayed_height == self.height:
                lines_blitted = 0
                chars_per_line = self.width // cursor_width
                for i in range(len(self.stdout_history))[::-1]:
                    hist_output = self.stdout_history[i]
                    #Split by newlines
                    hist_lines = hist_output.rstrip('\n').split('\n')
                    
                    for l in hist_lines:
                        #Split line into console_width sized surfaces
                        line_split = [ l[j:j+chars_per_line] for j in range(0, len(l), \
                                                                               chars_per_line) ]
                        for line in line_split[::-1]:
                            text_surface = self.console_font.render(line, False, self.console_font_color)
                            text_height = self.height - self.text_line_height *\
                                                        (1 + lines_blitted)
                            surface.blit(text_surface, (0,text_height))
                            lines_blitted +=1  
              
    def get_cursor_color(self):
            t = (math.cos(time.time() * 2)) ** 2
            return mahou_utils.color_lerp((255,255,255), self.cursor_color, t)
         
    def current_command_insert_char_at_index(self, c):
        self.current_command = self.current_command[:self.current_command_cursor] + c + \
                               self.current_command[self.current_command_cursor:]
        self.current_command_cursor += 1


    def current_command_remove_char_at_index(self):
        if self.current_command_cursor > 0:
            self.current_command = self.current_command[:self.current_command_cursor-1] + \
                                   self.current_command[self.current_command_cursor:]
            self.current_command_cursor = max(0, self.current_command_cursor -1)

    def process_event(self, event, game_engine, entity_mgr):
        if not self.open:   #Redundent...
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKQUOTE:
                    self.open = not self.open
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.open = not self.open
                if event.key == pygame.K_BACKSPACE:
                    self.backspace_depressed = True
                    self.current_command_remove_char_at_index()
                if event.key == pygame.K_RETURN:
                    self.history.append(self.current_command)
                    self.run_command(self.current_command, game_engine, entity_mgr)
                    self.current_command = ''
                    self.history_index = -1
                    self.current_command_cursor = 0
                if event.key == pygame.K_UP:
                    if len(self.history) > 0:
                        if self.history_index == -1:
                            self.history_index = len(self.history) - 1
                        elif self.history_index > 0:
                            self.history_index -= 1
                        self.current_command = self.history[self.history_index]
                        self.current_command_cursor = len(self.current_command)
                if event.key == pygame.K_DOWN:
                    if self.history_index != -1 and self.history_index < len(self.history) - 1:
                        self.history_index += 1
                        self.current_command = self.history[self.history_index]
                        self.current_command_cursor = len(self.current_command)
                    else:
                        self.history_index = -1
                        self.current_command = ''
                        self.current_command_cursor = 0
                if event.key in ALPHABET:
                    if self.caps_on:
                        self.current_command_insert_char_at_index(ALPHABET[event.key].upper())
                    else:   
                        self.current_command_insert_char_at_index(ALPHABET[event.key])
                if event.key in NUMBERS_SPECIAL_KEYS:
                        if self.caps_on:
                            self.current_command_insert_char_at_index( \
                                        NUMBERS_SPECIAL_KEYS_SHIFTED[event.key])
                        else:
                            self.current_command_insert_char_at_index(NUMBERS_SPECIAL_KEYS[event.key])
                if event.key == pygame.K_CAPSLOCK or \
                   event.key == pygame.K_RSHIFT or \
                   event.key == pygame.K_LSHIFT:
                        self.caps_on = not self.caps_on
                if event.key == pygame.K_LEFT:
                    self.current_command_cursor = max(0, self.current_command_cursor - 1)
                if event.key == pygame.K_RIGHT:
                    self.current_command_cursor = min(len(self.current_command), \
                                                         self.current_command_cursor + 1)
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_CAPSLOCK or \
                       event.key == pygame.K_RSHIFT or \
                       event.key == pygame.K_LSHIFT:
                        self.caps_on = not self.caps_on
                    if event.key == pygame.K_BACKSPACE:
                       self.backspace_depressed = False
                       self.backspace_depressed_timer = 0


    def run_command(self, s, game_engine, entity_mgr):
        #Parse args
        s_parsed = s.split()
        cmd = s_parsed[0]
        if cmd == 'echo':
            output = ''
            for arg in s_parsed[1:]:
                output += arg
                output += ' '
            output = output[:-1]
            self.stdout_history.append(output)
        elif cmd == 'pause':
            game_engine.paused = True
        elif cmd == 'unpause':
            game_engine.paused = False
        elif cmd == 'quit':
            sys.exit()
        elif cmd == 'hitbox':
            entity_mgr.display_hitboxes = not entity_mgr.display_hitboxes
        elif cmd == 'godmode':
            entity_mgr.player_ship.health = 100000
        elif cmd == 'exec':
            try:
                executed_cmd = s[5:]
                
                console_out = io.StringIO()
                sys.stdout = console_out
                exec(executed_cmd)
                sys.stdout = sys.__stdout__
                
                output = console_out.getvalue()
        
                for c in output:
                    print(ord(c))
                self.stdout_history.append(output)
                console_out.close()
            except:
                output = "ERROR -" + s +": "
                output += str(sys.exc_info()[0])
                output += str(sys.exc_info()[1])
                output += str(sys.exc_info()[2])
                self.stdout_history.append(output)
        else:
            output = "Invalid command: " + s_parsed[0]
            self.stdout_history.append(output)
            

def main():
    pygame.init()
    console = Console()
    screen = pygame.display.set_mode((console.width, 2 * console.screen_height))

    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if not console.open:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKQUOTE:
                        console.open = not console.open
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        console.open = not console.open
                    if event.key == pygame.K_BACKSPACE:
                        console.backspace_depressed = True
                        console.current_command_remove_char_at_index()
                    if event.key == pygame.K_RETURN:
                        console.history.append(console.current_command)
                        console.run_command(console.current_command)
                        console.current_command = ''
                        console.history_index = -1
                        console.current_command_cursor = 0
                    if event.key == pygame.K_UP:
                        if len(console.history) > 0:
                            if console.history_index == -1:
                                console.history_index = len(console.history) - 1
                            elif console.history_index > 0:
                                console.history_index -= 1
                            console.current_command = console.history[console.history_index]
                            console.current_command_cursor = len(console.current_command)
                    if event.key == pygame.K_DOWN:
                        if console.history_index != -1 and console.history_index < len(console.history) - 1:
                            console.history_index += 1
                            console.current_command = console.history[console.history_index]
                            console.current_command_cursor = len(console.current_command)
                        else:
                            console.history_index = -1
                            console.current_command = ''
                            console.current_command_cursor = 0
                    if event.key in ALPHABET:
                        if console.caps_on:
                            console.current_command_insert_char_at_index(ALPHABET[event.key].upper())
                        else:   
                            console.current_command_insert_char_at_index(ALPHABET[event.key])
                    if event.key in NUMBERS_SPECIAL_KEYS:
                            if console.caps_on:
                                console.current_command_insert_char_at_index( \
                                            NUMBERS_SPECIAL_KEYS_SHIFTED[event.key])
                            else:
                                console.current_command_insert_char_at_index(NUMBERS_SPECIAL_KEYS[event.key])
                    if event.key == pygame.K_CAPSLOCK or \
                       event.key == pygame.K_RSHIFT or \
                       event.key == pygame.K_LSHIFT:
                            console.caps_on = not console.caps_on
                    if event.key == pygame.K_LEFT:
                        console.current_command_cursor = max(0, console.current_command_cursor - 1)
                    if event.key == pygame.K_RIGHT:
                        console.current_command_cursor = min(len(console.current_command), \
                                                             console.current_command_cursor + 1)
                if event.type == pygame.KEYUP:
                        if event.key == pygame.K_CAPSLOCK or \
                           event.key == pygame.K_RSHIFT or \
                           event.key == pygame.K_LSHIFT:
                            console.caps_on = not console.caps_on
                        if event.key == pygame.K_BACKSPACE:
                           console.backspace_depressed = False
                           console.backspace_depressed_timer = 0

                     
        #print(console.history, console.current_command, console.current_command_cursor)
        console.update()
 
        screen.fill((0,0,0))
        console.draw(screen)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()

