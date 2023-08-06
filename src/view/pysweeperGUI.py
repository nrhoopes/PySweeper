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

    def createBasicGame(self):
        cols = 20
        rows = 20
        self.infoFrame = tk.Frame(self.mainFrame, highlightthickness=4, highlightbackground="gray", background="gray")
        self.gameFrame = tk.Frame(self.mainFrame, highlightthickness=4, highlightbackground="gray", background="gray")
        self.gameFrame.grid_columnconfigure(0, weight=1)

        self.flagCounter = tk.Label(self.infoFrame, text="040", background="black", foreground="red")
        self.flagCounter.grid(row=0, column=0)

        for row in range(rows):
            for col in range(cols):
                button = tk.Button(self.gameFrame, width=1, height=1, text="", highlightbackground="gray")
                button.grid(row=row, column=col)

        self.infoFrame.grid(row=0, column=0)
        self.gameFrame.grid(row=1, column=0)


# pysweeper()
