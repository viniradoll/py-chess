# ruff: noqa
from chess.core.datatypes import Color
from chess.core.gameloop.game import Game
from chess.core.board import MatrixBoard


def main():
    g = Game(MatrixBoard())
    while True:
        print(g.turn)
        print(g.board)
        f = input()
        t = input()

def test():
    print(~Color.WHITE)

if __name__ == "__main__":
    test()
