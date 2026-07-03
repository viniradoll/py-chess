from chess.core.datatypes import Color, Square, Move
from chess.core.gameloop.game import Game
from chess.core.pieces import Piece, King, Pawn
from chess.core.board import MatrixBoard


def main():
    g = Game(MatrixBoard())
    while True:
        print(g.turn)
        print(g.board)
        f = input()
        t = input()
        try:
            g.make_move(g.turn, f, t)
        except:
            pass

def test():
    print(~Color.WHITE)

if __name__ == "__main__":
    test()
