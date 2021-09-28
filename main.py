import tkinter as tk
from abc import ABC, abstractmethod
from random import choice
from dataclasses import dataclass

# константы активно используемые в коде
CROSS = "Cross"
NOUGHT = "Nought"
EMPTY = "Empty"
END = "end"
DRAW = "Draw"
# наборы цифр для проверки ячеек на наличие выигрышной комбинации
WinCheckPattern = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                   (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6)]


# Размары холста
@dataclass
class CS:  # CANVAS SIZE, (X, Y)
    X = 800
    Y = 800


# координаты ячеек в холсте. Используются для обсчёта позиции курсора игрока
CellCoordinates = [[[0, 0], [1 / 3, 1 / 3]],
                   [[1 / 3, 0], [2 / 3, 1 / 3]],
                   [[2 / 3, 0], [1, 1 / 3]],
                   [[0, 1 / 3], [1 / 3, 2 / 3]],
                   [[1 / 3, 1 / 3], [2 / 3, 2 / 3]],
                   [[2 / 3, 1 / 3], [1, 2 / 3]],
                   [[0, 2 / 3], [1 / 3, 1]],
                   [[1 / 3, 2 / 3], [2 / 3, 1]],
                   [[2 / 3, 2 / 3], [1, 1]],
                   ]

for i in range(len(CellCoordinates)):
    CellCoordinates[i][0][0] *= CS.X
    CellCoordinates[i][1][0] *= CS.X
    CellCoordinates[i][0][1] *= CS.Y
    CellCoordinates[i][1][1] *= CS.Y


# класс ячейки, имеет аттрибук - характеристику ячейки, пустая, крестик или нолик. (4 класса ниже.)
# имеет собственные координаты.
class Cell:

    def __init__(self, CoordStart, CoordEnd, canvas: tk.Canvas):
        self.CellType = Empty()
        self.canvas = canvas
        self.Xstart = CoordStart[0]
        self.Ystart = CoordStart[1]
        self.Xend = CoordEnd[0]
        self.Yend = CoordEnd[1]


class Shape(ABC):
    @abstractmethod
    def Draw(self):
        pass


class Empty(Shape):
    name = EMPTY

    def Draw(self):
        print("There is no shape here")


class Cross(Shape):
    name = CROSS

    def __init__(self, cell: Cell):
        self.canvas = cell.canvas
        self.cell = cell

    def Draw(self):
        QuarterX = (self.cell.Xend - self.cell.Xstart) / 4
        QuarterY = (self.cell.Yend - self.cell.Ystart) / 4
        Line1CoordX = [i for i in
                       range(int(self.cell.Xstart + QuarterX), int(self.cell.Xstart + 3 * QuarterX),
                             int(2 * QuarterX / 100))]
        Line1CoordY = [i for i in
                       range(int(self.cell.Ystart + QuarterY), int(self.cell.Ystart + 3 * QuarterY),
                             int(2 * QuarterY / 100))]
        Line2CoordX = [i for i in
                       range(int(self.cell.Xstart + 3 * QuarterX), int(self.cell.Xstart + QuarterX),
                             -int(2 * QuarterX / 100))]
        Line2CoordY = [i for i in
                       range(int(self.cell.Ystart + QuarterY), int(self.cell.Ystart + 3 * QuarterY),
                             int(2 * QuarterY / 100))]
        # эти все усложнения просто задел под анимацию отрисовки крестиков
        for i in range(len(Line1CoordY) - 1):
            self.canvas.create_line(Line1CoordX[i], Line1CoordY[i], Line1CoordX[i + 1], Line1CoordY[i + 1], width=3)

        for i in range(len(Line2CoordX) - 2):
            self.canvas.create_line(Line2CoordX[i], Line2CoordY[i], Line2CoordX[i + 1], Line2CoordY[i + 1], width=3)


class Nought(Shape):
    name = NOUGHT

    def __init__(self, cell: Cell):
        self.canvas = cell.canvas
        self.cell = cell

    def Draw(self):
        QuarterX = (self.cell.Xend - self.cell.Xstart) / 4
        QuarterY = (self.cell.Yend - self.cell.Ystart) / 4
        self.canvas.create_oval(self.cell.Xstart + QuarterX, self.cell.Ystart + QuarterY,
                                self.cell.Xstart + 3 * QuarterX,
                                self.cell.Ystart + 3 * QuarterY, width=3)


