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

        # Predefined 20x20 field (400 tiles) with a 10% chance for a tile to contain a mine.
        # NOTE: This may create performance issues with Tkinter, especially if you increase the number
        #       of tiles, as each tile is an individual widget, and Tkinter runs into performance problems
        #       with a large amount of widgets on screen at once.
        self.gameField = self.__createField(20, 20, 0.10) 
        self.flagCount = self.bombCount
        self.gui.createBasicGame(self.gameField, self.flagCount)

    def setButtonTile(self, row, col, button):
        self.gameField[row][col][1] = button

    def unsetButtonTile(self, row, col):
        self.gameField[row][col][1] = None

    def printGameField(self):
        for row in self.gameField:
            print("This is Row: " + str(row))

    def notifyFlagSet(self, row, col):
        self.flagCount -= 1
        self.gui.updateFlagCounter(self.flagCount)
        if self.gameField[row][col][0] == 'B':
            self.correctFlags += 1
            if self.correctFlags == self.bombCount:
                print("Win!")
                self.gui.notifyWin()
    
    def notifyFlagUnset(self, row, col):
        self.flagCount += 1
        self.gui.updateFlagCounter(self.flagCount)
        if self.gameField[row][col][0] == 'B':
            self.correctFlags -= 1

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
                