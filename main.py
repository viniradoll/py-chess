import chess.core.board as board

def main():
    b = board.MatrixBoard()
    b.setupStartingPosition()
    print(b)


if __name__ == "__main__":
    main()
