import random

class pyControl:
    def __init__(self, GUI) -> None:
        self.gui = GUI

    def startGame(self):
        self.gui.clearFrame(self.gui.mainFrame)
        self.time = 0
        self.bombCount = 0
        self.gameField = []

        self.gameField = self.__createField(20, 20, 0.10)
        self.gui.createBasicGame(self.gameField, self.bombCount)

    def setButtonTile(self, row, col, button):
        self.gameField[row][col][1] = button

    def printGameField(self):
        for row in self.gameField:
            print("This is Row: " + str(row))

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
                