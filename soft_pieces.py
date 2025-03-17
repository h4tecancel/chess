class ChessPiece:
    """Базовый класс для всех шахматных фигур."""

    def __init__(self, color, symbol):
        """
        Инициализирует шахматную фигуру.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
            symbol (str): Символ, представляющий фигуру на доске.
        """
        self.color = color
        self.symbol = symbol

    def __str__(self):
        """
        Возвращает строковое представление фигуры.

        Returns:
            str: Символ фигуры.
        """
        return self.symbol

    def is_opponent(self, piece):
        """
        Проверяет, является ли фигура противником.

        Args:
            piece (ChessPiece): Фигура для проверки.

        Returns:
            bool: True, если фигура противника, иначе False.
        """
        return piece is not None and piece.color != self.color

    def is_empty(self, piece):
        """
        Проверяет, является ли клетка пустой.

        Args:
            piece (ChessPiece): Фигура для проверки.

        Returns:
            bool: True, если клетка пуста, иначе False.
        """
        return piece is None

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для фигуры.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Raises:
            NotImplementedError: Если метод не реализован в подклассе.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def moves_in_direction(self, board, position, dx, dy):
        """
        Генерирует ходы в заданном направлении (dx, dy) до конца доски или до встречи с другой фигурой.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).
            dx (int): Направление по оси X.
            dy (int): Направление по оси Y.

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        x, y = position
        moves = []
        while True:
            x += dx
            y += dy
            if not (0 <= x < 8 and 0 <= y < 8):
                break
            target = board[x][y]
            if self.is_empty(target):
                moves.append((x, y))
            elif self.is_opponent(target):
                moves.append((x, y))
                break
            else:
                break
        return moves


class Pawn(ChessPiece):
    """Класс, представляющий пешку."""

    def __init__(self, color):
        """
        Инициализирует пешку.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'P' if color == 'white' else 'p')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для пешки.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        x, y = position
        moves = []
        direction = -1 if self.color == 'white' else 1

        if 0 <= x + direction < 8 and board[x + direction][y] is None:
            moves.append((x + direction, y))

        if (x == 6 and self.color == 'white') or (x == 1 and self.color == 'black'):
            if board[x + direction][y] is None and board[x + 2 * direction][y] is None:
                moves.append((x + 2 * direction, y))

        for dy in [-1, 1]:
            if 0 <= y + dy < 8 and 0 <= x + direction < 8:
                target = board[x + direction][y + dy]
                if self.is_opponent(target):
                    moves.append((x + direction, y + dy))

        return moves


class Rook(ChessPiece):
    """Класс, представляющий ладью."""

    def __init__(self, color):
        """
        Инициализирует ладью.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'R' if color == 'white' else 'r')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для ладьи.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        moves = []
        for dx, dy in directions:
            moves.extend(self.moves_in_direction(board, position, dx, dy))
        return moves


class Knight(ChessPiece):
    """Класс, представляющий коня."""

    def __init__(self, color):
        """
        Инициализирует коня.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'N' if color == 'white' else 'n')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для коня.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        x, y = position
        moves = []

        for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if self.is_empty(target) or self.is_opponent(target):
                    moves.append((nx, ny))

        return moves


class Bishop(ChessPiece):
    """Класс, представляющий слона."""

    def __init__(self, color):
        """
        Инициализирует слона.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'B' if color == 'white' else 'b')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для слона.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        moves = []
        for dx, dy in directions:
            moves.extend(self.moves_in_direction(board, position, dx, dy))
        return moves


class Queen(ChessPiece):
    """Класс, представляющий ферзя."""

    def __init__(self, color):
        """
        Инициализирует ферзя.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'Q' if color == 'white' else 'q')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для ферзя.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        moves = []
        for dx, dy in directions:
            moves.extend(self.moves_in_direction(board, position, dx, dy))
        return moves


class King(ChessPiece):
    """Класс, представляющий короля."""

    def __init__(self, color):
        """
        Инициализирует короля.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'K' if color == 'white' else 'k')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для короля.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        x, y = position
        moves = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[nx][ny]
                    if self.is_empty(target) or self.is_opponent(target):
                        moves.append((nx, ny))

        return moves