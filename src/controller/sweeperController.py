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
        for i in range(rows):
            row = []
            for j in range(cols):
                if random.random() <= percentChanceOfBomb:
                    row.append("B")
                    self.bombCount += 1
                else:
                    row.append(" ")
            field.append(row)
        return field
                