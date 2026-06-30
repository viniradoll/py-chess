from chess.core.pieces import Piece
from chess.core.board import MatrixBoard


def main():
    b = MatrixBoard()
    b.setup_starting_position()
    for p in b:
        print(p.color)


if __name__ == "__main__":
    main()
