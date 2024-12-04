import pygame as pg
from colors import Colors

class Piece():
    def __init__(self, player="none"):
        self.player = player
        self.img = None
        self.can_jump = False

    def draw(self, screen, position):
        max_size = 80
        scaled_img = pg.transform.scale(self.img, (max_size,                                                   int(self.img.get_height() * max_size / self.img.get_width())) if self.img.get_width() > self.img.get_height() else (
        int(self.img.get_width() * max_size / self.img.get_height()), max_size))
        screen.blit(scaled_img, position)

    def findValidMoves(self, current_position, board_size):
        return []

    def __str__(self):
        return f"{self.player}---{self.__class__.__name__}"


class Empty(Piece):
    def __init__(self):
        super().__init__()

class King(Piece):
    def __init__(self, player):
        super().__init__(player)
        # Load the image for the King piece
        self.img = pg.image.load(f'assets/{self.player.name}_king.png')

    def findValidMoves(self, current_position, board_size):
        x, y = current_position
        possible_moves = [
            (x + dx, y + dy)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            if (dx != 0 or dy != 0)  # exclude current position
        ]

        # Filter out moves that are out of the board bounds
        valid_moves = [
            (new_x, new_y)
            for new_x, new_y in possible_moves
            if 0 <= new_x < board_size and 0 <= new_y < board_size
        ]

        return valid_moves


class Queen(Piece):
    def __init__(self, player):
        super().__init__(player)
        # Load the image for the Queen piece
        self.img = pg.image.load(f'assets/{self.player.name}_queen.png')

    def findValidMoves(self, current_position, board_size):
        x, y = current_position
        possible_moves = []

        # Horizontal moves
        horizontal_moves_right = [(i, y) for i in range(x + 1, board_size)]  # Moves to the right are already sorted
        horizontal_moves_left = [(i, y) for i in range(x - 1, -1, -1)]  # Moves to the left sorted closest first
        possible_moves.append(('horizontal right', horizontal_moves_right))
        possible_moves.append(('horizontal left', horizontal_moves_left))

        # Vertical moves
        vertical_moves_up = [(x, i) for i in range(y - 1, -1, -1)]  # Moves up sorted closest first
        vertical_moves_down = [(x, i) for i in range(y + 1, board_size)]  # Moves down are already sorted
        possible_moves.append(('vertical up', vertical_moves_up))
        possible_moves.append(('vertical down', vertical_moves_down))

        # Diagonal moves
        diagonal_moves_1 = [(x + i, y + i) for i in range(1, board_size) if
                            x + i < board_size and y + i < board_size]  # Down-right
        diagonal_moves_2 = [(x - i, y + i) for i in range(1, board_size) if
                            x - i >= 0 and y + i < board_size]  # Up-right
        diagonal_moves_3 = [(x + i, y - i) for i in range(1, board_size) if
                            x + i < board_size and y - i >= 0]  # Down-left
        diagonal_moves_4 = [(x - i, y - i) for i in range(1, board_size) if x - i >= 0 and y - i >= 0]  # Up-left

        possible_moves.append(('diagonal down-right', diagonal_moves_1))
        possible_moves.append(('diagonal up-right', diagonal_moves_2))
        possible_moves.append(('diagonal down-left', diagonal_moves_3))
        possible_moves.append(('diagonal up-left', diagonal_moves_4))

        return possible_moves


class Bishop(Piece):
    def __init__(self, player):
        super().__init__(player)
        # Load the image for the Bishop piece
        self.img = pg.image.load(f'assets/{self.player.name}_bishop.png')

    def findValidMoves(self, current_position, board_size):
        x, y = current_position
        possible_moves = []

        # Diagonal moves
        diagonal_moves_1 = [(x + i, y + i) for i in range(1, board_size) if
                            x + i < board_size and y + i < board_size]  # Down-right
        diagonal_moves_2 = [(x - i, y + i) for i in range(1, board_size) if
                            x - i >= 0 and y + i < board_size]  # Up-right
        diagonal_moves_3 = [(x + i, y - i) for i in range(1, board_size) if
                            x + i < board_size and y - i >= 0]  # Down-left
        diagonal_moves_4 = [(x - i, y - i) for i in range(1, board_size) if x - i >= 0 and y - i >= 0]  # Up-left

        possible_moves.append(('diagonal up-right', diagonal_moves_1))
        possible_moves.append(('diagonal up-left', diagonal_moves_2))
        possible_moves.append(('diagonal down-right', diagonal_moves_3))
        possible_moves.append(('diagonal down-left', diagonal_moves_4))

        return possible_moves


