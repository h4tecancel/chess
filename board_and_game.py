from soft_pieces import *
from new_pieces import Wizard, Hunter, Guardian
from for_checkers import CheckerPiece
import sys


class Board:
    """Класс, представляющий игровую доску для шахмат или шашек."""

    def __init__(self, mode="chess"):
        """
        Инициализирует доску.

        Args:
            mode (str): Режим игры. Возможные значения: 'chess', 'checkers', 'modified_chess'.
                        По умолчанию 'chess'.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.mode = mode
        self.hints = set()
        self.setup_board()

    def setup_board(self):
        """
        Настраивает начальную расстановку фигур на доске в зависимости от режима игры.

        Returns:
            None
        """
        if self.mode == "checkers":
            for i in range(8):
                for j in range(8):
                    if (i + j) % 2 == 1:
                        if i < 3:
                            self.board[i][j] = CheckerPiece('black')
                        elif i > 4:
                            self.board[i][j] = CheckerPiece('white')
        elif self.mode == "chess":
            self.board[0] = [
                Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
                King('black'), Bishop('black'), Knight('black'), Rook('black')
            ]
            self.board[1] = [Pawn('black') for _ in range(8)]
            self.board[6] = [Pawn('white') for _ in range(8)]
            self.board[7] = [
                Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
                King('white'), Bishop('white'), Knight('white'), Rook('white')
            ]
        elif self.mode == "modified_chess":
            self.board[0] = [
                Rook('black'), Knight('black'), Bishop('black'), Queen('black'),
                King('black'), Bishop('black'), Knight('black'), Rook('black')
            ]
            self.board[1] = [Pawn('black') for _ in range(8)]
            self.board[6] = [Pawn('white') for _ in range(8)]
            self.board[7] = [
                Rook('white'), Knight('white'), Bishop('white'), Queen('white'),
                King('white'), Bishop('white'), Knight('white'), Rook('white')
            ]
            self.board[0][2] = Wizard('black')
            self.board[0][5] = Hunter('black')
            self.board[7][2] = Wizard('white')
            self.board[7][5] = Hunter('white')
            self.board[0][3] = Guardian('black')
            self.board[7][3] = Guardian('white')
        else:
            raise ValueError("Invalid mode. Choose 'chess', 'checkers' or 'modified_chess'.")

    def display(self):
        """
        Отображает доску с координатами и подсказками.

        Returns:
            None
        """
        print("    a b c d e f g h")
        print("  +-----------------+")
        for i, row in enumerate(self.board):
            print(f"{8 - i} |", end=" ")
            for j, piece in enumerate(row):
                if (i, j) in self.hints:
                    print("*", end=" ")
                else:
                    print(str(piece) if piece else ".", end=" ")
            print(f"| {8 - i}")
        print("  +-----------------+")
        print("    a b c d e f g h")
        print()

    def show_hints(self, position):
        """
        Показывает доступные ходы и фигуры соперника для выбранной фигуры.

        Args:
            position (tuple): Позиция фигуры на доске в формате (x, y).

        Returns:
            None
        """
        x, y = position
        piece = self.board[x][y]
        if piece is None:
            self.hints = set()
            return
        valid_moves = piece.valid_moves(self.board, (x, y))
        self.hints = valid_moves

    def clear_hints(self):
        """
        Очищает подсказки.

        Returns:
            None
        """
        self.hints = set()


class Move:
    """Класс, представляющий ход в игре."""

    def __init__(self, start_pos, end_pos, piece, captured_piece=None):
        """
        Инициализирует ход.

        Args:
            start_pos (tuple): Начальная позиция фигуры в формате (x, y).
            end_pos (tuple): Конечная позиция фигуры в формате (x, y).
            piece: Фигура, которая была перемещена.
            captured_piece: Фигура, которая была взята (если есть).
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece = piece
        self.captured_piece = captured_piece


