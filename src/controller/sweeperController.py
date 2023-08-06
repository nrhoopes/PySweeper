class pyControl:
    def __init__(self, GUI) -> None:
        self.gui = GUI

    def startGame(self):
        self.gui.clearFrame(self.gui.mainFrame)

        self.gui.createBasicGame()