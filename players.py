import random

def random_move(game):
    moves = []    
    for r in [0,1,2]:
        for c in [0,1,2]:
            if game.moves[-1].board[r][c] == 0:
                moves.append([r,c])
    game.move(*moves[random.randint(0, len(moves)-1)])

def player_move(game):
    correct_move = False
    while not correct_move:
        try:
            move = input("You play {0}, please enter you move (row col).\n".format( "X" if game.moves[-1].side == 1 else "O"))
            r,c = move.strip().split(" ")
            game.move(int(r),int(c))
            correct_move = True
        except:
            print("Invalid move. Try again.\n\n")
 
