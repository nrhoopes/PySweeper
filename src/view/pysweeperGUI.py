# PySweeper GUI
# Implemented using Python's tkinter
#
# TO USE:
#   In a main driver script, create a pysweeper object.  This object is what
#   will be passed to the pyControl object, defined in the sweeperController.py file.
#   NOTE:
#       A pyControl controller object is required to be tied to the GUI using
#       the assignController() method, otherwise the game will not be able to function
#       correctly.  Assure to do this in the main.py driver script.
#
#   When everything is correctly assigned and linked, use the GUI's .launch() method
#   to launch the application.
#
#   EX:
#       gui = pysweeper()
#       controller = pyControl(gui)
#       gui.assignController(controller)
#       gui.launch()

import tkinter as tk
from tkinter import messagebox

class pysweeper:
    # pysweeper constructor
    # Creates tk Object and populates it with mainMenu widgets.
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("PySweeper")
        self.mainFrame = tk.Frame(self.root)

        self.populateMainMenu()

        self.mainFrame.pack()

    # Public method launch
    #
    # Used in the main.py driver script to launch the mainloop of the
    # tkinter program.
    def launch(self):
        self.root.mainloop()

    # Public method clearFrame
    # Arguments:
    #   - frame: The tkinter.Frame frame to be cleared
    #
    # Clears all widgets from the passed frame.
    def clearFrame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    # Public method populateMainMenu
    # 
    # Populates the self.mainFrame with the widgets for the main menu.
    def populateMainMenu(self):
        welcomeLabel = tk.Label(self.mainFrame, text="PySweeper", font=('Arial', 72))
        welcomeLabel.grid(row=0, column=0)
        descLabel = tk.Label(self.mainFrame, text="A minesweeper clone, in Python", font=('Arial', 14))
        descLabel.grid(row=1, column=0)

        playGameButton = tk.Button(self.mainFrame, text="Play Game", font=('Arial', 56), width=10, command=lambda: self.controller.startGame())
        quitGameButton = tk.Button(self.mainFrame, text="Quit Game", font=('Arial', 56), width=10, command=lambda: self.root.destroy())

        dummySpace = tk.Label(self.mainFrame, text="")
        dummySpace.grid(row=2, column=0, pady=50)

        playGameButton.grid(row=3, column=0, pady=25)
        quitGameButton.grid(row=4, column=0, pady=25)

    # Public method assignController
    # Arguments:
    #   - controller: A pyControl object
    #
    # Used to link a pyControl controller object to the GUI object
    # used to launch the game.
    def assignController(self, controller):
        self.controller = controller

    # Public method createBasicGame
    # Arguments:
    #   - gameField: A 2D list that represents the game field, passed in
    #                by the controller.
    #   - bombCount: The total number of mines on the field.
    #
    # Creates a minefield of tiles and labels underneath the tiles. Assigns
    # each tile a function corresponding to the label underneath it, and tied
    # that row and column of the gameField list.
    def createBasicGame(self, gameField, bombCount):
        # Default game field size is 20x20, 400 tiles.
        cols = 20
        rows = 20

        # # # # # # Creation of the timer and flag count labels, and the reset button. # # # # # # 
        self.infoFrame = tk.Frame(self.mainFrame, highlightthickness=4, highlightbackground="gray", background="gray")
        self.gameFrame = tk.Frame(self.mainFrame, highlightthickness=4, highlightbackground="gray", background="gray")
        self.gameFrame.grid_columnconfigure(0, weight=1)
        
        flagLabel = tk.Label(self.infoFrame, text="B/F:", font=("", 25), highlightbackground="gray")
        flagLabel.grid(row=0, column=0, sticky="w")
        self.flagCounter = tk.Label(self.infoFrame, text="0" + str(bombCount), background="black", foreground="red", font=("", 25))
        self.flagCounter.grid(row=0, column=1, sticky="w")

        restartButton = tk.Button(self.infoFrame, text="R", font=("", 25), command=self.controller.startGame)
        restartButton.grid(row=0, column=2, padx=50)

        timerLabel = tk.Label(self.infoFrame, text="Time:", font=("", 25), highlightbackground="gray")
        timerLabel.grid(row=0, column=3, sticky="e")
        self.timer = tk.Label(self.infoFrame, text=str("0"), background="black", foreground="red", font=("", 25), width=3, anchor="e")
        self.timer.grid(row=0, column=4, sticky="e")

        # # # # # # Creation of the label field underneath the tiles. # # # # # #
        for i, row in enumerate(gameField):
            for k, spot in enumerate(row):
                label = tk.Label(self.gameFrame, text=spot[0], padx=12, pady=5, background="gray")
                label.grid(row=i, column=k)
    
        # # # # # # Creation of the tile field itself. # # # # # # 
        for row in range(rows):
            for col in range(cols):
                button = tk.Button(self.gameFrame, width=1, height=1, text="", highlightbackground="gray")
                
                # Setting of the three different functions depending on the label underneath the tile.
                if gameField[row][col][0] == 'B':
                    # If the tile is a mine, call for a game loss condition.
                    button.configure(command=lambda bn=button: self.__gameLoss(bn))
                elif gameField[row][col][0] == 0:
                    # If the tile is a 0, recursively search through the adjacent 0's
                    button.configure(command=lambda bn=button, row=row, col=col: self.__searchZeroes(bn, row, col))
                else: 
                    # If the tile is anything else (a number) simply destroy itself on click.
                    button.configure(command=lambda bn=button, row=row, col=col: self.__regButtonClick(bn, row, col))

                # Right click/Middle click events depending on OS
                button.bind("<Button-2>", lambda event, status=False, row=row, col=col: self.__setFlag(event, status, row, col))
                button.bind("<Button-3>", lambda event, status=False, row=row, col=col: self.__setFlag(event, status, row, col))

                button.grid(row=row, column=col)

                # Send the actual button address to the controller to store in another list with the corresponding position.
                self.controller.setButtonTile(row, col, button)


        self.infoFrame.grid(row=0, column=0)
        self.gameFrame.grid(row=1, column=0)
        # 1 second to allow loading, 1 second to begin timer.
        # May be better to start timer on first button click in future...
        self.infoFrame.after(2000, self.__updateTimer)
    
    # Public method updateFlagCounter
    # Arguments:
    #   - flagCount: The number of flags to update the counter with.
    #
    # Accepts a flag count and updates the flagCounter label to that value on screen.
    def updateFlagCounter(self, flagCount):
        if flagCount > 9:
            self.flagCounter.configure(text="0" + str(flagCount))
        else:
            self.flagCounter.configure(text="00" + str(flagCount))

    # Public method notifyWin
    #
    # Causes a message box to appear, notifying the user they have won.  Then clears the
    # screens and loads the main menu.
    def notifyWin(self):
        tk.messagebox.showinfo(parent=self.root, title="Victory!", message="Congratulations! You cleared the Minefield!")
        self.clearFrame(self.mainFrame)
        self.populateMainMenu()

    # Private method __gameLoss
    # Arguments:
    #   - button: The tile to destroy when uncovering a mine.
    #
    # When the conditions for a game loss is met (a user clicks a tile that covers a mine),
    # the user will be notified of a gameloss.
    def __gameLoss(self, button):
        button.destroy()
        tk.messagebox.showinfo(parent=self.root, title="KABOOM!", message="You've stepped on a mine! Game Over!")
        self.clearFrame(self.mainFrame)
        self.populateMainMenu()

    # Private method __regButtonClick
    # Arguments:
    #   - button: the tile clicked
    #   - row: the row of the tile
    #   - col: the col of the tile
    #
    # Destroys the button passed when it is clicked, and notifies the controller of it being pressed.
    def __regButtonClick(self, button, row, col):
        button.destroy()
        self.controller.unsetButtonTile(row, col)

    # Private method __searchZeroes
    # Arguments:
    #   - button: the tile clicked
    #   - row: the row of the tile
    #   - col: the col of the tile
    #
    # Destroys the button passed when it is clicked.
    # Because it is a zero, the game knows there are no mines adjacent to it,
    # so it automatically invokes a button press on each of the surrounding buttons adjacent
    # to it.  If any of those buttons also happen to be covering a 0, the game will
    # then recursively call this function to continuously clear out 0 tiles.
    def __searchZeroes(self, button, row, col):
        button.destroy()
        self.controller.unsetButtonTile(row, col)
        field = self.controller.gameField
        
        if len(field) > row + 1 and len(field[row]) > col + 1:
            if field[row+1][col+1][1] is not None:
                field[row+1][col+1][1].invoke()
        if len(field) > row + 1:
            if field[row+1][col][1] is not None:
                field[row+1][col][1].invoke()
        if len(field) > row + 1 and 0 <= col - 1:
            if field[row+1][col-1][1] is not None:
                field[row+1][col-1][1].invoke()

        if len(field[row]) > col + 1:
            if field[row][col+1][1] is not None:
                field[row][col+1][1].invoke()
        if 0 <= col - 1:
            if field[row][col-1][1] is not None:
                field[row][col-1][1].invoke()

        if 0 <= row - 1 and len(field[row]) > col + 1:
            if field[row-1][col+1][1] is not None:
                field[row-1][col+1][1].invoke()
        if 0 <= row - 1:
            if field[row-1][col][1] is not None:
                field[row-1][col][1].invoke()
        if 0 <= row - 1 and 0 <= col - 1:
            if field[row-1][col-1][1] is not None:
                field[row-1][col-1][1].invoke()
    # Private method __setFlag
    # Arguments:
    #   - event: The button event that occurred (right click)
    #   - status: Whether or not the flag should be set or unset
    #   - row: the row of the tile
    #   - col: the column of the tile
    #
    # Will either set or unset a flag on a tile when the user right/middle clicks it.
    # Will not allow a flag to be set if there are no flags remaining.
    def __setFlag(self, event, status, row, col):
        if status: # If flag is set
            # unset flag
            event.widget.configure(text="")
            event.widget.bind("<Button-2>", lambda event, status=False: self.__setFlag(event, status, row, col))
            event.widget.bind("<Button-3>", lambda event, status=False: self.__setFlag(event, status, row, col))

            self.controller.notifyFlagUnset(row, col)
        else: # If flag is not set
            if self.controller.flagCount > 0: # If player still has flags remaining
                # set flag
                event.widget.configure(text="F")
                event.widget.bind("<Button-2>", lambda event, status=True: self.__setFlag(event, status, row, col))
                event.widget.bind("<Button-3>", lambda event, status=True: self.__setFlag(event, status, row, col))

                self.controller.notifyFlagSet(row, col)

    # Private method __updateTimer
    #
    # Called by tkinter every second to increment the time
    # counter.
    def __updateTimer(self):
        self.controller.time += 1
        self.timer.configure(text=str(self.controller.time))
        self.infoFrame.after(1000, self.__updateTimer)


# pysweeper()
