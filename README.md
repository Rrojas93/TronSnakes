# Tron Snakes
Author: Raul Rojas
Contact: rrojas994@gmail.com

### Description:
Tron snakes is a game that mixes... wait for it... Tron and Snake! There is a single
and two player mode. Single player is just the good old classic Snake. The two 
player mode is where the real fun is! Two players must race to the green apple
to get larger and be able to eliminate the other player! There are three rounds
and the winner is decided based on score (how many apples you eat) however, you 
will lose points if you die!

### Setup
#### Linux
* Download project files via `git clone` or zip file. 
* Ensure you have python 3 and pip 3 installed with `python3 -V` and `pip3 -V`
    * To install run `sudo apt-get install python3 python3-pip`
* Set setup.py as executable with `sudo chmod +x setup.py`
* Run `python3 setup.py` on Linux
* Run game with `python3 TronSnakes.py`

#### Windows
* Ensure you have [python 3](https://www.python.org/) installed 
* Run `python -m pip install setuptools`
* Run `python -m pip install -r requirements.txt`
* Run game with `python TronSnakes.py`

---

## Version History
### V2.0.0
* Scrapped the need for a launcher
* Snake game is now complete and is renamed "TronSnakes.py".
* TronSnakes is now the top level script in root directory.
* TronSnakes supports two players or a solo player now.

### V1.0.0
* Snake Game is now in a most basic complete state. 
    * Single player only. Game resets upon colliding with self or screen bounds.

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
