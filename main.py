import game
import board
import logging
import estimator
import os
import tensorflow as tf
import gui

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)
    estimator = estimator.estimator()
    gui = gui.gui(estimator)
    gui.play()
    #game.play(estimator.move, estimator.move)