class Knight(Piece):
    def __init__(self, player):
        super().__init__(player)
        # Load the image for the Knight piece
        self.img = pg.image.load(f'assets/{self.player.name}_knight.png')
        self.can_jump = True

    def findValidMoves(self, current_position, board_size):
        x, y = current_position
        possible_moves = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2)
        ]

        # Filter out moves that are out of the board bounds
        valid_moves = [
            (new_x, new_y)
            for new_x, new_y in possible_moves
            if 0 <= new_x < board_size and 0 <= new_y < board_size
        ]

        return valid_moves


class Rook(Piece):
    def __init__(self, player):
        super().__init__(player)
        # Load the image for the Rook piece
        self.img = pg.image.load(f'assets/{self.player.name}_rook.png')

    def findValidMoves(self, current_position, board_size):
        x, y = current_position
        possible_moves = []

        # Horizontal moves
        horizontal_moves_right = [(i, y) for i in range(x + 1, board_size)]  # Moves to the right are already sorted
        horizontal_moves_left = [(i, y) for i in range(x - 1, -1, -1)]  # Moves to the left sorted closest first
        possible_moves.append(('horizontal right', horizontal_moves_right))
        possible_moves.append(('horizontal left', horizontal_moves_left))

        # Vertical moves
        vertical_moves_up = [(x, i) for i in range(y - 1, -1, -1)]  # Moves up sorted closest first
        vertical_moves_down = [(x, i) for i in range(y + 1, board_size)]  # Moves down are already sorted
        possible_moves.append(('vertical up', vertical_moves_up))
        possible_moves.append(('vertical down', vertical_moves_down))

        return possible_moves


class Pawn(Piece):
    def __init__(self, player):
        super().__init__(player)
        # Load the image for the Pawn piece
        self.img = pg.image.load(f'assets/{self.player.name}_pawn.png')

    def findValidMoves(self, current_position, board_size):
        x, y = current_position
        direction = -1 if self.player.name == 'player1' else 1
        possible_moves = [(x, y + direction)]

        # Add initial two-step move
        print()
        if (self.player.name == 'player1' and y == board_size - 2) or (self.player.name == 'player2' and y == 1):
            print ("in here")
            possible_moves.append((x, y + (direction * 2)))

        valid_moves = [
            (new_x, new_y)
            for new_x, new_y in possible_moves
            if 0 <= new_x < board_size and 0 <= new_y < board_size
        ]

        valid_moves.extend(self.findCapturingMoves(current_position, board_size))

        return valid_moves

    def findCapturingMoves(self, current_position, board_size):
        x, y = current_position
        direction = -1 if self.player == 'player1' else 1
        possible_moves = [(x + direction, y - 1), (x + direction, y + 1)]

        valid_moves = [
            (new_x, new_y)
            for new_x, new_y in possible_moves
            if 0 <= new_x < board_size and 0 <= new_y < board_size
        ]

        return valid_moves


# run this file directly to test the classes display the images correctly
#
# pg.init()
# clock = pg.time.Clock()
# screen = pg.display.set_mode((800, 800))
# pg.display.set_caption('Chess Piece Test')
#
# positions = [(0, 0), (100, 0), (200, 0), (300, 0), (400, 0), (500, 0)]
#
# pieces = [
#     King('player1'),
#     Queen('player1'),
#     Bishop('player1'),
#     Knight('player1'),
#     Rook('player1'),
#     Pawn('player1')
# ]
#
# running = True
# while running:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             running = False
#
#     screen.fill(Colors.WHITE)
#
#     for piece in pieces:
#         piece.draw(screen, positions[pieces.index(piece)])
#
#     pg.display.flip()
#
#     clock.tick(60)
#
# pg.quit()
