import random

class pyControl:
    def __init__(self, GUI) -> None:
        self.gui = GUI
        self.gameField = []
        self.bombCount = 0

    def startGame(self):
        self.gui.clearFrame(self.gui.mainFrame)

        self.gameField = self.__createField(20, 20, 0.15)
        self.gui.createBasicGame(self.gameField)

    def __createField(self, rows, cols, percentChanceOfBomb):
        field = []
        # Populate field with mines
        for i in range(rows):
            row = []
            for j in range(cols):
                if random.random() <= percentChanceOfBomb:
                    row.append("B")
                    self.bombCount += 1
                else:
                    row.append(0)
            field.append(row)
        # Label spaces around mines
        for i, row in enumerate(field):
            for j, col in enumerate(row):
                if col == 'B':
                    ## Right of mine ##
                    if not j + 1 >= cols:
                        if field[i][j + 1] == 'B':
                            pass
                        else:
                            field[i][j + 1] += 1

                    ## Left of mine ##
                    if not j - 1 < 0:
                        if field[i][j - 1] == 'B':
                            pass
                        else:
                            field[i][j - 1] += 1

                    ## Below mine ##
                    if not i + 1 >= rows:
                        if field[i + 1][j] == 'B':
                            pass
                        else:
                            field[i + 1][j] += 1

                    ## Above mine ##
                    if not i - 1 < 0:
                        if field[i - 1][j] == 'B':
                            pass
                        else:
                            field[i - 1][j] += 1

                    ## Top Right ##
                    if not j + 1 >= cols and not i - 1 < 0:
                        if field[i - 1][j + 1] == 'B':
                            pass
                        else:
                            field[i - 1][j + 1] += 1

                    ## Top Left ##
                    if not j - 1 < 0 and not i - 1 < 0:
                        if field[i - 1][j - 1] == 'B':
                            pass
                        else:
                            field[i - 1][j - 1] += 1
                    ## Bottom Right ##
                    if not j + 1 >= cols and not i + 1 >= rows:
                        if field[i + 1][j + 1] == 'B':
                            pass
                        else:
                            field[i + 1][j + 1] += 1

                    ## Bottom Left ##
                    if not j - 1 < 0 and not i + 1 >= rows:
                        if field[i + 1][j - 1] == 'B':
                            pass
                        else:
                            field[i + 1][j - 1] += 1
        return field
                