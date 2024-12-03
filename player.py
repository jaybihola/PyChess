from turtledemo.penrose import start

from pieces import King, Queen, Bishop, Knight, Rook, Pawn

class Player():
    def __init__(self, name):
        self.name = name

    def make_move(self, start_pos, end_pos, board, piece):
        validMoves = piece.findValidMoves(start_pos, board.size)

        # check if it is pawn
        if isinstance(piece, Pawn):
            killMoves = piece.findCapturingMoves(start_pos, board.size)
            for move in killMoves:
                if not board.is_empty_pos(move):
                    validMoves.append(move)

        if end_pos in validMoves:
            board.movePiece(piece, start_pos, end_pos)
            return True

        return False

    def __str__(self):
        return f"{self.name}"

