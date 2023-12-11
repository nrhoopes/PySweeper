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
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import StringVar
from PIL import Image, ImageTk

class pysweeper:
    # pysweeper constructor
    # Creates tk Object and populates it with mainMenu widgets.
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("PySweeper")
        self.root.resizable(False, False)

        # Load all images
        self.mineImgRaw = Image.open('src/img/mine.png')
        # self.mineImgRaw = self.mineImgRaw.resize((25, 25))
        self.mineImg = ImageTk.PhotoImage(self.mineImgRaw)

        self.zeroImgRaw = Image.open('src/img/zero.png')
        self.zeroImg = ImageTk.PhotoImage(self.zeroImgRaw)

        self.oneImgRaw = Image.open('src/img/one.png')
        self.oneImg = ImageTk.PhotoImage(self.oneImgRaw)

        self.twoImgRaw = Image.open('src/img/two.png')
        self.twoImg = ImageTk.PhotoImage(self.twoImgRaw)

        self.threeImgRaw = Image.open('src/img/three.png')
        self.threeImg = ImageTk.PhotoImage(self.threeImgRaw)

        self.fourImgRaw = Image.open('src/img/four.png')
        self.fourImg = ImageTk.PhotoImage(self.fourImgRaw)

        self.fiveImgRaw = Image.open('src/img/five.png')
        self.fiveImg = ImageTk.PhotoImage(self.fiveImgRaw)

        self.sixImgRaw = Image.open('src/img/six.png')
        self.sixImg = ImageTk.PhotoImage(self.sixImgRaw)

        self.sevenImgRaw = Image.open('src/img/seven.png')
        self.sevenImg = ImageTk.PhotoImage(self.sevenImgRaw)

        self.eightImgRaw = Image.open('src/img/eight.png')
        self.eightImg = ImageTk.PhotoImage(self.eightImgRaw)

        self.flagImgRaw = Image.open('src/img/flag1.png')
        self.flagImg = ImageTk.PhotoImage(self.flagImgRaw)

        self.emptyTileRaw = Image.open('src/img/emptyTile.png')
        self.emptyTile = ImageTk.PhotoImage(self.emptyTileRaw)

        self.titleImgRaw = Image.open('src/img/title.png')
        self.titleImg = ImageTk.PhotoImage(self.titleImgRaw)

        # Create and populate Main Menu, then display
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
        self.mainFrame.grid_propagate(True)
        welcomeLabel = tk.Label(self.mainFrame, image=self.titleImg, text="PySweeper", font=('Arial', 72))
        welcomeLabel.grid(row=0, column=0, padx=25)
        descLabel = tk.Label(self.mainFrame, text="A minesweeper clone, in Python", font=('Arial', 14))
        descLabel.grid(row=1, column=0, padx=25)

        playGameButton = tk.Button(self.mainFrame, text="Play Game", font=('Arial', 56), width=10, command=lambda: self.controller.startGame())
        highScoreButton = tk.Button(self.mainFrame, text="High Scores", font=('Arial', 56), width=10, command=lambda: self.showScoreboard())
        quitGameButton = tk.Button(self.mainFrame, text="Quit Game", font=('Arial', 56), width=10, command=lambda: self.root.destroy())

        dummySpace = tk.Label(self.mainFrame, text="")
        dummySpace.grid(row=2, column=0, pady=25, padx=25)

        playGameButton.grid(row=3, column=0, pady=25, padx=25)
        highScoreButton.grid(row=4, column=0, pady=25, padx=25)
        quitGameButton.grid(row=5, column=0, pady=25, padx=25)

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
        self.flagCounterFrame = tk.Frame(self.infoFrame, highlightbackground="gray")
        self.gameFrame = tk.Frame(self.mainFrame, highlightthickness=4, highlightbackground="gray", background="gray")
        self.gameFrame.grid_columnconfigure(0, weight=1)
        
        # Different sized images for the top label
        self.mineImgLargeRaw = self.mineImgRaw.resize((36, 36))
        self.mineImgLarge = ImageTk.PhotoImage(self.mineImgLargeRaw)

        self.flagImgLargeRaw = self.flagImgRaw.resize((36, 36))
        self.flagImgLarge = ImageTk.PhotoImage(self.flagImgLargeRaw)

        mineLabel = tk.Label(self.flagCounterFrame, image=self.mineImgLarge)
        slashLabel = tk.Label(self.flagCounterFrame, text="/", font=("", 19), highlightbackground="gray")
        flagLabel = tk.Label(self.flagCounterFrame, image=self.flagImgLarge)
        colonLabel = tk.Label(self.flagCounterFrame, text=":", font=("", 19), highlightbackground="gray")

        mineLabel.grid(row=0, column=0, sticky="w")
        slashLabel.grid(row=0, column=1, sticky="w")
        flagLabel.grid(row=0, column=2, sticky="w")
        colonLabel.grid(row=0, column=3, sticky="w")
        self.flagCounter = tk.Label(self.flagCounterFrame, text="0" + str(bombCount), background="black", foreground="red", font=("", 25))
        self.flagCounter.grid(row=0, column=4, sticky="w")

        self.flagCounterFrame.grid(row=0, column=0, sticky="w")

        self.restartImgRaw = Image.open('src/img/restart.png')
        self.restartImgRaw = self.restartImgRaw.resize((64, 64))
        self.restartImg = ImageTk.PhotoImage(self.restartImgRaw)

        restartButton = tk.Button(self.infoFrame, image=self.restartImg, font=("", 25), command=self.controller.startGame)
        restartButton.grid(row=0, column=1, padx=50)

        timerLabel = tk.Label(self.infoFrame, text="Time:", font=("", 25), highlightbackground="gray")
        timerLabel.grid(row=0, column=2, sticky="e")
        self.timer = tk.Label(self.infoFrame, text=str("0"), background="black", foreground="red", font=("", 25), width=3, anchor="e")
        self.timer.grid(row=0, column=3, sticky="e")

        # # # # # # Creation of the label field underneath the tiles. # # # # # #
        for i, row in enumerate(gameField):
            for k, spot in enumerate(row):
                match spot[0]:
                    case 'B':
                        label = tk.Label(self.gameFrame, image=self.mineImg, background="gray")
                    case 0:
                        label = tk.Label(self.gameFrame, image=self.zeroImg, background="gray")
                    case 1:
                        label = tk.Label(self.gameFrame, image=self.oneImg, background="gray")
                    case 2:
                        label = tk.Label(self.gameFrame, image=self.twoImg, background="gray")
                    case 3:
                        label = tk.Label(self.gameFrame, image=self.threeImg, background="gray")
                    case 4:
                        label = tk.Label(self.gameFrame, image=self.fourImg, background="gray")
                    case 5:
                        label = tk.Label(self.gameFrame, image=self.fiveImg, background="gray")
                    case 6:
                        label = tk.Label(self.gameFrame, image=self.sixImg, background="gray")
                    case 7:
                        label = tk.Label(self.gameFrame, image=self.sevenImg, background="gray")
                    case 8:
                        label = tk.Label(self.gameFrame, image=self.eightImg, background="gray")
                    case _:
                        label = tk.Label(self.gameFrame, text=spot[0], background="gray")
                label.grid(row=i, column=k, padx=8, pady=8)
    
        # # # # # # Creation of the tile field itself. # # # # # # 
        for row in range(rows):
            for col in range(cols):
                button = tk.Button(self.gameFrame, width=39, height=39, image=self.emptyTile, highlightbackground="gray")
                
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
        self.controller.stopTimer()
        tk.messagebox.showinfo(parent=self.root, title="Victory!", message="Congratulations! You cleared the Minefield!")
        # Check to see if a new score is valid.
        if self.controller.checkIfScoreValid():
            # Update high scores
            self.newHighscore()
        else:
            self.clearFrame(self.mainFrame)
            self.populateMainMenu()
            self.showScoreboard()

    def newHighscore(self):
        self.highScoreEntryWin = tk.Toplevel()
        self.highScoreEntryWin.protocol('WM_DELETE_WINDOW', lambda: self.__cancelHighScore())
        
        congratsLabel = tk.Label(self.highScoreEntryWin, font=('', 19), text="Congratulations! Your time was: " + str(self.controller.time) + " seconds.\nEnter your intitials for the scoreboard!:")
        congratsLabel.grid(row=0, column=0, columnspan=2)

        self.username = StringVar()
        self.usernameEntry = tk.Entry(self.highScoreEntryWin, justify='center', width=20, font=('Arial', 26), textvariable=self.username)
        self.username.trace("w", lambda *args: self.__charLimit(self.username))
        self.usernameEntry.grid(row=1, column=0, columnspan=2)

        enterButton = tk.Button(self.highScoreEntryWin, text="Enter", font=('', 30), command=lambda: self.__sendUsername(self.username.get(), self.controller.time))
        enterButton.grid(row=2, column=0, sticky="e")

        cancelButton = tk.Button(self.highScoreEntryWin, text="Cancel", font=('', 30), command=lambda: self.__cancelHighScore())
        cancelButton.grid(row=2, column=1, sticky="w")

    def __cancelHighScore(self):
        self.highScoreEntryWin.destroy()
        self.scoreHandshake(True)

    def scoreHandshake(self, success):
        if not success:
            tk.messagebox.showerror(title="Error!", message="Something has gone wrong with saving your score!")

        self.showScoreboard()
        self.clearFrame(self.mainFrame)
        self.populateMainMenu()

    def showScoreboard(self):
        self.scoreboardWin = tk.Toplevel()
        scores = self.controller.getScoreboardInfo()

        table = ttk.Treeview(self.scoreboardWin, columns=('Place', 'Player', 'Score'), show='headings')
        table.heading('Place', text='Place')
        table.heading('Player', text='Player')
        table.heading('Score', text='Score')
        table.column('Place', width=100, anchor='e')
        table.column('Player', anchor='center')
        table.column('Score', width=375, anchor='e')

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", rowheight=60, font=('', 20))

        for pos, item in enumerate(scores):
            item = list(item)
            item[0] = pos + 1
            item[2] = str(item[2]) + ' seconds'
            table.insert('', tk.END, values=item)

        highScoreTitle = tk.Label(self.scoreboardWin, text="High Scores!", font=('', 30))

        highScoreTitle.grid(row=0, column=0)
        table.grid(row=1, column=0, padx=5, pady=5)



    def __charLimit(self, username):
        if len(username.get()) > 0:
            username.set(username.get()[:3].upper())

    def __sendUsername(self, username, time):
        self.controller.createHighscoreEntry(username, time)
        self.highScoreEntryWin.destroy()


    # Private method __gameLoss
    # Arguments:
    #   - button: The tile to destroy when uncovering a mine.
    #
    # When the conditions for a game loss is met (a user clicks a tile that covers a mine),
    # the user will be notified of a gameloss.
    def __gameLoss(self, button):
        button.destroy()
        # If this is the first mine that the player has clicked on.
        if self.controller.getRunningStatus():
            self.controller.stopTimer()
            self.__searchMines()
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

    # Private method __searchMines
    #
    # Used on a gameloss situation.  If a player steps on a mine, the game will want to 
    # show the user where the remaining mines are, so it will invoke the button above every
    # mine to display that to the user.
    def __searchMines(self):
        field = self.controller.getGameField()
        for row in field:
            for col in row:
                if col[0] == 'B' and col[1].winfo_exists():
                    if col[1].cget("state") == 'disabled':
                        col[1].configure(state="normal")
                    col[1].invoke()

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
        field = self.controller.getGameField()
        
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
            event.widget.configure(image=self.emptyTile, state="normal")
            event.widget.bind("<Button-2>", lambda event, status=False: self.__setFlag(event, status, row, col))
            event.widget.bind("<Button-3>", lambda event, status=False: self.__setFlag(event, status, row, col))

            self.controller.notifyFlagUnset(row, col)
        else: # If flag is not set
            if self.controller.flagCount > 0: # If player still has flags remaining
                # set flag
                event.widget.bind("<Button-2>", lambda event, status=True: self.__setFlag(event, status, row, col))
                event.widget.bind("<Button-3>", lambda event, status=True: self.__setFlag(event, status, row, col))

                # Prevents player from accidentally clicking an already flagged tile.
                event.widget.configure(image=self.flagImg, state="disabled")

                self.controller.notifyFlagSet(row, col)

    # Private method __updateTimer
    #
    # Called by tkinter every second to increment the time
    # counter.
    def __updateTimer(self):
        if self.controller.timerRunning:
            self.controller.time += 1
            self.timer.configure(text=str(self.controller.time))
            self.infoFrame.after(1000, self.__updateTimer)
        else:
            print("final time: " + str(self.controller.time) + " seconds")


# pysweeper()
