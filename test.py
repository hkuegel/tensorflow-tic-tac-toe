import unittest
import estimator
import game
import players
import os
import tensorflow as tf

class TestTicTacToe(unittest.TestCase):
    
    def play(self, ai_starts, cnt) :
        res = { "win" : 0, "loss" : 0, "draw" : 0}
        esti = estimator.estimator()
        for i in range(cnt):
            g = game.game()
            if ai_starts:
                g.play(esti.move, players.random_move)
            else :
                g.play(players.random_move, esti.move)
            if g.result == 1 :
                res["win"] += 1
            elif g.result == -1 :
                res["loss"] += 1
            else :
                res["draw"] += 1
        return res

    def test_play(self):
        res_start = self.play(True, 100)
        print("Result ai vs random " + str(res_start))
        res_no_start = self.play(False, 100)
        print("Result random vs ai " + str(res_no_start))
    

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)
    unittest.main()