import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import game
import traceback

class gui(object):
    """graphical interface for tic tac toe"""
    
    def __init__(self, ai, player_starts=True):
        self.game = game.game()
        self.player_starts = player_starts
        self.ai = ai
        

    def play(self):
        if not self.player_starts: 
            self.ai.move(self.game)
        self.draw()

    def draw_board(self, ax):
        for row in [0,1,2] :
            for col in [0,1,2]:
                x,y = col + 0.5, 2 - row + 0.5
                if self.game.moves[-1].board[row][col] == 1:
                    ax.plot(x,y ,'x',markersize=25, markeredgecolor=(0,0,0), markerfacecolor=(1,1,.8), markeredgewidth=3)
                if self.game.moves[-1].board[row][col] == -1:
                    ax.plot(x,y,'o',markersize=25, markeredgecolor=(0,0,0), markerfacecolor=(1,1,.8), markeredgewidth=3)


    def draw(self):
        plt.rcParams['toolbar'] = 'None'
        fig = plt.figure(figsize=[3,3])
        fig.patch.set_facecolor((1,1,.8))

        ax = fig.add_subplot(111)

        # draw the grid
        for x in range(4):
            ax.plot([x, x], [0,3], 'k')
        for y in range(4):
            ax.plot([0, 3], [y,y], 'k')

        # scale the axis area to fill the whole figure
        ax.set_position([0,0,1,1])

        # get rid of axes and everything (the figure background will show through)
        ax.set_axis_off()

        # scale the plot area conveniently (the board is in 0,0..2,2)
        ax.set_xlim(-1,4)
        ax.set_ylim(-1,4)

        self.draw_board(ax)
        
        def onclick(event):         
            to_move = 'x' if self.game.moves[-1].side == 1 else 'o'
            x,y = 0.5 + math.floor(event.xdata), 0.5 + math.floor(event.ydata)
            try :
                self.game.move(2 - math.floor(y),math.floor(x))
                ax.plot(x,y,to_move ,markersize=25, markeredgecolor=(0,0,0), markerfacecolor=(1,1,.8), markeredgewidth=3)
                fig.canvas.draw()
                if self.game.result is None:
                    self.ai.move(self.game)
                    self.draw_board(ax)
                    if self.game.result is not None:
                        if self.game.result == 0.0:
                            fig.suptitle("Draw!")
                        else:
                            fig.suptitle("I win. Better luck next time!")
                    fig.canvas.draw()
                else :
                    if self.game.result == 0.0:
                        fig.suptitle("Draw!")
                    else: 
                        fig.suptitle("You win. Well done!")
                    fig.canvas.draw()
            except:
                print(traceback.format_exc())
                fig.suptitle("Invalid move, try again!")
                fig.canvas.draw()
            
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        mng = plt.get_current_fig_manager()
        mng.window.resizable(False, False)
        fig.canvas.set_window_title("Tic Tac Toe")
        to_move = 'x' if self.game.moves[-1].side == 1 else 'o'
        fig.suptitle(to_move + " to move")
        plt.show()

