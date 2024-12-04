from board import ChessBoard as Board, Selection, SelectionType
from player import Player


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player("player1"), Player("player2")]
        self.board.setup_board(self.players)
        self.current_turn = self.players[0]
        self.clicks = []

    def draw_all(self, screen):
        self.board.draw(screen)

    def __handle_first_click(self, click):
        if not self.board.can_click_position(click, self.current_turn):
            return
        self.clicks.append(click)
        self.board.selections.append(Selection(click, SelectionType.SELECTEDSQUARE))
        (valid_moves, removed_moves, killing_moves) = self.board.get_valid_moves(click)
        for move in valid_moves:
            self.board.selections.append(Selection(move, SelectionType.POSSIBLEOPTION))
        for move in removed_moves:
            self.board.selections.append(Selection(move, SelectionType.IMPOSSIBLEOPTION))
        for move in killing_moves:
            self.board.selections.append(Selection(move, SelectionType.VALIDKILLINGMOVE))

    def __handle_second_click(self, click):
        self.board.selections.clear()
        first_click = self.clicks[0]
        print("first click", first_click)
        (valid_moves, _, _) = self.board.get_valid_moves(first_click)
        print("second click", click)
        print("-----------------")

        self.clicks.append(click)

        if (first_click == click):
            self.clear_clicks()
            return

        if click in valid_moves:
            self.board.selections.append(Selection(click, SelectionType.VALIDTARGET))
            self.board.move_piece(first_click, click)
            self.switch_turn()
        else:
            self.board.selections.append(Selection(click, SelectionType.INVALIDTARGET))

    def handle_clicks(self, click):
        # Two scenarios, this is the first click or it is the second click
        ## First Click Handling
        if (len(self.clicks) >= 2):
            self.clicks.clear()
            self.board.selections.clear()

        if len(self.clicks) <= 0:
            self.__handle_first_click(click)
        elif len(self.clicks) == 1:
            self.__handle_second_click(click)

    def clear_clicks(self):
        self.clicks.clear()
        self.board.selections.clear()

    def switch_turn(self):
        self.current_turn = self.players[0] if self.current_turn == self.players[1] else self.players[1]

    def play(self):
        return False

    def is_game_over(self):
        return False