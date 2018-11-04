import tensorflow as tf
import board
import game
import numpy as np
import logging
import os
import players
import random

class estimator(object):
    """tic tac toe position evaluator"""

    def __init__(self):
        feature_columns = [tf.feature_column.numeric_column("x", shape=[10])]
        self.estimator = tf.estimator.DNNRegressor(feature_columns=feature_columns,
            hidden_units=[50, 20], model_dir="/tmp/tic_tac_toe_estimator")
          #  ,warm_start_from="/tmp/tic_tac_toe_estimator")


    def evaluate_boards(self, some_boards) :
        boards = [ b.flatten() for b in some_boards ]
        boards = np.asarray(boards)
        labels = np.asarray([0.0 for i in some_boards])
        eval_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": boards},
            y=labels,
            num_epochs=1,
            shuffle=False)
        equity = self.estimator.predict(eval_input_fn)  
        return equity

    def evaluate(self, board) :
        equity = self.evaluate_boards([board])
        return next(equity)['predictions'][0]
        

    def learn(self, boards, scores):
        boards = [ b.flatten() for b in boards ]
        boards = np.asarray(boards)
        labels = np.asarray(scores)
        train_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": boards},
            y=labels,
            batch_size=len(scores),
            num_epochs=None,
            shuffle=True)
        self.estimator.train(input_fn=train_input_fn,steps=len(boards))

    def get_moves(self, board):
        moves = []
        for row in [0,1,2] :
            for col in [0,1,2]:
                if board.board[row][col] == 0:
                    new_board = board.move(row,col)
                    new_score = new_board.eval()
                    moves.append([ [row,col], new_board, new_score])
        return moves

    def move(self, game) :
        board = game.moves[-1]
        if board.side == -1:
            board = board.invert_board()
        best_move = None
        best_score = 100.0
        moves = self.get_moves(board)
        to_eval = []
        for coords, new_board, new_score in moves:
            if new_score is None:
                to_eval += [ b.invert_board() for _, b, s in self.get_moves(new_board) if s is None]
            else: # this is either win or forced draw
                game.move(*coords)   
                return
        equity = self.evaluate_boards(to_eval)
        for coords, new_board, new_score in moves:
            best_opponent_score = -100
            for _,_, s in self.get_moves(new_board):
                if s is None:
                    one_ahead = next(equity)['predictions'][0] *  -1
                    if one_ahead > best_opponent_score :
                        best_opponent_score = one_ahead
                else :
                    best_opponent_score = s * -100
                    break
                        
            if best_opponent_score < best_score or best_move is None:
                best_score = best_opponent_score
                best_move = coords
        game.move(*best_move)   
        logging.info("Evaluation = {0}".format(best_score))

    def randomized_move(self, game) :
        if random.randint(0,4) < 4:
            self.move(game)
        else:
            players.random_move(game)

    def assign_qscores(self, game):
        q = 0.7
        score = game.result
        scores = []
        boards = []
        for b in reversed(game.moves):
            if b.side == 1:
                boards.append(b)
            else:
                boards.append(b.invert_board())
                score *= -1
            scores.append(score)
            score *= q
        return boards,scores
    
def main(unused_argv):
    estimator = estimator()
    allboards = []
    allscores = []
    for i in range(1000):
        game = game.game()
        game.play(estimator.randomized_move, estimator.randomized_move)
        boards, scores = estimator.assign_qscores(game)
        allboards += boards
        allscores += scores
        estimator.learn(boards,scores)
        logging.info("Game {0} played and learned.".format(i))
    #estimator.learn(allboards,allscores)
        
if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)
    tf.app.run()
           
    
    
