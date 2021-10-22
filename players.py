from abc import ABC, abstractmethod
from random import choice
from shapes import *

# наборы цифр для проверки ячеек на наличие выигрышной комбинации
WinCheckPattern = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                   (0, 3, 6), (1, 4, 7), (2, 5, 8),
                   (0, 4, 8), (2, 4, 6)]


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

    def __init__(self, app, typeOfShape: str):

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
                self.app.ShouldMove(NOUGHT)
            elif self.typeOfShape == NOUGHT:
                cell.CellType = Nought(cell)
                self.app.ShouldMove(CROSS)
            cell.CellType.Draw()
        super().CheckWinningCondition()


class Gamer(Player):

    def __init__(self, app, typeOfShape: str, computerToPlay: Computer):

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
