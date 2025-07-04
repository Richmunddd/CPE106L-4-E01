import unittest
from tic_tac_toe import TicTacToeGame

class TestTicTacToeGame(unittest.TestCase):
    
    def setUp(self):
        """Set up a new game for each test."""
        self.game = TicTacToeGame()

    def test_new_game(self):
        """Test if a new game initializes correctly."""
        game = self.game.new_game()
        self.assertEqual(game, [" "] * 9)

    def test_user_move(self):
        """Test if user can make a valid move."""
        self.game.user_move(0)
        self.assertEqual(self.game.board[0], 'X')

    def test_invalid_user_move(self):
        """Test invalid user move on an already occupied cell."""
        self.game.user_move(0)
        with self.assertRaises(ValueError):
            self.game.user_move(0)

    def test_computer_move(self):
        """Test if computer makes a valid move."""
        self.game.computer_move()
        self.assertTrue('O' in self.game.board)

    def test_winning_move(self):
        """Test if a winning move is detected."""
        self.game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertTrue(self.game._is_winning_move())

    def test_draw(self):
        """Test if the game recognizes a draw."""
        self.game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
        self.assertIsNone(self.game._is_winning_move())
        self.assertEqual(self.game.winner, 'D')

if __name__ == "__main__":
    unittest.main()
