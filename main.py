from board_and_game import ChessGame


class GameLauncher:
    """Класс для запуска игры и взаимодействия с пользователем."""

   
    # Константы для режимов игры
    CHESS_MODE = "chess"
    CHECKERS_MODE = "checkers"
    MODIFIED_CHESS_MODE = "modified_chess"

    def __init__(self):
        """Инициализирует GameLauncher."""
        self.mode = None

    def get_game_mode(self):
        """
        Запрашивает у пользователя выбор режима игры.

        Returns:
            str: Режим игры, выбранный пользователем.
        """
        while True:
            print("Choose game mode:")
            print("1. Chess")
            print("2. Checkers")
            print("3. Modified Chess (with new pieces)")
            choice = input("Enter 1, 2, or 3: ").strip()

            if choice == "1":
                return self.CHESS_MODE
            elif choice == "2":
                return self.CHECKERS_MODE
            elif choice == "3":
                return self.MODIFIED_CHESS_MODE
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def launch_game(self):
        """Запускает игру в выбранном режиме."""
        try:
            self.mode = self.get_game_mode()
            game = ChessGame(mode=self.mode)
            print(f"Starting {self.mode.capitalize()} game. Enjoy!")
            game.play()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please restart the game.")


if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.launch_game()