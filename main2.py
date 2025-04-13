import numpy as np
import copy
import random

class NineMensMorris:
    def __init__(self, board_state, pieces_to_place):
        self.board = board_state
        self.pieces_to_place = pieces_to_place  # (x_pieces, o_pieces)
        
        # Define the valid positions on the board
        self.positions = [
            (0, 0), (0, 3), (0, 6),
            (1, 1), (1, 3), (1, 5),
            (2, 2), (2, 3), (2, 4),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6),
            (4, 2), (4, 3), (4, 4),
            (5, 1), (5, 3), (5, 5),
            (6, 0), (6, 3), (6, 6)
        ]
        
        # Define the mill lines
        self.mills = [
            # Horizontal mills
            [(0, 0), (0, 3), (0, 6)],
            [(1, 1), (1, 3), (1, 5)],
            [(2, 2), (2, 3), (2, 4)],
            [(3, 0), (3, 1), (3, 2)],
            [(3, 4), (3, 5), (3, 6)],
            [(4, 2), (4, 3), (4, 4)],
            [(5, 1), (5, 3), (5, 5)],
            [(6, 0), (6, 3), (6, 6)],
            
            # Vertical mills
            [(0, 0), (3, 0), (6, 0)],
            [(1, 1), (3, 1), (5, 1)],
            [(2, 2), (3, 2), (4, 2)],
            [(0, 3), (1, 3), (2, 3)],
            [(4, 3), (5, 3), (6, 3)],
            [(2, 4), (3, 4), (4, 4)],
            [(1, 5), (3, 5), (5, 5)],
            [(0, 6), (3, 6), (6, 6)]
        ]
        
        # Define adjacent positions for the movement phase
        self.adjacent = {
            (0, 0): [(0, 3), (3, 0)],
            (0, 3): [(0, 0), (0, 6), (1, 3)],
            (0, 6): [(0, 3), (3, 6)],
            (1, 1): [(1, 3), (3, 1)],
            (1, 3): [(0, 3), (1, 1), (1, 5), (2, 3)],
            (1, 5): [(1, 3), (3, 5)],
            (2, 2): [(2, 3), (3, 2)],
            (2, 3): [(1, 3), (2, 2), (2, 4), (3, 3)],
            (2, 4): [(2, 3), (3, 4)],
            (3, 0): [(0, 0), (3, 1), (6, 0)],
            (3, 1): [(1, 1), (3, 0), (3, 2), (5, 1)],
            (3, 2): [(2, 2), (3, 1), (4, 2)],
            (3, 4): [(2, 4), (3, 5), (4, 4)],
            (3, 5): [(1, 5), (3, 4), (3, 6), (5, 5)],
            (3, 6): [(0, 6), (3, 5), (6, 6)],
            (4, 2): [(3, 2), (4, 3)],
            (4, 3): [(4, 2), (4, 4), (5, 3)],
            (4, 4): [(3, 4), (4, 3)],
            (5, 1): [(3, 1), (5, 3)],
            (5, 3): [(4, 3), (5, 1), (5, 5), (6, 3)],
            (5, 5): [(3, 5), (5, 3)],
            (6, 0): [(3, 0), (6, 3)],
            (6, 3): [(5, 3), (6, 0), (6, 6)],
            (6, 6): [(3, 6), (6, 3)]
        }
        
        # Convert string board representation to 2D array
        self.board_array = self.create_board_array(board_state)
        
    def create_board_array(self, board_state):
        """Convert the flat board state to a 2D array for easier processing"""
        board_array = [['' for _ in range(7)] for _ in range(7)]
        
        for idx, pos in enumerate(self.positions):
            if idx < len(board_state) and board_state[idx] in ['x', '0', 'o']:
                # Standardize 'o' and '0' to 'o'
                piece = 'x' if board_state[idx] == 'x' else 'o'
                board_array[pos[0]][pos[1]] = piece
        
        return board_array
    
    def get_position_value(self, row, col):
        """Get the piece at a specific position or empty string if no piece"""
        if 0 <= row < 7 and 0 <= col < 7:
            return self.board_array[row][col]
        return ''
    
    def count_pieces(self):
        """Count the number of 'x' and 'o' pieces on the board"""
        x_count = sum(row.count('x') for row in self.board_array)
        o_count = sum(row.count('o') for row in self.board_array)
        return x_count, o_count
    
    def is_valid_move(self, row, col):
        """Check if a position is valid for placing a piece"""
        return (row, col) in self.positions and self.board_array[row][col] == ''
    
    def get_valid_moves(self, player='x'):
        """Get all valid moves for the current phase"""
        x_pieces_placed, o_pieces_placed = self.count_pieces()
        x_pieces_left, o_pieces_left = self.pieces_to_place
        
        # Placement phase for the player
        if (player == 'x' and x_pieces_left > 0) or (player == 'o' and o_pieces_left > 0):
            return [(row, col) for row, col in self.positions if self.is_valid_move(row, col)]
        
        # Movement phase - not implemented for this example
        # Would include code for moving pieces based on adjacency
        
        return []
    
    def check_mill(self, row, col, player):
        """Check if placing a piece at (row, col) forms a mill for the player"""
        for mill in self.mills:
            if (row, col) in mill:
                # Check if the other two positions in the mill are occupied by the player
                if all(self.get_position_value(r, c) == player for r, c in mill):
                    return True
        return False
    
    def simulate_move(self, move, player):
        """Simulate making a move and return the new board state"""
        row, col = move
        new_board = copy.deepcopy(self.board_array)
        new_board[row][col] = player
        
        # Convert back to the format needed for the result
        new_state = []
        for pos in self.positions:
            new_state.append(new_board[pos[0]][pos[1]] if new_board[pos[0]][pos[1]] in ['x', 'o'] else '')
        
        # Update pieces to place
        new_x_pieces, new_o_pieces = self.pieces_to_place
        if player == 'x':
            new_x_pieces -= 1
        else:
            new_o_pieces -= 1
            
        return new_state, (new_x_pieces, new_o_pieces)
    
    def bayesian_evaluation(self, board_array, move=None):
        """
        Bayesian evaluation of a board state
        Returns a probability of winning for 'x'
        """
        if move:
            row, col = move
            # Simulate the move
            board_array = copy.deepcopy(board_array)
            board_array[row][col] = 'x'
            
        # Feature 1: Mill formations (weight 0.4)
        x_mills = 0
        o_mills = 0
        potential_x_mills = 0
        potential_o_mills = 0
        
        for mill in self.mills:
            pieces = [board_array[r][c] for r, c in mill if 0 <= r < 7 and 0 <= c < 7]
            
            # Count actual mills
            if pieces.count('x') == 3:
                x_mills += 1
            elif pieces.count('o') == 3:
                o_mills += 1
                
            # Count potential mills (2 pieces + 1 empty)
            if pieces.count('x') == 2 and pieces.count('') == 1:
                potential_x_mills += 1
            elif pieces.count('o') == 2 and pieces.count('') == 1:
                potential_o_mills += 1
        
        # Feature 2: Piece count (weight 0.2)
        x_count = sum(row.count('x') for row in board_array)
        o_count = sum(row.count('o') for row in board_array)
        
        # Feature 3: Strategic positions (weight 0.1)
        # Center and intersection points have higher value
        strategic_positions = [(1, 1), (1, 5), (5, 1), (5, 5), (3, 3)]
        x_strategic = sum(1 for pos in strategic_positions if 
                         0 <= pos[0] < 7 and 0 <= pos[1] < 7 and board_array[pos[0]][pos[1]] == 'x')
        o_strategic = sum(1 for pos in strategic_positions if 
                         0 <= pos[0] < 7 and 0 <= pos[1] < 7 and board_array[pos[0]][pos[1]] == 'o')
        
        # Feature 4: Blocking opponent's mills (weight 0.3)
        x_blocks = 0
        o_blocks = 0
        
        for mill in self.mills:
            pieces = [board_array[r][c] for r, c in mill if 0 <= r < 7 and 0 <= c < 7]
            if pieces.count('x') == 1 and pieces.count('o') == 2:
                x_blocks += 1
            elif pieces.count('o') == 1 and pieces.count('x') == 2:
                o_blocks += 1
        
        # Calculate Bayesian probability of winning for 'x'
        # These weights represent our prior beliefs about the importance of each feature
        weights = {
            'mills': 0.4,
            'blocking': 0.3,
            'pieces': 0.2,
            'strategic': 0.1
        }
        
        # Normalize feature values between 0 and 1
        if x_mills + o_mills > 0:
            mill_score = x_mills / (x_mills + o_mills) if x_mills > o_mills else 0.5
        else:
            mill_score = 0.5
            
        if potential_x_mills + potential_o_mills > 0:
            potential_mill_score = potential_x_mills / (potential_x_mills + potential_o_mills)
        else:
            potential_mill_score = 0.5
            
        if x_count + o_count > 0:
            piece_score = x_count / (x_count + o_count)
        else:
            piece_score = 0.5
            
        if x_strategic + o_strategic > 0:
            strategic_score = x_strategic / (x_strategic + o_strategic)
        else:
            strategic_score = 0.5
            
        if x_blocks + o_blocks > 0:
            blocking_score = x_blocks / (x_blocks + o_blocks)
        else:
            blocking_score = 0.5
        
        # Combined score using weights
        mill_combined = (mill_score + potential_mill_score) / 2
        win_probability = (
            weights['mills'] * mill_combined + 
            weights['blocking'] * blocking_score + 
            weights['pieces'] * piece_score + 
            weights['strategic'] * strategic_score
        )
        
        return win_probability
    
    def bayesian_decision(self):
        """Use a Bayesian approach to decide the best move"""
        valid_moves = self.get_valid_moves()
        
        if not valid_moves:
            return None, 0.0
        
        # Evaluate each move using the Bayesian network
        move_probabilities = {}
        for move in valid_moves:
            win_probability = self.bayesian_evaluation(self.board_array, move)
            move_probabilities[move] = win_probability
        
        # Choose the move with the highest win probability
        best_move = max(move_probabilities, key=move_probabilities.get)
        best_prob = move_probabilities[best_move]
        
        return best_move, best_prob
    
    def make_best_move(self):
        """Make the best move according to the Bayesian network"""
        best_move, probability = self.bayesian_decision()
        
        if best_move:
            new_state, new_pieces = self.simulate_move(best_move, 'x')
            return new_state, new_pieces, probability, best_move
        
        return self.board, self.pieces_to_place, 0.0, None
    
    def format_board(self, board_state):
        """Format the board state for display"""
        formatted = []
        for i, piece in enumerate(board_state):
            if piece == '':
                formatted.append('""')
            else:
                formatted.append(f"'{piece}'")
        
        return "[" + ",".join(formatted) + "]"
    
    def print_clear_board(self):
        """Print a clearer representation of the board"""
        # Create an empty board with all positions marked as spaces
        clear_board = [[' ' for _ in range(7)] for _ in range(7)]
        
        # Mark valid positions with -
        for pos in self.positions:
            clear_board[pos[0]][pos[1]] = '-'
        
        # Add pieces
        for pos in self.positions:
            if self.board_array[pos[0]][pos[1]] != '':
                clear_board[pos[0]][pos[1]] = self.board_array[pos[0]][pos[1]]
        
        # Print the board with proper Nine Men's Morris layout
        print("Current Board:")
        print("  a     d     g")
        print("1 " + clear_board[0][0] + "-----" + clear_board[0][3] + "-----" + clear_board[0][6])
        print("  |     |     |")
        print("2 | " + clear_board[1][1] + "---" + clear_board[1][3] + "---" + clear_board[1][5] + " |")
        print("  | |   |   | |")
        print("3 | | " + clear_board[2][2] + "-" + clear_board[2][3] + "-" + clear_board[2][4] + " | |")
        print("  | | |   | | |")
        print("4 " + clear_board[3][0] + "-" + clear_board[3][1] + "-" + clear_board[3][2] + "   " + clear_board[3][4] + "-" + clear_board[3][5] + "-" + clear_board[3][6])
        print("  | | |   | | |")
        print("5 | | " + clear_board[4][2] + "-" + clear_board[4][3] + "-" + clear_board[4][4] + " | |")
        print("  | |   |   | |")
        print("6 | " + clear_board[5][1] + "---" + clear_board[5][3] + "---" + clear_board[5][5] + " |")
        print("  |     |     |")
        print("7 " + clear_board[6][0] + "-----" + clear_board[6][3] + "-----" + clear_board[6][6])
        print("  a  b  c  d  e  f  g")

    def opponent_move(self):
        """Simulate a move for the opponent (player 'o')"""
        valid_moves = self.get_valid_moves('o')
        
        if not valid_moves:
            return self.board, self.pieces_to_place
        
        # For this example, just choose a random valid move for the opponent
        # In a real implementation, you'd use a similar Bayesian evaluation for 'o'
        move = random.choice(valid_moves)
        
        new_state, new_pieces = self.simulate_move(move, 'o')
        return new_state, new_pieces, move

