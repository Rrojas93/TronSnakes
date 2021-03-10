# -*- coding: utf-8 -*-

'''
    PiGames
    Author: Raul Rojas
    Contact: rrojas994@gmail.com
    Description: 
        Opens a small game launcher for all available py games in the "games"
        directory in the project.
'''

import PySimpleGUI as sg
import os
import glob
import re
import subprocess
import platform

BASEDIR = os.path.dirname(os.path.abspath(__file__))
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
        if(re.match(r'GAME_.*\.py', os.path.basename(event))):
            window.close()
            launchGame(event)
            break

def launchGame(game:str):
    '''
    Launches a game in a subprocess. 

    :param game: Game file path string.
    '''
    python_version = 'python3' if platform.system().lower() == 'linux' else 'python'
    gameProc = subprocess.Popen(
        f"{python_version} {game}", 
        stdin=None, 
        stdout=None, 
        stderr=None, 
        close_fds=True,
        shell=True,
        cwd=os.path.dirname(game)
    )
    window.close()
    gameProc.wait() # wait for the game to exit to close out launcher process.

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
        for gamePath in gameList:
            game = os.path.basename(gamePath) # isolate file name from path.
            gameListButtons.append(
                [
                    sg.Button(
                        game.replace('GAME_', '').replace('.py', '').capitalize(), # clean up the name 
                        key=gamePath # the key to use is the path of the file.
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
    pyFileList = glob.glob(os.path.join(BASEDIR, 'games', 'GAME_*', "GAME_*.py"))
    return pyFileList

    

if __name__ == "__main__":
    main()