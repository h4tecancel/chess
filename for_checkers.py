from soft_pieces import ChessPiece


class CheckerPiece(ChessPiece):
    """Класс, представляющий шашку."""

    def __init__(self, color):
        """
        Инициализирует шашку.

        Args:
            color (str): Цвет шашки. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'C' if color == 'white' else 'c')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для шашки.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция шашки на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        x, y = position
        moves = []
        direction = -1 if self.color == 'white' else 1

        for dy in [-1, 1]:
            nx, ny = x + direction, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if self.is_empty(target):
                    moves.append((nx, ny))
                elif self.is_opponent(target):
                    nx2, ny2 = nx + direction, ny + dy
                    if 0 <= nx2 < 8 and 0 <= ny2 < 8 and self.is_empty(board[nx2][ny2]):
                        moves.append((nx2, ny2))

        return moves