# Example game state from the problem
board_state = ["", "x", "x", "0", "x", "", "", "", "0", "x", "0", "x", "", "0", ""]
pieces_to_place = (3, 4)  # (x pieces left, o pieces left)

# Create the game
game = NineMensMorris(board_state, pieces_to_place)

# Display the initial board
print("Initial state:")
print(game.format_board(board_state))
print(f"Pieces to place: x={pieces_to_place[0]}, o={pieces_to_place[1]}")
print("\nInitial board visualization:")
game.print_clear_board()

# Make the best move for player 'x'
print("\n--- First move (player 'x') ---")
new_state, new_pieces, probability, x_move = game.make_best_move()
print(f"Player 'x' placed a piece at position {x_move}")
print("New state:")
print(game.format_board(new_state))
print(f"New pieces to place: x={new_pieces[0]}, o={new_pieces[1]}")
print(f"Win probability: {probability:.4f}")

# Update game state
game = NineMensMorris(new_state, new_pieces)
print("\nBoard after 'x' move:")
game.print_clear_board()

# Now simulate a move for player 'o'
print("\n--- Second move (player 'o') ---")
o_state, o_pieces, o_move = game.opponent_move()
print(f"Player 'o' placed a piece at position {o_move}")
print("New state after 'o' move:")
print(game.format_board(o_state))
print(f"New pieces to place: x={o_pieces[0]}, o={o_pieces[1]}")

# Update game state
game = NineMensMorris(o_state, o_pieces)
print("\nBoard after 'o' move:")
game.print_clear_board()

# Make another move for player 'x'
print("\n--- Third move (player 'x') ---")
final_state, final_pieces, final_probability, final_move = game.make_best_move()
print(f"Player 'x' placed a piece at position {final_move}")
print("Final state:")
print(game.format_board(final_state))
print(f"Final pieces to place: x={final_pieces[0]}, o={final_pieces[1]}")
print(f"Win probability: {final_probability:.4f}")

# Display final board
game = NineMensMorris(final_state, final_pieces)
print("\nFinal board:")
game.print_clear_board()