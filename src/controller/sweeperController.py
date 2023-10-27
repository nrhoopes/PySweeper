# pyControl controller object for the pysweeperGUI and PySweeper game.
import random

class pyControl:
    # pyControl constructor
    # ties the gui to the controller.
    def __init__(self, GUI) -> None:
        self.gui = GUI

    # Public method startGame
    #
    # Creates a brand new game by initializing all required variables
    # to 0, notifying the gui to clear itself, creates the new gamefield
    # based on predefined numbers, and sends it to the GUI to create the field.
    def startGame(self):
        self.gui.clearFrame(self.gui.mainFrame)
        self.time = 0
        self.bombCount = 0
        self.flagCount = 0
        self.correctFlags = 0
        self.gameField = []
        self.timerRunning = True

        # Predefined 20x20 field (400 tiles) with a 10% chance for a tile to contain a mine.
        # NOTE: This may create performance issues with Tkinter, especially if you increase the number
        #       of tiles, as each tile is an individual widget, and Tkinter runs into performance problems
        #       with a large amount of widgets on screen at once.
        self.gameField = self.__createField(20, 20, 0.10) 
        self.flagCount = self.bombCount
        self.gui.createBasicGame(self.gameField, self.flagCount)

    # Public method setButtonTile
    # Arguments:
    #   - row: the row of the tile
    #   - col: the column of the tile
    #   - button: the button object itself
    #
    # Assigns the button object to the correct place in the 3D list
    # that is the gamefield.  This is used by the GUI when constructing the field
    # for the user.  Storing the button like this allows the game to invoke it later
    # if needed.
    def setButtonTile(self, row, col, button):
        self.gameField[row][col][1] = button

    # Public method unsetButtonTile
    # Arguments:
    #   - row: the row of the tile
    #   - col: the column of the tile
    #
    # When a tile is clicked on, this will remove the button from it's respective
    # coordinates in the gamefield list, notifying the controller that it is no longer
    # an active tile in the game.
    def unsetButtonTile(self, row, col):
        self.gameField[row][col][1] = None

    # Public method printGameField
    #
    # Used for debugging and modification purposes, prints the entire gamefield to the console.
    def printGameField(self):
        for row in self.gameField:
            print("This is Row: " + str(row))

    # Public method notifyFlagSet
    # Arguments:
    #   - row: the row of the tile
    #   - col: the column of the tile
    #
    # Notifies the controller that a flag has been set.  Called in the GUI on right click.
    # Will decrement the flag counter and tell the GUI to display the new flag count.
    # Also checks for win conditions.
    def notifyFlagSet(self, row, col):
        self.flagCount -= 1
        self.gui.updateFlagCounter(self.flagCount)
        if self.gameField[row][col][0] == 'B':
            self.correctFlags += 1
            if self.correctFlags == self.bombCount:
                print("Win!")
                self.gui.notifyWin()
    
    # Public method notifyFlagUnset
    # Arguments:
    #   -row: the row of the tile
    #   -col: the column of the tile
    #
    # Notifies the controller that a flag has been unset.  Called in the GUI on right click.
    # Adds one to the flag count (they are unsetting a previously set flag), and checks if
    # that flag was in a correct position.
    def notifyFlagUnset(self, row, col):
        self.flagCount += 1
        self.gui.updateFlagCounter(self.flagCount)
        if self.gameField[row][col][0] == 'B':
            self.correctFlags -= 1

    # Public method stopTimer
    # 
    # Stops the running timer, in the case of a game loss or win.
    def stopTimer(self):
        self.timerRunning = False

    # Private method __createField
    # Arguments:
    #   - rows: the number of rows to create
    #   - cols: the number of columns to create
    #   - precentChanceOfBomb: the decimal percent chance of a mine appearing per tile.
    #
    # EX:
    #   self.controller.__createField(5, 5, 0.05)
    #   # in this case, a 5x5 (25 tile) field will be created with a 
    #   # 5% chance of a mine existing per tile.
    #
    # Returns:
    #   - field: a 3D list that represents the entire gamefield, including
    #            mine locations and adjacent number tiles.
    def __createField(self, rows, cols, percentChanceOfBomb):
        field = []
        # Populate field with mines
        for i in range(rows):
            row = []
            for j in range(cols):
                if random.random() <= percentChanceOfBomb:
                    row.append(["B", None])
                    self.bombCount += 1
                else:
                    row.append([0, None])
            field.append(row)
        # Label spaces around mines
        for i, row in enumerate(field):
            for j, col in enumerate(row):
                if col[0] == 'B':
                    ## Right of mine ##
                    if not j + 1 >= cols:
                        if field[i][j + 1][0] == 'B':
                            pass
                        else:
                            field[i][j + 1][0] += 1

                    ## Left of mine ##
                    if not j - 1 < 0:
                        if field[i][j - 1][0] == 'B':
                            pass
                        else:
                            field[i][j - 1][0] += 1

                    ## Below mine ##
                    if not i + 1 >= rows:
                        if field[i + 1][j][0] == 'B':
                            pass
                        else:
                            field[i + 1][j][0] += 1

                    ## Above mine ##
                    if not i - 1 < 0:
                        if field[i - 1][j][0] == 'B':
                            pass
                        else:
                            field[i - 1][j][0] += 1

                    ## Top Right ##
                    if not j + 1 >= cols and not i - 1 < 0:
                        if field[i - 1][j + 1][0] == 'B':
                            pass
                        else:
                            field[i - 1][j + 1][0] += 1

                    ## Top Left ##
                    if not j - 1 < 0 and not i - 1 < 0:
                        if field[i - 1][j - 1][0] == 'B':
                            pass
                        else:
                            field[i - 1][j - 1][0] += 1
                    ## Bottom Right ##
                    if not j + 1 >= cols and not i + 1 >= rows:
                        if field[i + 1][j + 1][0] == 'B':
                            pass
                        else:
                            field[i + 1][j + 1][0] += 1

                    ## Bottom Left ##
                    if not j - 1 < 0 and not i + 1 >= rows:
                        if field[i + 1][j - 1][0] == 'B':
                            pass
                        else:
                            field[i + 1][j - 1][0] += 1
        return field
                