# класс сетки. Имеет массив с классами ячеек.
class Grid:
    CellList: []

    def __init__(self, canvas: tk.Canvas):
        self.CellList = [Cell(CellCoordinates[i][0], CellCoordinates[i][1], canvas) for i in range(9)]


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
            computer = Computer(self, NOUGHT)
            gamer = Gamer(self, CROSS, computerToPlay=computer)
            self.InfoFieldUpdate('Вы играете крестиками.')
        elif CrossOrNought == NOUGHT:
            computer = Computer(self, CROSS)
            gamer = Gamer(self, NOUGHT, computerToPlay=computer)
            self.InfoFieldUpdate('Вы играете ноликами')
            computer.Move()

        self.DisableStartButtons()

    def AppDelay(self, delay: int):
        self.master.after(delay)

    def InfoFieldUpdate(self, message: str):
        self.infoField.delete('0', tk.END)
        self.infoField.insert(0, message)


# классы - игроки. используются для реализации непосредственного участия в игре.
class Player(ABC):

    def GetFreeCells(self):
        freeCells = []
        for cell in self.app.grid.CellList:
            if cell.CellType.name == "Empty":
                freeCells.append(cell)
        return freeCells

    def CheckWinningCondition(self):

        CeLi = self.app.grid.CellList  # Cell List Short

        for pat in WinCheckPattern:
            if CeLi[pat[0]].CellType.name == CeLi[pat[1]].CellType.name == CeLi[pat[2]].CellType.name:
                if CeLi[pat[0]].CellType.name == CROSS:
                    self.ProceedAfterWinningCondition(endState=CROSS)
                    return True
                elif CeLi[pat[0]].CellType.name == NOUGHT:
                    self.ProceedAfterWinningCondition(endState=NOUGHT)
                    return True

        if not self.GetFreeCells():
            self.ProceedAfterWinningCondition(endState=DRAW)
            return True

        return None

    def ProceedAfterWinningCondition(self, endState: str):
        if endState == CROSS:
            self.app.InfoFieldUpdate('Победитель - крестики! Для повторной игры выберите за какую сторону '
                                     'вы будете играть.')
        elif endState == NOUGHT:
            self.app.InfoFieldUpdate('Победитель - нолики! Для повторной игры выберите за какую сторону '
                                     'вы будете играть.')
        elif endState == DRAW:
            self.app.InfoFieldUpdate('Ничья! Для повторной игры выберите за какую сторону '
                                     'вы будете играть.')
        self.app.whoShouldMove = 'end'
        self.app.EnableStartButtons()


class Computer(Player):

    def __init__(self, app: Application, typeOfShape: str):

        assert typeOfShape in (CROSS, NOUGHT), "Неправильный тип знака. Допустимы константы CROSS и NOUGHT"
        self.typeOfShape = typeOfShape
        self.app = app
        self.canvas = self.app.canvas

    def Move(self):

        freeCells = super().GetFreeCells()

        if freeCells:
            cell = choice(freeCells)
            if self.typeOfShape == CROSS:
                cell.CellType = Cross(cell)
                self.app.whoShouldMove = NOUGHT
            elif self.typeOfShape == NOUGHT:
                cell.CellType = Nought(cell)
                self.app.whoShouldMove = CROSS
            cell.CellType.Draw()
        super().CheckWinningCondition()


class Gamer(Player):

    def __init__(self, app: Application, typeOfShape: str, computerToPlay: Computer):

        assert typeOfShape in (CROSS, NOUGHT), "Неправильный тип знака. Допустимы константы CROSS и NOUGHT"
        self.computer = computerToPlay
        self.typeOfShape = typeOfShape
        self.app = app
        self.canvas = self.app.canvas
        self.canvas.bind("<Button-1>", self.Move)

    def Move(self, event):
        '''Метод для осуществления хода живым игроком'''
        cell = self.CheckCell(event.x, event.y)

        # проверяем чей сейчас ход, проверяем свободна ли ячейка, и проставляем крестик или нолик, меняем флаг хода на противоположный
        freeCells = super().GetFreeCells()
        if freeCells:
            if self.app.whoShouldMove == self.typeOfShape:
                if cell.CellType.name == "Empty":
                    if self.typeOfShape == CROSS:
                        cell.CellType = Cross(cell)
                        self.app.whoShouldMove = NOUGHT
                    elif self.typeOfShape == NOUGHT:
                        cell.CellType = Nought(cell)
                        self.app.whoShouldMove = CROSS
                    cell.CellType.Draw()
                    if not super().CheckWinningCondition():
                        self.computer.Move()

    # метод для поиска ячейки, по которой ткнул игрок. Поиск по координатам canvas
    def CheckCell(self, x, y):

        CeLi = self.app.grid.CellList  # Cell List
        for Cell in CeLi:
            if Cell.Xstart < x < Cell.Xend and Cell.Ystart < y < Cell.Yend:
                return Cell


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
