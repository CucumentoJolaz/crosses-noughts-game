import tkinter as tk
import players as pl
from shapes import *

# основной класс приложение. В нём осуществляется инициализация холста, сетки, ячеек, игроков.
class Application(tk.Frame):
    grid: Grid

    def __init__(self, master=None):
        self.whoShouldMove = CROSS
        super().__init__(master)
        self.master = master
        self.pack()
        self.CreateWidgets()
        self.grid = Grid(self.canvas)

    def CreateWidgets(self):
        self.playerCross = tk.Button(self)
        self.playerCross["text"] = "Играть за крестики"
        self.playerCross["command"] = lambda: self.PlayersInit(CROSS)
        self.playerCross.pack(side="left")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="right")

        self.playerNoughts = tk.Button(self)
        self.playerNoughts["text"] = "Играть за нолики"
        self.playerNoughts["command"] = lambda: self.PlayersInit(NOUGHT)
        self.playerNoughts.pack(side="right")

        self.infoField = tk.Entry(width=int(CS.X / 8))
        self.infoField.pack(side="top")
        self.infoField.insert(0, 'Выберите за какую сторону вы будете играть')

        self.CanvasInit()

    def CanvasInit(self):
        if 'canvas' not in self.__dict__:
            self.canvas = tk.Canvas(self.master, width=CS.X, height=CS.Y, bg='white')
        self.canvas.create_line(1 / 3 * CS.X, 0, 1 / 3 * CS.X, CS.Y, width=5)
        self.canvas.create_line(2 / 3 * CS.X, 0, 2 / 3 * CS.X, CS.Y, width=5)
        self.canvas.create_line(0, 1 / 3 * CS.Y, CS.X, 1 / 3 * CS.Y, width=5)
        self.canvas.create_line(0, 2 / 3 * CS.Y, CS.X, 2 / 3 * CS.Y, width=5)

        # for i in range(9):
        #     self.grid.CellList[i].CellType = Cross()
        #     self.grid.CellList[i].CellType.Draw(self.canvas, self.grid.CellList[i])

        self.canvas.pack()

    def DisableStartButtons(self):
        self.playerCross['state'] = "disabled"
        self.playerNoughts['state'] = "disabled"

    def EnableStartButtons(self):
        self.playerCross['state'] = "active"
        self.playerNoughts['state'] = "active"

    def ReInit(self):

        self.whoShouldMove = CROSS
        self.canvas.delete('all')
        self.CanvasInit()
        self.grid = Grid(self.canvas)

    def PlayersInit(self, CrossOrNought: str):

        # Инициализация игрока и компьютера в соответствии с выбором игрока
        if self.whoShouldMove == END:
            self.ReInit()
        if CrossOrNought == CROSS:
            computer = pl.Computer(self, NOUGHT)
            gamer = pl.Gamer(self, CROSS, computerToPlay=computer)
            self.InfoFieldUpdate('Вы играете крестиками.')
        elif CrossOrNought == NOUGHT:
            computer = pl.Computer(self, CROSS)
            gamer = pl.Gamer(self, NOUGHT, computerToPlay=computer)
            self.InfoFieldUpdate('Вы играете ноликами')
            computer.Move()

        self.DisableStartButtons()

    def AppDelay(self, delay: int):
        self.master.after(delay)

    def InfoFieldUpdate(self, message: str):
        self.infoField.delete('0', tk.END)
        self.infoField.insert(0, message)

    def WhoShouldMove(self):
        return self.whoShouldMove

    def ShouldMove(self, shape):
        self.whoShouldMove = shape