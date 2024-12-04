from enum import Enum
import pygame
import string

from colors import Colors
from pieces import *

# selection type enum
class SelectionType(Enum):
    SELECTEDSQUARE = 1
    VALIDTARGET = 2
    INVALIDTARGET = 3
    POSSIBLEOPTION = 4
    IMPOSSIBLEOPTION = 5
    VALIDKILLINGMOVE = 6

class Selection:
    selection_to_color_mapping = {
        SelectionType.SELECTEDSQUARE: Colors.YELLOW,
        SelectionType.VALIDTARGET: Colors.GREEN,
        SelectionType.INVALIDTARGET: Colors.RED,
        SelectionType.POSSIBLEOPTION: Colors.BLUE,
        SelectionType.IMPOSSIBLEOPTION: Colors.PINK,
        SelectionType.VALIDKILLINGMOVE: Colors.LIGHT_RED,
    }

    def __init__(self, pos, sel_type:SelectionType):
        self.sel_type = sel_type
        self.pos = pos
        self.color = self.selection_to_color_mapping[sel_type]

class ChessBoard:
    def __init__(self, board_size=8, square_size=80, border_size=40, border_color=Colors.WHITE):
        self.board_size = board_size
        self.square_size = square_size
        self.border_size = border_size
        self.border_color = border_color
        self.board = [[Empty() for _ in range(board_size)] for _ in range(board_size)]
        self.colors = [Colors.WHITE, Colors.GRAY]
        self.select_color = Colors.YELLOW
        self.fail_color = Colors.RED
        self.selections = []

    def draw(self, screen):
        font = pygame.font.SysFont(None, 32)

        total_size = self.board_size * self.square_size + 2 * self.border_size
        pygame.draw.rect(screen, self.border_color, pygame.Rect(0, 0, total_size, total_size))

        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.colors[(row + col) % 2]
                rect = pygame.Rect(
                    self.border_size + col * self.square_size,
                    self.border_size + row * self.square_size,
                    self.square_size,
                    self.square_size
                )
                pygame.draw.rect(screen, color, rect)

                if col == 0:
                    row_label = font.render(str(self.board_size - row), True, pygame.Color('black'))
                    screen.blit(row_label, (self.border_size // 2 - row_label.get_width() // 2,
                                            self.border_size + row * self.square_size + self.square_size // 2 - row_label.get_height() // 2))

                if row == self.board_size - 1:
                    col_label = font.render(string.ascii_uppercase[col], True, pygame.Color('black'))
                    screen.blit(col_label, (
                        self.border_size + col * self.square_size + self.square_size // 2 - col_label.get_width() // 2,
                        total_size - self.border_size // 2 - col_label.get_height() // 2))

        for selection in self.selections:
            pygame.draw.rect(screen, selection.color, pygame.Rect(
                self.border_size + selection.pos[0] * self.square_size,
                self.border_size + selection.pos[1] * self.square_size,
                self.square_size,
                self.square_size
            ))

        # draw each piece by iterating through self.board
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.board[row][col]
                if not isinstance(piece, Empty):
                    position = (
                        col * self.square_size + self.square_size // 2 + (self.border_size // 2),
                        row * self.square_size + self.square_size // 2
                    )
                    piece.draw(screen, position)

    def setup_board(self, players):

        player1 = players[0]
        player2 = players[1]

        for col in range(self.board_size):
            self.board[1][col] = Pawn(player2)
            self.board[6][col] = Pawn(player1)

        # Set up rooks
        self.board[0][0] = Rook(player2)
        self.board[0][7] = Rook(player2)
        self.board[7][0] = Rook(player1)
        self.board[7][7] = Rook(player1)

        # Set up knights
        self.board[0][1] = Knight(player2)
        self.board[0][6] = Knight(player2)
        self.board[7][1] = Knight(player1)
        self.board[7][6] = Knight(player1)

        # Set up bishops
        self.board[0][2] = Bishop(player2)
        self.board[0][5] = Bishop(player2)
        self.board[7][2] = Bishop(player1)
        self.board[7][5] = Bishop(player1)

        # Set up queens
        self.board[0][3] = Queen(player2)
        self.board[7][3] = Queen(player1)

        # Set up kings
        self.board[0][4] = King(player2)
        self.board[7][4] = King(player1)

    def can_click_position(self, pos, player):
        (x, y) = pos

        entry = self.board[y][x]
        if entry == "":
            return False

        if isinstance(entry, Piece):
            if entry.player == player:
                return True

        return False

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos[1]][start_pos[0]]
        self.board[end_pos[1]][end_pos[0]] = piece
        self.board[start_pos[1]][start_pos[0]] = Empty()

    def get_piece(self, pos):
        (x, y) = pos
        return self.board[y][x]

    def get_valid_moves(self, pos):
        (x, y) = pos
        print ("clicked pos", pos)
        piece = self.board[y][x]
        print(piece)
        if isinstance(piece, Empty):
            return []
        valid_moves = piece.findValidMoves(pos, self.board_size)
        print("valid mvoes", valid_moves)
        filtered_valid_moves = []
        invalid_moves = valid_moves[:]
        killing_moves = []
        if (piece.can_jump or isinstance(piece, King)):
            print("piece can jump or is king")
            for move in valid_moves:
                (moveX, moveY) = move
                if isinstance(self.board[moveY][moveX], Empty):
                    filtered_valid_moves.append(move)
                    invalid_moves.remove(move)
                elif (self.board[moveY][moveX].player != piece.player):
                    killing_moves.append(move)
                    filtered_valid_moves.append(move)
                    invalid_moves.remove(move)
        elif (isinstance(piece, Pawn)):
            print("piece is pawn")
            invalid_moves = []
            for move in valid_moves:
                print ("analyzing move:", move)
                (moveX, moveY) = move
                isUpDown = (moveX - x) == 0
                isForward = (moveY - y) < 0 if piece.player.name == "player1" else (moveY - y) > 0
                print("is up down", isUpDown)
                print("is forward", isForward)
                if isinstance(self.board[moveY][moveX], Empty) and isUpDown and isForward:
                    filtered_valid_moves.append(move)
                elif not isinstance(self.board[moveY][moveX], Empty) and self.board[moveY][moveX].player != piece.player and isForward:
                    filtered_valid_moves.append(move)
                    killing_moves.append(move)
        else:
            print("piece is other")
            invalid_moves = [item for _, sublist in invalid_moves for item in sublist]
            for (direction, direction_moves) in valid_moves:
                for move in direction_moves:
                    (moveX, moveY) = move
                    if isinstance(self.board[moveY][moveX], Empty):
                        filtered_valid_moves.append(move)
                        invalid_moves.remove(move)
                    elif self.board[moveY][moveX].player != piece.player:
                        filtered_valid_moves.append(move)
                        invalid_moves.remove(move)
                        killing_moves.append(move)
                        break
                    else:
                        break


        print("filtered valid moves", filtered_valid_moves)
        return filtered_valid_moves, invalid_moves, killing_moves

# run main to test the board logic
def main():
    pygame.init()

    square_size = 80
    board_size = 8
    border_size = 40
    window_size = (board_size * square_size + 2 * border_size,
                   board_size * square_size + 2 * border_size)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Chess Board with Labels and Border')

    chess_board = ChessBoard(board_size, square_size, border_size, border_color=Colors.GRAY)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(Colors.BLACK)  # black background

        chess_board.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