class ChessGame:
    """Класс, управляющий игровым процессом."""

    def __init__(self, mode="chess"):
        """
        Инициализирует игру.

        Args:
            mode (str): Режим игры. Возможные значения: 'chess', 'checkers', 'modified_chess'.
                        По умолчанию 'chess'.
        """
        self.board = Board(mode=mode)
        self.current_player = 'white'
        self.move_count = 0
        self.mode = mode
        self.move_history = []

    def play(self):
        """
        Запускает игровой цикл.

        Returns:
            None
        """
        while True:
            self.board.display()
            print(f"{self.current_player.capitalize()}'s turn")
            print(f"Move count: {self.move_count}")
            move_input = input("Enter your move (e.g., 'e2 e4' or 'undo' to revert or 'hint e2' for hints, or 'exit'): ").strip()

            if move_input.lower() == 'exit' or move_input.lower() == 'quit':
                print("Exiting the game. Goodbye!")
                sys.exit(0)

            if move_input.lower() == 'undo':
                self.undo_move()
                continue

            if move_input.lower().startswith('hint'):
                try:
                    _, pos = move_input.split()
                    x, y = self.parse_position(pos)
                    if 0 <= x < 8 and 0 <= y < 8:
                        self.board.show_hints((x, y))
                    else:
                        print("Invalid position for hint.")
                except ValueError:
                    print("Invalid hint format. Use 'hint e2'.")
                continue

            if len(move_input.split()) != 2:
                print("Invalid input. Please enter the move in the format 'e2 e4'.")
                continue

            start, end = move_input.split()
            if self.make_move(start, end):
                self.move_count += 1
                self.current_player = 'black' if self.current_player == 'white' else 'white'
                self.board.clear_hints()
            else:
                print("Invalid move, try again.")

    def make_move(self, start, end):
        """
        Выполняет ход.

        Args:
            start (str): Начальная позиция фигуры в формате 'e2'.
            end (str): Конечная позиция фигуры в формате 'e4'.

        Returns:
            bool: True, если ход выполнен успешно, иначе False.
        """
        start_x, start_y = self.parse_position(start)
        end_x, end_y = self.parse_position(end)

        if not (0 <= start_x < 8 and 0 <= start_y < 8 and 0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        piece = self.board.board[start_x][start_y]
        if piece is None or piece.color != self.current_player:
            return False

        if (end_x, end_y) not in piece.valid_moves(self.board.board, (start_x, start_y)):
            return False

        captured_piece = self.board.board[end_x][end_y]
        move = Move((start_x, start_y), (end_x, end_y), piece, captured_piece)
        self.move_history.append(move)

        self.board.board[end_x][end_y] = piece
        self.board.board[start_x][start_y] = None

        if self.mode == "checkers":
            dx = end_x - start_x
            dy = end_y - start_y
            if abs(dx) == 2:
                captured_x = start_x + dx // 2
                captured_y = start_y + dy // 2
                self.board.board[captured_x][captured_y] = None

        return True

    def undo_move(self):
        """
        Отменяет последний ход.

        Returns:
            None
        """
        if not self.move_history:
            print("No moves to undo.")
            return

        last_move = self.move_history.pop()

        start_x, start_y = last_move.start_pos
        end_x, end_y = last_move.end_pos

        self.board.board[start_x][start_y] = last_move.piece
        self.board.board[end_x][end_y] = last_move.captured_piece

        if self.mode == "checkers":
            dx = end_x - start_x
            dy = end_y - start_y
            if abs(dx) == 2:
                captured_x = start_x + dx // 2
                captured_y = start_y + dy // 2
                self.board.board[captured_x][captured_y] = last_move.captured_piece

        self.move_count -= 1
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def parse_position(self, position):
        """
        Преобразует строковую позицию (например, 'e2') в координаты (x, y).

        Args:
            position (str): Позиция на доске в формате 'e2'.

        Returns:
            tuple: Координаты (x, y). Если позиция некорректна, возвращает (-1, -1).
        """
        if len(position) != 2 or not position[0].isalpha() or not position[1].isdigit():
            return -1, -1
        x = 8 - int(position[1])
        y = ord(position[0]) - ord('a')
        return x, y