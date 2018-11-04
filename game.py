import copy
import board
import logging as log

class game(object):
    """a game of tic tac toe"""

    def __init__(self):
        self.moves = [board.board()]
        self.result = None

    def move(self, r, c) :
        if self.result is not None:
            raise Exception("Cannot move, game already finished.")
        new_board = self.moves[-1].move(r,c)
        self.moves.append(new_board)
        self.result = new_board.eval()

    def play(self, player1, player2):
        log.info("Starting a new game. \n\n")
        log.info("\n" + str(self.moves[-1]))
        player = player1
        while self.result is None:
            player(self)        
            log.info("\n" + str(self.moves[-1]))   
            player = player2 if player == player1 else player1
        log.info("Game finished. Result = {0}\n\n{1}".format(self.result, self.moves[-1]))
       
