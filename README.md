# PiGames
Author: Raul Rojas
Contact: rrojas994@gmail.com

### Description:
PiGames is a collection of simple games that utilize the pygame module. This 
project provides its own simple game launcher which loads available games in 
the project. 

### Included Game List: 
* Snake

### Setup
* Download project files via `git clone` or zip file. 
* Run `python3 setup.py` on Linux

### Usage
* Developed in an Ubuntu Linux environment. Can't guarantee that it works anywhere 
else.

---

## Version History

### V0.2.0
* Launcher now actually launches the selected game. 
* Added basic functionality to snake game. 
    * Snake is drawn to screen with a length of 3 cells as a starting point.
    * Movement can be controlled with arrow keys on the keyboard.
    * There still isn't any food for the snake to pick up.

### V0.1.0
* Initial version of the project. 
* Contains a very basic GUI which generates a list of games from the games directory. 
* Doesn't actually load the games yet. Currently only prints out that it is launching 
the game to console but doesn't actually do anything.
