from soft_pieces import ChessPiece


class Wizard(ChessPiece):
    """Класс, представляющий фигуру Волшебника."""

    def __init__(self, color):
        """
        Инициализирует Волшебника.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'W' if color == 'white' else 'w')
        self.teleport_cooldown = 0

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для Волшебника.

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

        if self.teleport_cooldown == 0:
            for i in range(8):
                for j in range(8):
                    if board[i][j] is None:
                        moves.append((i, j))
        else:
            self.teleport_cooldown -= 1

        return moves

    def teleport(self):
        """
        Активирует телепортацию и устанавливает кулдаун.

        Returns:
            None
        """
        self.teleport_cooldown = 5


class Hunter(ChessPiece):
    """Класс, представляющий фигуру Ловца."""

    def __init__(self, color):
        """
        Инициализирует Ловца.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'H' if color == 'white' else 'h')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для Ловца.

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

        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if self.is_opponent(target):
                    moves.append((nx, ny))

        return moves


class Guardian(ChessPiece):
    """Класс, представляющий фигуру Стража."""

    def __init__(self, color):
        """
        Инициализирует Стража.

        Args:
            color (str): Цвет фигуры. Возможные значения: 'white', 'black'.
        """
        super().__init__(color, 'G' if color == 'white' else 'g')

    def valid_moves(self, board, position):
        """
        Возвращает список допустимых ходов для Стража.

        Args:
            board (list): Игровая доска в виде двумерного списка.
            position (tuple): Текущая позиция фигуры на доске в формате (x, y).

        Returns:
            list: Список допустимых ходов в формате [(x1, y1), (x2, y2), ...].
        """
        x, y = position
        moves = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board[nx][ny]
                if self.is_empty(target):
                    moves.append((nx, ny))
                elif self.is_opponent(target):
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board[nx][ny]
                    if target is not None and target.color != self.color:
                        moves.append((nx, ny))

        return moves