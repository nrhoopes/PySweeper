# PySweeper
A minesweeper clone, built in Python utilizing an MVC structure.

# Python Version and Operating Systems
- Developed on Python 3.10.12
- Tested in Python 3.10, 3.11
- Written for Debian Linux (Verified working on Ubuntu)
- Tested and functional in Windows 10 on 1080p screens.

# Instructions for Running current build
1. Clone Repository
2. Use command ```cd PySweeper```
3. Run the program using:
    - ```python3 main.py``` for Linux
    - ```py main.py``` for Windows

# Instructions for Play
The game is played exactly like Minesweeper, upon creating a new game, you are presented with
a field of tiles you can either right click, or left click on.
    
    - A left click with uncover what is behind the tile
    - A right click will mark the tile with a flag

In order to complete the game, the objective is to mark all of the mines on the field correctly,
with or without clearing the remaining empty tiles.  If you clear a tile that is not a mine,
there will be a number uncovered that corresponds to the number of adjacent mines to that tile
you cleared.  This means if you uncover a 2, then that tile is touching a mine, either vertically,
horizontally, or diagonally.  The maximum number of adjacent mines is 8, while the minimum is 0.
If you clear a tile that has 0 adjacent mines, the game will automatically uncover all adjacent
0 tiles recursively, including any adjacent number tiles to those 0 tiles to quickly clear dummy
tiles in the minefield.

Currently when the field is being created, the default difficulty causes tiles to have a 10%
chance of being a mine, resulting in anywhere between 35-45 mines being populated in a 400
tile field.

# Future Work:
- A High Score board for users to compete in speedrunning a minefield.
- Multiple / User customized difficulty levels