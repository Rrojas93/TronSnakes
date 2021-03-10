#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    GAME_snake.py
    Author: Raul Rojas
    Contact: rrojas994@gmail.com
    Description:
        The game of snake. Pretty much just as simple as you can get.
'''
import os, sys, time, random, platform
# You can run this headleass if imported as a module. 
# The calling script will handle drawing everything to the screen
# Can be used to train agents in TensorFlow maybe?
run_headless = True if __name__ != "__main__" else False 
screen_size = (800,480)
play_area_size = (min(screen_size), min(screen_size))
if(not(run_headless)):
    import pygame
    pygame.init()
    flags = pygame.FULLSCREEN if platform.system().lower() == 'linux' else 0
    screen = pygame.display.set_mode(size=screen_size, flags=flags)
    background_color = (60, 60, 60)
    screen.fill(background_color)
    play_area = pygame.surface.Surface(play_area_size)
    # screen.blit(play_area, (0,0))
    clock = pygame.time.Clock()

def main():
    """
    Running the main game loop and renders the game using pygame module.
    """
    game_env = Environment(play_area_size, 10, True)
    game_env.game_state = GameState(GameState.SETUP)
    left_text_area = TextArea(
        0, 
        0, 
        int((screen_size[0]-play_area_size[0])/2),
        screen_size[1], 
        screen
    )
    right_text_area = TextArea(
        int(screen_size[0]/2)+int(play_area_size[0]/2), 
        0, 
        int((screen_size[0]-play_area_size[0])/2), 
        screen_size[1], 
        screen
    )
    refresh_delay = 0.04
    last_refresh = 0
    tic_rate = 60
    p1_next_move = None
    p2_next_move = None
    input_interface = KeyboardInput()
    while True:
        # LOOP SETUP
        left_text_area.reset()
        right_text_area.reset()

        # === STATE: CLOSE
        if(game_env.game_state == GameState.CLOSE):
            break

        # === STATE: SETUP
        if(game_env.game_state == GameState.SETUP):
            screen.fill(background_color)
            play_area.fill(Colors.BLACK)
            game_env.restart()
            p1_next_move = None
            p2_next_move = None
            last_refresh = 0

        # === STATE: GAMEOVER
        if(game_env.game_state == GameState.GAMEOVER):
            game_env.game_state.set(GameState.SETUP)
            game_env.round += 1
            if(game_env.round > 3):
                game_env.game_state.set(GameState.WIN)
            continue

        # === STATE: PLAY
        if(game_env.game_state == GameState.PLAY):
            input_interface.prepare()
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    game_env.game_state.set(GameState.CLOSE)
                    break
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_ESCAPE):
                        game_env.game_state.set(GameState.CLOSE)
                        break
                p1_input = input_interface.scan_p1_movement(event)
                p2_input = input_interface.scan_p2_movement(event)
                if(p1_input):
                    p1_next_move = p1_input
                if(p2_input):
                    p2_next_move = p2_input
            if(time.time() > last_refresh+refresh_delay):
                if(p1_next_move is not None):
                    game_env.snakes[0].change_direction(p1_next_move)
                    p1_next_move = None
                if(game_env.two_players):
                    if(p2_next_move is not None):
                        game_env.snakes[1].change_direction(p2_next_move)
                        p2_next_move = None
                game_env.update()
                last_refresh = time.time()

        # === STATE: WIN
        if(game_env.game_state == GameState.WIN):
            if(game_env.two_players):
                if(game_env.p1_score > game_env.p2_score):
                    game_env.snakes[0].draw(Colors.GREEN)
                    game_env.snakes[1].draw(Colors.GRAY)
                else:
                    game_env.snakes[0].draw(Colors.GRAY)
                    game_env.snakes[1].draw(Colors.GREEN)
            else:
                game_env.snakes[0].draw(Colors.GREEN)
            p1_option_input = None
            p2_option_input = None
            for event in pygame.event.get():
                if(p1_option_input is None):
                    p1_option_input = input_interface.scan_p1_options(event)
                if(p2_option_input is None):
                    p2_option_input = input_interface.scan_p2_options(event)
            options = [p1_option_input, p2_option_input]
            if(InputInterface.ACTION_CONFIRM in options):
                game_env.round = 0
                game_env.p1_score = 0
                game_env.p2_score = 0
                game_env.game_state.set(GameState.SETUP)

        # === STATE: ANY/ALL
        screen.blit(play_area, (int(screen_size[0]/2)-int(play_area_size[0]/2),0))
        if(game_env.two_players):
            update_text_two_player(left_text_area, game_env.snakes[0], game_env)
            update_text_two_player(right_text_area, game_env.snakes[1], game_env)
        else:
            update_text_single_player(left_text_area, right_text_area, game_env)
            
        left_text_area.draw()
        right_text_area.draw()
        pygame.display.update()
        clock.tick(tic_rate)
    
def update_text_single_player(left_area, right_area, game_env):
    '''
    Updates the text areas for one player scenarios.
    '''
    pass

def update_text_two_player(text_area_obj, snake_obj, game_env):
    '''
    Updates the text areas for two player scenarious.
    '''
    # Add title text
    text_area_obj.set_cursor(10, 0)
    text_area_obj.print_text(f'Player {"1" if snake_obj.player_one else "2"}', color=snake_obj.color, size=45)

    # Add score label
    text_area_obj.new_line(number_of_lines=2)
    text_area_obj.set_cursor(30, text_area_obj.cursor_y)
    text_area_obj.print_text(f'Score', size=40, color=snake_obj.color)

    # Add score
    text_area_obj.new_line()
    text_area_obj.set_cursor(55, text_area_obj.cursor_y)
    text_area_obj.print_text(f'{game_env.p1_score if snake_obj.player_one else game_env.p2_score}', size=60, color=snake_obj.color)

    # Add round label
    text_area_obj.new_line()
    text_area_obj.set_cursor(25, text_area_obj.cursor_y)
    text_area_obj.print_text(f'Round', size=40)

    # Add round
    text_area_obj.new_line()
    if(game_env.round <= 3):
        text_area_obj.set_cursor(55, text_area_obj.cursor_y)
        text_area_obj.print_text(f'{game_env.round}', size=60)
    else:
        text_area_obj.set_cursor(30, text_area_obj.cursor_y)
        text_area_obj.print_text("GAME\n\nOVER", size=40)
    
class InputInterface():
    # informal interface. Mostly just here to demonstrate what the intentional 
    #   use is.
    ACTION_CONFIRM = 'CONFIRM'
    ACTION_PAUSE = 'PAUSE'
    ACTION_RETURN = 'RETURN'
    ACTION_EXIT = 'EXIT'
    ACTION_UP = 'UP'
    ACTION_DOWN = 'DOWN'
    ACTION_LEFT = 'LEFT'
    ACTION_RIGHT = 'RIGHT'
    def prepare(self):
        '''
        This acts as preparation function which is called right before inputs are 
        scanned from pygame module. This is to allow for reinitialization of some interfaces
        like gamepads which could potentially become disconnected. 
        '''
        pass

    def scan_p1_movement(self, pygame_event):
        '''
        Override this funtion to define your movement scanning function for player 1. 
        No input from p1 should return None. This function must return any of the 
        following vectors:
        Vector.up()
        Vector.down()
        Vector.left()
        Vector.right()
        '''
        pass

    def scan_p1_options(self, pygame_event):
        '''
        Override this function to define your scanning function for player 1 
        option inputs. This is any input that can be returned for things like 
        pause, accept, back, etc.
        '''
        pass

    def scan_p2_movement(self, pygame_event):
        '''
        Override this function to define your movement scanning function for player 2.
        No input from p2 should return None. This function must return any of the 
        following vectors:
        Vector.up()
        Vector.down()
        Vector.left()
        Vector.right()
        '''
        pass

    def scan_p2_options(self, pygame_event):
        '''
        Override this function to define your scanning function for player 2 
        option inputs. This is any input that can be returned for things like 
        pause, accept, back, etc.
        '''
        

class KeyboardInput(InputInterface):
    def scan_p2_movement(self, pygame_event):
        if(pygame_event.type == pygame.KEYDOWN):
            if(pygame_event.key == pygame.K_UP):
                return Vector.up()
            elif(pygame_event.key == pygame.K_DOWN):
                return Vector.down()
            elif(pygame_event.key == pygame.K_LEFT):
                return Vector.left()
            elif(pygame_event.key == pygame.K_RIGHT):
                return Vector.right()
        return None
    def scan_p1_movement(self, pygame_event):
        if(pygame_event.type == pygame.KEYDOWN):
            if(pygame_event.key == pygame.K_w):
                return Vector.up()
            elif(pygame_event.key == pygame.K_s):
                return Vector.down()
            elif(pygame_event.key == pygame.K_a):
                return Vector.left()
            elif(pygame_event.key == pygame.K_d):
                return Vector.right()
        return None

    def scan_p1_options(self, pygame_event):
        if(pygame_event.type == pygame.KEYDOWN):
            if(pygame_event.key == pygame.K_SPACE):
                return self.ACTION_CONFIRM
            if(pygame_event.key == pygame.K_p):
                return self.ACTION_PAUSE
            if(pygame_event.key == pygame.K_BACKSPACE):
                return self.ACTION_RETURN
            if(pygame_event.key == pygame.K_ESCAPE):
                return self.ACTION_EXIT
            if(pygame_event.key in [pygame.K_w, pygame.K_UP]):
                return self.ACTION_UP
            if(pygame_event.key in [pygame.K_a, pygame.K_LEFT]):
                return self.ACTION_LEFT
            if(pygame_event.key in [pygame.K_s, pygame.K_DOWN]):
                return self.ACTION_DOWN
            if(pygame_event.key in [pygame.K_d, pygame.K_RIGHT]):
                return self.ACTION_RIGHT
        return None

    def scan_p2_options(self, pygame_event):
        return self.scan_p1_options(pygame_event)

class GamePadInput(InputInterface):
    def __init__(self, joystick_threshold=0.4):
        """
        Provides an interface for a gamepad as an input. 

        :param joystick_threshold: Joystick values range from -1 to 1. The threshold 
        represents the value in which the absolute value of the reading will be accepted. 
        This is to help with joystick drift and jitters from input.
        """
        self.joystick_threshold = joystick_threshold
        pygame.joystick.init()
        self.joysticks = list()

    def _get_joystics(self):
        self.joysticks = list()
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
            self.joysticks[i].init()
            # print(f'Added Gamepad: {self.joysticks[i].get_guid()}')
            # print (f'Game pad {i} initialized: ' + str(self.joysticks[i].get_init()))

    def _scan_joystick_movement(self, index):
        '''
        Provides an internal helper function for cleaner and less redundent 
        p1 & p2 scanning functions.
        '''
        if(len(self.joysticks)<index+1):
            # index will be out of range and cause exception.
            return None
        for i in range(self.joysticks[index].get_numhats()):
            hat_val = self.joysticks[index].get_hat(i)
            if(hat_val[0] or hat_val[1]):
                print(f'Hat: {i}, Value: {self.joysticks[index].get_hat(i)}')
                return Vector(hat_val[0], hat_val[1]*-1)
        
        x = None
        y = None
        # no input on hats so check joysticks
        for i in range(self.joysticks[index].get_numaxes()):
            if(i==0): # left joystick x axis
                x = self.joysticks[index].get_axis(i)
            if(i==1): # left joystick y axis
                y = self.joysticks[index].get_axis(i)
        if (x and y):
            if(abs(x) > abs(y) and abs(x) > self.joystick_threshold):
                return Vector.left() if x < 0 else Vector.right()
            elif(abs(y) > abs(x) and abs(y) > self.joystick_threshold):
                return Vector.up() if y < 0 else Vector.down()
        
        return None

    def _scan_joystick_options(self, index, game_event):
        '''
        Returns the input from the joystick for option type actions.
        '''
        if(len(self.joysticks)<index+1):
            # index will be out of range and cause exception.
            return None
        joystick = self.joysticks[index]
        if(game_event.type == pygame.JOYBUTTONDOWN):
            if(joystick.get_button(0)):
                return self.ACTION_CONFIRM
            if(joystick.get_button(1)):
                return self.ACTION_RETURN
            if(joystick.get_button(7)):
                return self.ACTION_PAUSE
            movement_keys = self._scan_joystick_movement(index)
            if(movement_keys == Vector.up()):
                return self.ACTION_UP
            if(movement_keys == Vector.down()):
                return self.ACTION_DOWN
            if(movement_keys == Vector.left()):
                return self.ACTION_LEFT
            if(movement_keys == Vector.right()):
                return self.ACTION_RIGHT
        return None

    def scan_p1_movement(self, pygame_event):
        return self._scan_joystick_movement(0)

    def scan_p2_movement(self, pygame_event):
        return self._scan_joystick_movement(1)

    def scan_p1_options(self, pygame_event):
        return self._scan_joystick_options(0, pygame_event)

    def scan_p2_options(self, pygame_event):
        return self._scan_joystick_options(1, pygame_event)

    def prepare(self):
        '''
        Runs prior to checking for input from the gamepads.
        '''
        self._get_joystics()

class GameState():
    CLOSE = 'CLOSE'
    SETUP = 'SETUP'
    PLAY = 'PLAY'
    GAMEOVER = 'GAMEOVER'
    WIN = 'WIN'
    PAUSE = 'PAUSE'
    NONESTATE = 'NONESTATE'
    def __init__(self, state='SETUP'):
        self.state = state

    def __eq__(self, other):
        if(isinstance(other, GameState)):
            return self.state == other.state
        elif(isinstance(other, str)): # to compare with other instances or native types
            return self.state == other
        
    def set(self, new_state):
        self.state = new_state

class Colors():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    TRON_RED = (255, 100, 0)
    TRON_BLUE = (87, 227, 255)
    GRAY = (60, 60, 60)
    def __init__(self):
        pass

class TextArea():
    def __init__(
        self, 
        loc_x, 
        loc_y, 
        width, 
        height, 
        target_surface, 
        margin_x=10, 
        margin_y=10, 
        font_size=20, 
        text_color=Colors.BLACK,
        background_color = Colors.WHITE,
        line_height=15
    ):
        '''
        Helps print out text to a surface.

        :param loc_x: The top left corner x coordinate of the text area.
        :param loc_y: The top left corner y coordinate of the text area.
        :param width: The horizontal size of the text area.
        :param height: The vertical size of the text area.
        :param target_surface: The surface to draw the text on.
        :param margin_x: Left and Right margins for the text area.
        :param margin_y: Top and Bottom margins for the text area.
        :param font_size: The size that the font should render at.
        :param text_color: The color of the text as an RGB tuple. (0-255)
        :param background_color: The color of the background as an RGB tuple. (0-255)
        :param line_height: The vertical distance between each line.
        '''
        self.x = loc_x
        self.y = loc_y
        self.width = width
        self.height = height
        self.surface = target_surface
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.font_size = font_size
        # self.font = pygame.font.Font(None, self.font_size)
        self.line_height = line_height
        self.text_color = text_color
        self.background_color = background_color
        self.cursor_x = 0
        self.cursor_y = 0
        self.reset()
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.clear()
    
    def reset(self):
        '''
        Resets the cursor to a default location.
        '''
        self.reset_cursor()
        self.clear()

    def print_text(self, text:str, size=None, color=None):
        '''
        Prints the input text to the surface at the current cursor location.
        '''
        if(size is None):
            size = self.font_size
        if(color is None):
            color = self.text_color
        text_lines = text.splitlines()
        starting_x = self.cursor_x
        for line in text_lines:
            font = pygame.font.Font(None, size)
            text_bit_map = font.render(line, True, color)
            self.surface.blit(text_bit_map, (self.cursor_x, self.cursor_y))
            self.new_line()
            self.cursor_x = starting_x

    def new_line(self, number_of_lines=1):
        '''
        Moves the cursor down by line_height and resets the cursors horizontal 
        position.
        '''
        self.cursor_y += self.line_height * number_of_lines
        self.reset_cursor_x()
    
    def reset_cursor(self):
        '''
        Resets the cursor position to the default starting location.
        '''
        self.set_cursor(0,0)

    def reset_cursor_x(self):
        '''
        Resets the cursor position on the x axis to the left most location of 
        the text area.
        '''
        self.cursor_x = self.margin_x

    def set_cursor(self, x, y):
        '''
        Sets the cursor location relative to the text area.
        '''
        self.cursor_x = self.margin_x + x
        self.cursor_y = self.margin_y + self.line_height + y

    def clear(self):
        '''
        Clears the text area by filling with the background color.
        '''
        self.surface.fill(self.background_color)

    def draw(self):
        '''
        Draws the text area surface onto the screen surface.
        '''
        screen.blit(self.surface, (self.x, self.y))

class Vector():
    """
    Represents a direction. Vertical directions should be stored inverted to normal
    convention since positive screen growth happens downward.
    """
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if(isinstance(other, Vector)):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def opposite(self):
        """
        Returns the opposite direction vector as a new vector.
        """
        return Vector(-1*self.x, -1*self.y)
    
    @staticmethod
    def up():
        '''
        Returns an up vector
        '''
        return Vector(0,-1)
    
    @staticmethod
    def down():
        '''
        Returns a down vector
        '''
        return Vector(0,1)
    
    @staticmethod
    def left():
        '''
        Returns a left vector (-1,0)
        '''
        return Vector(-1,0)
    
    @staticmethod
    def right():
        '''
        Returns a right vector (1, 0)
        '''
        return Vector(1,0)

class Cell():
    """
    Represents a square block of the snake.

    """
    def __init__(
        self, 
        location_x:int,
        location_y:int,
        size:int,
        color=Colors.WHITE,
        parent_cell=None,
        child_cell = None, 
        parent_snake = None
    ):
        self.x = location_x
        self.y = location_y
        self.size = size
        if(not(run_headless)):
            self.rect = pygame.Rect(self.x*self.size, self.y*self.size, size, size)
        else:
            self.rect = None
        self.parent = parent_cell
        self.child = child_cell
        self.parent_snake = parent_snake
        self.draw(color)

    def __eq__(self, other):
        if(isinstance(other, Cell)):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def get_head(self):
        '''
        Returns the head of the cell chain.
        '''
        current_cell = self
        while(current_cell.parent is not None):
            current_cell = current_cell.parent
        return current_cell
    
    def get_tail(self):
        '''
        Returns the tail of the cell chain.
        '''
        current_cell = self
        while(current_cell.child is not None):
            current_cell = current_cell.child
        return current_cell

    def draw(self, color:tuple):
        '''
        Draws the cell on the screen as a rect.
        '''
        if(not(run_headless)):
            pygame.draw.rect(
                play_area,
                color,
                self.rect
            )
    
    def remove(self):
        '''
        Removes any references to parents and children as well as any references 
        to it. This should allow garbage collection to clean it up.
        '''
        if(self.parent):
            self.parent.child = None # Remove references to this cell at parent cell.
        if(self.child):
            self.child.parent = None # Remove references to this cell at child cell.
        self.parent = None
        self.child = None
        self.snake = None
        self.draw(Colors.BLACK)

class Snake():
    """
    Instantiates a snake object.

    :param init_location: Initial location of the first cell of the snake as a tuple (x,y).
    :param cell_size: Size of each cell. Cell is a square so cell width = height
    :param screen_size: Screen size for bounds.
    :param length: The length of the snake in in cells.
    :param direction: The direction that the snake is moving as a Vector object
    """
    def __init__(
        self,
        init_location_x:int,
        init_location_y:int,
        cell_size:int,
        environment,
        color=Colors.WHITE,
        length=3,
        direction=Vector.up(),
        player_one=True
    ):
        self.cell_size = cell_size
        self.env = environment
        self.color = color
        self.init_length = length
        self.length = length
        self.direction = direction
        self.player_one = player_one
        self.head = None
        self.tail = None
        self.__create(init_location_x, init_location_y)

    def __create(self, location_x:int, location_y:int):
        '''
        Creates the first few cells of the snake. The direction in which the cells
        are created are opposite to the direction that the snake is moving.

        :param location_x: x location of new head cell.
        :param location_y: y location of new head cell.
        '''
        current_cell = None
        for _ in range(self.length):
            if(self.head is None):
                self.head = Cell(location_x, location_y, self.cell_size, parent_snake=self, color=self.color)
                current_cell = self.head
                self.env.add_to_map(current_cell)
                continue
            current_cell.child = Cell(
                current_cell.x+self.direction.opposite().x,
                current_cell.y+self.direction.opposite().y,
                self.cell_size,
                parent_cell=current_cell,
                parent_snake=self,
                color=self.color
            )
            self.env.add_to_map(current_cell.child)
            current_cell = current_cell.child # set new child cell as current cell
        self.tail = current_cell

    def move(self)->bool:
        '''
        Moves the snake in the direction of movement. Return True if the move was
        successful (did not go out of bounds and did not collide with others.)
        '''
        new_loc_x = self.head.x + self.direction.x
        new_loc_y = self.head.y + self.direction.y
        
        if(self.env.is_out_of_bounds(new_loc_x, new_loc_y)):
            if(self.player_one):
                self.env.p1_score -= 1 if self.env.p1_score > 0 else 0
            else:
                self.env.p2_score -= 1 if self.env.p2_score > 0 else 0
            return False # snake dies, went out of bounds.
        else:
            location_contents = self.env.get_location_contents(new_loc_x, new_loc_y)
            if(location_contents is None): # if the location is empty.
                new_cell = Cell(
                    new_loc_x,
                    new_loc_y,
                    self.cell_size,
                    child_cell=self.head, 
                    parent_snake=self
                )
                self.add_to_head(new_cell)
                self.remove_tail()
                return True
            elif(location_contents.parent_snake is None):
                # it is food. eat it.
                self.add_to_head(location_contents, adjust_length=True)
                self.env.food = None
                if(self.color == Colors.TRON_RED):
                    self.env.p1_score += 1
                else:
                    self.env.p2_score += 1
                return True
            else:
                # the new location contains a cell that belongs to a snake. 
                if(self.player_one):
                    self.env.p1_score -= 1 if self.env.p1_score > 0 else 0
                else:
                    self.env.p2_score -= 1 if self.env.p2_score > 0 else 0
                return False # snake dies, collided with self or another snake.

    def change_direction(self, new_direction:Vector):
        '''
        Changes the direction of the snake and prevents it from moving backwards.
        '''
        if(new_direction == Vector.left() and self.direction != Vector.right()):
            self.direction = Vector.left()
        elif(new_direction == Vector.right() and self.direction != Vector.left()):
            self.direction = Vector.right()
        elif(new_direction == Vector.up() and self.direction != Vector.down()):
            self.direction = Vector.up()
        elif(new_direction == Vector.down() and self.direction != Vector.up()):
            self.direction = Vector.down()

    def add_to_head(self, new_cell:Cell, adjust_length=False):
        """
        Addes a new cell to the head of the snake. 

        :param new_cell: New cell to add as a head.
        """
        new_cell.child = self.head
        self.head.parent = new_cell
        self.head = new_cell
        self.head.draw(self.color)
        self.env.add_to_map(self.head)
        if(adjust_length):
            self.length += 1

    def remove_tail(self, adjust_length=False):
        new_tail = self.tail.parent
        self.tail.remove() # gets the last cell in the chain and removes it.
        self.env.remove_from_map(self.tail)
        self.tail = new_tail
        if(adjust_length):
            self.length -= 1
    
    def draw(self, color):
        '''
        Draws the snake with a different color.
        '''
        self.color = color
        current_cell = self.head
        while(current_cell is not None):
            current_cell.draw(color)
            current_cell = current_cell.child

class Environment():
    def __init__(self, resolution:tuple, cell_size:int, two_players:bool):
        self.resolution = resolution
        self.cell_size = cell_size
        # Calculate size of 2d map array
        self.size_x = int(resolution[0]/cell_size)
        self.size_y = int(resolution[1]/cell_size)
        self.two_players = two_players
        self.round = 0
        self.p1_score = 0
        self.p2_score = 0

        self._set_volatile_params()

    def restart(self):
        '''
        Creates a completely new environment with a new map and snake with all
        parameters reset to defaults.
        '''
        self._set_volatile_params()
        self._create_new_map()
        if(not(self.two_players)):
            self.snakes.append(Snake(
                int(self.size_x/2), 
                int(self.size_y/2), 
                self.cell_size, 
                self,
                length=5
            ))
        else:
            self.snakes.append(Snake(
                int(self.size_x/3), 
                int(self.size_y/3), 
                self.cell_size, 
                self,
                length=5, 
                direction=Vector.right(),
                color=Colors.TRON_RED
            ))
            self.snakes.append(Snake(
                int(self.size_x/3)*2, 
                int(self.size_y/3)*2, 
                self.cell_size, 
                self,
                length=5,
                direction=Vector.left(),
                color=Colors.TRON_BLUE,
                player_one=False
            ))
        self.add_food()
        self.game_state.set(GameState.PLAY)

    def add_food(self):
        '''
        If there is no food on the map, add one.
        '''
        if(self.food is None):
            # get a list of empty locations on the map.
            empty_locs = [
                (e_y, e_x) 
                for e_y in range(len(self.game_map))
                for e_x in range(len(self.game_map[e_y])) 
                if self.game_map[e_y][e_x] is None
            ]
            if(empty_locs):
                empty_location = empty_locs[random.randint(0, len(empty_locs)-1)]
                self.food = Cell(empty_location[1], empty_location[0], self.cell_size, color=Colors.GREEN)
                self.add_to_map(self.food)
            else:
                # Player won! 
                self.game_state.set(GameState.WIN)

    def _set_volatile_params(self):
        '''
        Sets instance parameters which can change depending on the state of the 
        game to defaults. 
        '''
        self.game_map = None
        self.snakes = list()
        self.food = None
        self.game_state = GameState() # defaults to SETUP state

    def _create_new_map(self):
        new_map = list()
        for i in range(self.size_y):
            new_map.append([None] * self.size_x)
        self.game_map = new_map

    def add_to_map(self, new_cell:Cell)->bool:
        '''
        Adds a new cell to the map. Returns if successful.
        '''
        try:
            self.game_map[new_cell.y][new_cell.x] = new_cell
        except IndexError as ie:
            return False
        return True
    
    def remove_from_map(self, dead_cell:Cell)->bool:
        '''
        Removes an existing cell from the map.
        '''
        try:
            self.game_map[dead_cell.y][dead_cell.x] = None
        except IndexError as ie:
            return

    def update(self):
        for s in self.snakes:
            if(not(s.move())):
                self.game_state.set(GameState.GAMEOVER)
        self.add_food()


    def is_out_of_bounds(self, x, y)->bool:
        '''
        Returns if the input location is out of environment bounds.
        '''
        return x < 0 or y < 0 or x >= self.size_x or y >= self.size_y

    def get_location_contents(self, x, y):
        '''
        Returns a Cell if the location contains a cell. Else returns None
        Assumes that location is within bounds.
        '''
        return self.game_map[y][x]

if __name__ == "__main__":
    main()
