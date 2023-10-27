# main.py is the driver script for the project
# import both the GUI and the pyControl class constructors
from src.view.pysweeperGUI import pysweeper
from src.controller.sweeperController import pyControl

# Create a GUI
game = pysweeper()

# Create a controller object and pass the GUI in.
controller = pyControl(game)

# Assign the controller to the GUI using the built in function.
game.assignController(controller)

# Launch the mainloop of the GUI.
game.launch()