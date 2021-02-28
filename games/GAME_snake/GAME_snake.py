#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    GAME_snake.py
    Author: Raul Rojas
    Contact: rrojas994@gmail.com
    Description:
        The game of snake. Pretty much just as simple as you can get.
'''
import sys
import pygame
pygame.init()

_white = (255, 255, 255)
_black = (0, 0, 0)
_red = (255, 0, 0)
_green = (0, 255, 0)
_blue = (0, 0, 255)

size = (800,600)
screen = pygame.display.set_mode(size=size)

def main():
    """
    Main loop of game.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(_white)
        pygame.draw.rect(screen, _black, [400, 300, 10, 10])
        
        pygame.display.update()
        

if __name__ == "__main__":
    main()
