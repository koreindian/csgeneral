#import mahou
import sys
import pygame

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 720

NUMBERS_SPECIAL_KEYS = { 
    pygame.K_TAB         : '\t',
    pygame.K_SPACE       : ' ' ,
    pygame.K_EXCLAIM     : '!' ,
    pygame.K_QUOTEDBL    : '"' ,
    pygame.K_HASH        : '#' ,
    pygame.K_DOLLAR      : '$' ,
    pygame.K_AMPERSAND   : '&' ,
    pygame.K_QUOTE       : ' ' ,
    pygame.K_LEFTPAREN   : '(' ,
    pygame.K_RIGHTPAREN  : ')' ,
    pygame.K_ASTERISK    : '*' ,
    pygame.K_PLUS        : '+' ,
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
    pygame.K_COLON       : ':' ,
    pygame.K_SEMICOLON   : ';' ,
    pygame.K_LESS        : '<' ,
    pygame.K_EQUALS      : '=' ,
    pygame.K_GREATER     : '>' ,
    pygame.K_QUESTION    : '?' ,
    pygame.K_AT          : '@' ,
    pygame.K_LEFTBRACKET : '[' ,
    pygame.K_BACKSLASH   : '\\',
    pygame.K_RIGHTBRACKET: ']' ,
    pygame.K_CARET       : '^' ,
    pygame.K_UNDERSCORE  : '_' ,
    pygame.K_BACKQUOTE   : '`' , 
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
#    def __init__(height=(mahou.SCREEN_HEIGHT // 2), width=mahou.SCREEN_WIDTH):
    def __init__(self, height=(SCREEN_HEIGHT // 2), width=SCREEN_WIDTH):
#    def __init__(self, height=400, width=720):
        self.height = height
        self.width = width

        self.open = False # If we are in console mode
        self.displayed_height = 0
        self.display_speed = 60 

        self.history = []
        self.history_index = -1
        self.current_command = ''
        self.current_command_cursor = 0

        self.caps_on = False
        self.console_font = pygame.font.SysFont('Courier', 16)
        self.prompt_text = ">>>"
        self.cursor_char = "|"
        self.cursor_blink_cycle = 60
        self.cursor_blink_timer = 0   
 
    def update(self):
        if self.open and self.displayed_height < self.height:
            self.displayed_height = min (self.height, self.displayed_height + self.display_speed)
        if not self.open and self.displayed_height > 0:
            self.displayed_height = max (0, self.displayed_height - self.display_speed)
        
        self.cursor_blink_timer = (self.cursor_blink_timer + 1) % self.cursor_blink_cycle

    def draw(self, surface):
        if self.displayed_height > 0:
            blue = 0, 0, 255
            
            #Main Console Display
            console_rect = pygame.Surface((self.width, self.displayed_height))
            console_rect.set_alpha(128)
            console_rect.fill(blue)
            surface.blit(console_rect, (0,0))

            #Command line 
            cline_rect = pygame.Surface((self.width, 20))
            cline_rect.set_alpha(200)
            cline_rect.fill(blue)
            
            cursor_char_blinking = self.cursor_char if self.cursor_blink_timer < self.cursor_blink_cycle // 2 else ''
            command_text = self.current_command[:self.current_command_cursor] + \
                           cursor_char_blinking + \
                           self.current_command[self.current_command_cursor:]
            command_text = self.prompt_text + command_text
            current_command_text_surface = self.console_font.render(command_text, False, (255,255,255))

            surface.blit(cline_rect, (0,self.displayed_height))
            surface.blit(current_command_text_surface , (0, self.displayed_height))

            
 
    def current_command_insert_char_at_index(self, c):
        self.current_command = self.current_command[:self.current_command_cursor] + c + \
                               self.current_command[self.current_command_cursor:]
        self.current_command_cursor += 1


    def current_command_remove_char_at_index(self):
        if self.current_command_cursor > 0:
            self.current_command = self.current_command[:self.current_command_cursor-1] + \
                                   self.current_command[self.current_command_cursor:]
            self.current_command_cursor = max(0, self.current_command_cursor -1)

def main():
    pygame.init()
    console = Console()
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)

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
                        console.current_command_remove_char_at_index()
                    if event.key == pygame.K_RETURN:
                        console.history.append(console.current_command)
                        #TODO: run command
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
                     
#K_RIGHT               right arrow
#K_LEFT                left arrow

        print(console.history, console.current_command, console.current_command_cursor)
        console.update()
 
        screen.fill((0,0,0))
        console.draw(screen)
        pygame.display.flip()
        
if __name__ == "__main__":
    main()

