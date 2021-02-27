#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    PiGames
    Author: Raul Rojas
    Contact: rrojas994@gmail.com
    Description: 
        This is a collection of small games that are utilizing the PyGame module. 
        These games are inspired from existing classical games but with a twist.
'''

import PySimpleGUI as sg
import os
import glob
import re


BASEDIR = os.path.dirname(__file__)
window = None
listOfGames = None

def main():
    global listOfGames
    global window

    listOfGames = getGameList()
    window = getGameSelectWindow(listOfGames)

    while True:
        event, values = window.read()
        if(event in ["EXIT", sg.WINDOW_CLOSED]):
            break
        if(re.match(r'GAME_.*\.py', event)):
            window.close()
            launchGame(event)
            break

def launchGame(game:str):
    '''
    Launches a game in a subprocess. 

    :param game: Game file string.
    '''
    print(f"Launching game: {game}")
    

def getGameSelectWindow(gameList:list)->sg.Window:
    '''
    Retrieves a window which acts as a game select screen.
    '''
    win = sg.Window(
        "Game Select", 
        layout=getWindowLayout(gameList),
        no_titlebar=True,
        grab_anywhere=True,
        element_justification='center',
        finalize=True
    )
    return win

def getWindowLayout(gameList:list)->list:
    '''
    Retireves the window layout list for the game select window.
    '''
    gameListButtons = []
    if(gameList):
        for game in gameList:
            gameListButtons.append(
                [
                    sg.Button(
                        game.replace('GAME_', '').replace('.py', '').capitalize(), 
                        key=game
                    )
                ]
            )
    else:
        gameListButtons.append(
            [sg.Text("No Games Found.")]
        )
    layout = [
        [sg.Text("Select Game")],
        [
            sg.Column(
                layout=gameListButtons, 
                scrollable=True, 
                vertical_scroll_only=True, 
                element_justification="center",
                justification="center"
            )
        ],
        [sg.Button("Exit", key="EXIT")]
    ]
    return layout

def getGameList()->list:
    '''
    Returns a list of games that can be played.
    '''
    pyFileList = glob.glob(os.path.join(BASEDIR, "GAME_*.py"))
    gList = [os.path.basename(g) for g in pyFileList]
    return gList

    

if __name__ == "__main__":
    main()