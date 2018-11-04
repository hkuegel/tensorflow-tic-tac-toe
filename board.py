import copy
import logging
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

class board(object):
    """tic tac toe board"""

    m = { -1 : "O", 0 : "_", 1 : "X"}

    def __init__(self):
        self.board = [[0,0,0], [0,0,0], [0,0,0]]
        self.side = 1

    def __eq__(self, other):
        return self.flatten() == other.flatten()
    
    def __str__(self):    
        s = ""
        for r in [0,1,2] :
            s += "   " + board.m[self.board[r][0]] + board.m[self.board[r][1]] + board.m[self.board[r][2]] + "\n"
        s += "to move: " + board.m[self.side]
        return s  

    def __copy__(self):
        cp = board()
        for r in [0,1,2] :
            for c in [0,1,2] :
                cp.board[r][c] = self.board[r][c] 
        cp.side = self.side
        return cp

    def move(self, r, c):
        if self.board[r][c] == 0:
            new_board = copy.copy(self)
            new_board.board[r][c] = self.side
            new_board.side = self.side * -1
            return new_board
        else:
            raise Exception("Invalid move.")


    def flatten(self):
        flat = [pos for row in self.board for pos in row]
        flat.append(self.side)
        return flat

    def invert_board(self):
        inverted_board = board()
        for r in [0,1,2] :
            for c in [0,1,2] :
                inverted_board.board[r][c] = self.board[r][c] * (-1)
        inverted_board.side = self.side * (-1)
        return inverted_board

    # 1 -> x wins, -1 -> 0 wins, 0.0 -> draw, None -> game not finished
    def eval(self):
        wins = []
        self.check_line(wins, 0,0 , 0,1, 0,2)
        self.check_line(wins, 1,0 , 1,1, 1,2)
        self.check_line(wins, 2,0 , 2,1, 2,2)
        self.check_line(wins, 0,0 , 1,0, 2,0)
        self.check_line(wins, 0,1 , 1,1, 2,1)
        self.check_line(wins, 0,2 , 1,2, 2,2)
        self.check_line(wins, 0,0 , 1,1, 2,2)
        self.check_line(wins, 2,0 , 1,1, 0,2)
        if len(wins) > 1 and wins[0] != wins[1]:
            raise Exception("invalid board")
        # 0 = no win, 1 = X wins, -1.0 = O wins
        if len(wins) > 0 :
            return 1.0 if wins[0] == 1 else -1.0 
        if 0 in self.flatten():
            return None
        return 0.0


    def check_line(self, wins, x1,x2,y1,y2,z1,z2) :
        if self.board[x1][x2] == self.board[y1][y2] == self.board[z1][z2] != 0:
            wins.append(self.board[x1][x2])


