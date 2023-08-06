from src.view.pysweeperGUI import pysweeper
from src.controller.sweeperController import pyControl

game = pysweeper()

controller = pyControl(game)
game.assignController(controller)

game.launch()