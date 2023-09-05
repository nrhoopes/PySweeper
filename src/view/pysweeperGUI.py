import tkinter as tk

class pysweeper:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("750x750")
        self.root.title("PySweeper")
        self.mainFrame = tk.Frame(self.root)

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

        self.mainFrame.pack()

    def launch(self):
        self.root.mainloop()

    def clearFrame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def assignController(self, controller):
        self.controller = controller

    def createBasicGame(self, gameField, bombCount):
        cols = 20
        rows = 20
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

        for i, row in enumerate(gameField):
            # print("This is row: " + str(row))
            for k, spot in enumerate(row):
                label = tk.Label(self.gameFrame, text=spot)
                label.grid(row=i, column=k)
    
        for row in range(rows):
            for col in range(cols):
                button = tk.Button(self.gameFrame, width=1, height=1, text="", highlightbackground="gray")
                button.configure(command=lambda bn=button: bn.destroy())
                button.grid(row=row, column=col)

                # Right click/Middle click events depending on OS
                button.bind("<Button-2>", lambda event, status=False: self.__setFlag(event, status))
                button.bind("<Button-3>", lambda event, status=False: self.__setFlag(event, status))

        self.infoFrame.grid(row=0, column=0)
        self.gameFrame.grid(row=1, column=0)
        # 1 second to allow loading, 1 second to begin timer.
        # May be better to start timer on first button click in future...
        self.infoFrame.after(2000, self.__updateTimer)

    def __setFlag(self, event, status):
        if status: # If flag is set
            # unset flag
            event.widget.configure(text="")
            event.widget.bind("<Button-2>", lambda event, status=False: self.__setFlag(event, status))
            event.widget.bind("<Button-3>", lambda event, status=False: self.__setFlag(event, status))
        else: # If flag is not set
            # set flag
            event.widget.configure(text="F")
            event.widget.bind("<Button-2>", lambda event, status=True: self.__setFlag(event, status))
            event.widget.bind("<Button-3>", lambda event, status=True: self.__setFlag(event, status))

    def __updateTimer(self):
        self.controller.time += 1
        self.timer.configure(text=str(self.controller.time))
        self.infoFrame.after(1000, self.__updateTimer)


# pysweeper()
