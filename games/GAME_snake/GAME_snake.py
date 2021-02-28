#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    GAME_snake.py
    Author: Raul Rojas
    Contact: rrojas994@gmail.com
    Description:
        The game of snake. Pretty much just as simple as you can get.
'''
import os, sys, time
import pygame
pygame.init()

screen_size = (800,600)
screen = pygame.display.set_mode(size=screen_size)
refresh_delay = 0.05 # equates to game speed, the lower the number the faster the snake moves.
last_refresh = 0 # the last time a refresh occured.
snake = None

def main():
    """
    Main loop of game.
    """
    global snake
    global last_refresh
    snake = Snake(
        int(screen_size[0]/2), 
        int(screen_size[1]/2),
        10, 
        screen_size
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_ESCAPE):
                    sys.exit()
                snake.change_direction(event.key)
        if((last_refresh+refresh_delay) <= time.time()):
            update()
            last_refresh = time.time()
        pygame.display.update()

def update():
    '''
    Redraws all game objects on the screen.
    '''
    snake.move() # move the snake first so screen represents current location.
    screen.fill(Colors.BLACK)
    snake.draw()

class Colors():
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    def __init__(self):
        pass


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
        Returns a down vector (0,-1)
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

    :param 
    """
    def __init__(
        self, 
        location_x:int,
        location_y:int,
        size:int,
        parent_cell=None,
        child_cell = None
    ):
        self.x = location_x
        self.y = location_y
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.parent = parent_cell
        self.child = child_cell

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
        pygame.draw.rect(
            screen,
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
        screen_size:tuple,
        color=Colors.WHITE,
        length=3,
        direction=Vector.up(),
    ):
        self.cell_size = cell_size
        self.color = color
        self.length = length
        self.direction = direction
        self.head = None
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
                self.head = Cell(location_x, location_y, self.cell_size)
                current_cell = self.head
                continue
            current_cell.child = Cell(
                current_cell.x+(self.cell_size*self.direction.opposite().x),
                current_cell.y+(self.cell_size*self.direction.opposite().y),
                self.cell_size,
                parent_cell=current_cell
            )
            current_cell = current_cell.child # set new child cell as current cell

    def draw(self):
        '''
        Draws the snake on the screen.
        '''
        current_cell = self.head
        while(current_cell is not None):
            current_cell.draw(self.color)
            current_cell = current_cell.child

    def move(self):
        '''
        Moves the snake in the direction of movement.
        '''
        new_cell = Cell(
            self.head.x + (self.cell_size*self.direction.x),
            self.head.y + (self.cell_size*self.direction.y),
            self.cell_size,
            child_cell=self.head
        )
        self.head.parent = new_cell
        self.head = new_cell
        self.head.get_tail().remove() # gets the last cell in the chain and removes it.

    def change_direction(self, key_code):
        '''
        Changes the direction of the snake and prevents it from moving backwards.
        '''
        if(key_code == pygame.K_LEFT and self.direction != Vector.right()):
            self.direction = Vector.left()
        elif(key_code == pygame.K_RIGHT and self.direction != Vector.left()):
            self.direction = Vector.right()
        elif(key_code == pygame.K_UP and self.direction != Vector.down()):
            self.direction = Vector.up()
        elif(key_code == pygame.K_DOWN and self.direction != Vector.up()):
            self.direction = Vector.down()

    def add_cell_head(self, location_x:int, location_y:int):
        """
        Addes a new cell to the head of the snake. 

        :param location_x: The x location of the new cell.
        :param location_y: The y locaiton of the new cell.
        """
        old_head = self.head
        self.head = Cell(location_x, location_y, self.cell_size, child_cell=old_head)
        old_head.parent = self.head
    
    def out_of_bounds(self)->bool:
        '''
        Checks if the snake is out of bounds. 
        '''
        if(
            self.head.x < 0 or
            self.head.x > screen_size[0] or
            self.head.y < 0 or
            self.head.y > screen_size[1]
        ):
            return True
        else:
            return False


if __name__ == "__main__":
    main()
