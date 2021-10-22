import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass

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


# константы активно используемые в коде
CROSS = "Cross"
NOUGHT = "Nought"
EMPTY = "Empty"
END = "end"
DRAW = "Draw"


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

