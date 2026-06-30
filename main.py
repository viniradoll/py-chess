import chess.core.board as board


def main():
    b = board.MatrixBoard()
    b.setup_starting_position()
    print(b)


if __name__ == "__main__":
    main()
