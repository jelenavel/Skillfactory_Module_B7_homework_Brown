import itertools
from random import randint
import random


class Ship:
    def __init__(self, board, orientation, size):
        self.board = board
        self.orientation = orientation
        self.size = size
        self.coordinates = []

    def plot_vertical(self, row, column):
        for i in range(self.size):
            if self.board[(row - 1) + i][column - 1] == "O":
                self.coordinates.append((row + i, column))
            else:
                raise Exception

    def plot_horizontal(self, row, column):
        for i in range(self.size):
            if self.board[row - 1][(column - 1) + i] == "O":
                self.coordinates.append((row, column + i))
            else:
                raise Exception


def is_fleet_empty(fleet):
    if len(fleet) == 0:
        return True
    return False


class Board:

    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.fleet = []
        self.neighbours = []
        self.board = [["O" for _ in range(width)] for _ in range(height)]

    def display(self):
        print(self.name)
        print("    1   2   3   4   5   6 ")
        for count, row in enumerate(self.board, 1):
            print(count, "|", " | ".join(row), "|")

    def __setitem__(self, coordinates, value):
        row, column = coordinates
        self.board[row - 1][column - 1] = value

    def __getitem__(self, coordinates):
        row, column = coordinates
        return self.board[row - 1][column - 1]

    def place_fleet(self):
        for _ in self.fleet:
            for coordinates in _:
                row, column = coordinates
                self.board[row - 1][column - 1] = u'\u2B1B'

    def list_neighbours(self):
        self.neighbours = []
        row_neighbours = []
        for i in self.fleet:
            for coordinates in i:
                row, column = coordinates
                row_neighbours.append([(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)])
        flat_neighbours = set(list(itertools.chain(*row_neighbours)))
        flat_fleet = set(list(itertools.chain(*self.fleet)))
        self.neighbours.append([item for item in flat_neighbours if item not in flat_fleet])
        self.neighbours = list(itertools.chain(*self.neighbours))
        for coordinates in self.neighbours:
            row, column = coordinates
            if row in range(1, self.height + 1) and column in range(1, self.width + 1):
                self.board[row - 1][column - 1] = "0"
            else:
                pass

    def create_ship(self, size):
        size = size
        flag = True
        while flag:
            self.display()
            try:
                print("Create your ship with %d" " deck(s)" % size)
                row = int(input("Pick a row you want to create your ship "))
                while row not in range(1, self.height + 1):
                    print("Wrong input.Try again")
                    row = int(input("Pick a row you want to create your ship "))
                else:
                    column = int(input("Pick a column you want to create your ship "))
                    while column not in range(1, self.width + 1):
                        print("Wrong input.Try again")
                        column = int(input("Pick a column you want to create your ship "))

                orientation = str(input("Choose V or H for vertical or  horizontal orientation accordingly "))
                if orientation == "v" or orientation == "h":
                    orientation = orientation
                else:
                    raise ValueError
                if orientation.lower() == "v":
                    ship = Ship(self.board, orientation, size)
                    ship.plot_vertical(row, column)
                    self.fleet.append(ship.coordinates)
                    self.place_fleet()
                    self.list_neighbours()
                    self.display()
                    print("Ship created")
                    flag = False
                elif orientation.lower() == "h":
                    ship = Ship(self.board, orientation, size)
                    ship.plot_horizontal(row, column)
                    self.fleet.append(ship.coordinates)
                    self.place_fleet()
                    self.list_neighbours()
                    self.display()
                    print("Ship created")
                    flag = False
            except ValueError:
                print("No, no, no...Type correct entrees. See rules of the game. Orientation value must be 'v' or 'h'."
                      " Row and column values should be numbers within width and height of the board.Try again")
            except IndexError:
                print("Incorrect input.Make sure your input row/column as height/width plus ship size")
            except Exception as e:
                print("Ops.Overlapping ships.")

    def create_fleet(self):
        self.create_ship(3)
        self.create_ship(2)
        self.create_ship(2)
        self.create_ship(1)
        self.create_ship(1)
        self.create_ship(1)
        self.create_ship(1)
        print("Fleet created")

    def shot(self, board):
        board = board
        board.fleet = board.fleet
        coordinates = []
        flag = True
        while flag:
            try:
                print(self.name + " shoots at " + board.name)
                print("Where are you going to shoot?")
                board.display()
                row = int(input("Pick a row you want to shoot "))
                while row not in range(1, self.height + 1):
                    print("Wrong input.Try again")
                    row = int(input("Pick a row you want to shoot "))
                else:
                    column = int(input("Pick a column you want to shoot "))
                    while column not in range(1, self.width + 1):
                        print("Wrong input.Try again")
                        column = int(input("Pick a column you want to shoot "))
                    else:
                        coordinates = row, column
                        if board.__getitem__(coordinates) == "O":
                            flag = False
                        else:
                            print("Already shot here.Try again")
            except Exception as e:
                print("Wrong input")

        if coordinates in board.fleet:
            board.__setitem__(coordinates, "X")
            board.fleet.remove(coordinates)
            print("Ship is hurt")
        elif coordinates not in board.fleet:
            board.__setitem__(coordinates, "T")
            print("Missed")

    def random_row(self):
        return randint(1, self.width)

    def random_column(self):
        return randint(1, self.height)

    def random_direction(self):
        choices = ["v", "h"]
        return random.choice(choices)

    def random_ship(self, size):
        size = size
        flag = True
        while flag:
            try:
                row = self.random_row()
                column = self.random_column()
                orientation = self.random_direction()
                if orientation.lower() == "v":
                    ship = Ship(self.board, orientation, size)
                    ship.plot_vertical(row, column)
                    self.fleet.append(ship.coordinates)
                    self.place_fleet()
                    self.list_neighbours()
                    print("Ship created")
                    flag = False
                elif orientation.lower() == "h":
                    ship = Ship(self.board, orientation, size)
                    ship.plot_horizontal(row, column)
                    self.fleet.append(ship.coordinates)
                    self.place_fleet()
                    self.list_neighbours()
                    print("Ship created")
                    flag = False
            except Exception:
                print("Ops.Overlapping ships.")

    def random_fleet(self):
        print("Computer is creating its fleet")
        self.random_ship(3)
        self.random_ship(2)
        self.random_ship(2)
        self.random_ship(1)
        self.random_ship(1)
        self.random_ship(1)
        self.random_ship(1)
        print("Fleet created")
        self.display()

    def random_shot(self, board):
        board = board
        board.fleet = board.fleet
        coordinates = []
        board.display()
        flag = True
        while flag:
            try:
                print(self.name + " shoots at " + board.name)
                print("Where are you going to shoot?")
                row = self.random_row()
                column = self.random_column()
                coordinates = row, column
                if board.__getitem__(coordinates) == "O":
                    flag = False
            except Exception as e:
                print("Already shot here.Try again")
        if coordinates in board.fleet:
            board.__setitem__(coordinates, "X")
            board.fleet.remove(coordinates)
            print("Ship is hurt")
        elif coordinates not in board.fleet:
            board.__setitem__(coordinates, "T")
            print("Missed")


player = Board("Player", 6, 6)
player.create_fleet()
player_hidden = Board("player_hidden", 6, 6)
player_hidden.fleet = player.fleet
player_hidden.fleet = list(itertools.chain(*player_hidden.fleet))
computer = Board("Computer", 6, 6)
computer.random_fleet()
computer_hidden = Board("Computer_hidden", 6, 6)
computer_hidden.fleet = computer.fleet
computer_hidden.fleet = list(itertools.chain(*computer_hidden.fleet))
while not is_fleet_empty(computer_hidden.fleet) and not is_fleet_empty(player_hidden.fleet):
    player.shot(computer_hidden)
    computer.random_shot(player_hidden)
else:
    print("we've got a winner.Game is over!!!")
