import tensorflow as tf
import estimator
import game
import logging
import os


def main(unused_argv):
    estim = estimator.estimator()
    allboards = []
    allscores = []
    for i in range(1000):
        g = game.game()
        g.play(estim.randomized_move, estim.randomized_move)
        boards, scores = estim.assign_qscores(g)
        allboards += boards
        allscores += scores
        estim.learn(boards,scores)
        logging.info("Game {0} played and learned.".format(i))
    estim.learn(allboards,allscores)
        
if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)
    tf.app.run()