class NineMensMorrisGame:
    def __init__(self, board_state, pieces_to_place):
        """
        Initialize the game with the given board state and pieces to place.
        
        Args:
            board_state: A list representing the current state of the board
            pieces_to_place: A tuple (nx, n0) where nx is the number of 'x' pieces to place
                            and n0 is the number of '0' pieces to place
        """
        self.board = board_state
        self.pieces_to_place = pieces_to_place
        
        self.mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [9, 10, 11], [12, 13, 14], [15, 16, 17],
            [18, 19, 20], [21, 22, 23],
            [0, 9, 21], [3, 10, 18], [6, 11, 15],
            [1, 4, 7], [16, 19, 22], [8, 12, 17],
            [5, 13, 20], [2, 14, 23]
        ]
            
        self.adjacency = {
            0: [1, 9],
            1: [0, 2, 4],
            2: [1, 14],
            3: [4, 10],
            4: [1, 3, 5, 7],
            5: [4, 13],
            6: [7, 11],
            7: [4, 6, 8],
            8: [7, 12],
            9: [0, 10, 21],
            10: [3, 9, 11, 18],
            11: [6, 10, 15],
            12: [8, 13, 17],
            13: [5, 12, 14, 20],
            14: [2, 13, 23],
            15: [11, 16],
            16: [15, 17, 19],
            17: [12, 16],
            18: [10, 19],
            19: [16, 18, 20, 22],
            20: [13, 19],
            21: [9, 22],
            22: [19, 21, 23],
            23: [14, 22]
        }

    def get_empty_positions(self):
        """Return a list of empty positions on the board."""
        return [i for i, piece in enumerate(self.board) if piece == ',']
    
    def get_player_positions(self, player):
        """Return a list of positions occupied by the given player."""
        return [i for i, piece in enumerate(self.board) if piece == player]
    
    def is_mill(self, position, player):
        """Check if placing a piece at the given position forms a mill."""
        for mill in self.mills:
            if position in mill and all(self.board[pos] == player for pos in mill):
                return True
        return False
    
    def can_move(self, position, player):
        """Check if a piece at the given position can move."""
        for adj in self.adjacency[position]:
            if self.board[adj] == ',':
                return True
        return False
    
    def get_possible_moves(self, player, opponent):
        """
        Get all possible moves for the current player.
        
        Args:
            player: The current player ('x' or '0')
            opponent: The opponent player ('0' or 'x')
            
        Returns:
            A list of possible new board states
        """
        possible_moves = []
        
        if player == 'x' and self.pieces_to_place[0] > 0 or player == '0' and self.pieces_to_place[1] > 0:
            empty_positions = self.get_empty_positions()
            
            for pos in empty_positions:
                new_board = self.board.copy()
                new_board[pos] = player
                
                new_pieces_to_place = list(self.pieces_to_place)
                if player == 'x':
                    new_pieces_to_place[0] -= 1
                else:
                    new_pieces_to_place[1] -= 1
                
                if self.is_mill(pos, player):
                    opponent_positions = self.get_player_positions(opponent)
                    for opp_pos in opponent_positions:
                        if not self.is_mill(opp_pos, opponent) or all(self.is_mill(p, opponent) for p in opponent_positions):
                            new_board_after_remove = new_board.copy()
                            new_board_after_remove[opp_pos] = ','
                            possible_moves.append((new_board_after_remove, tuple(new_pieces_to_place)))
                else:
                    possible_moves.append((new_board, tuple(new_pieces_to_place)))
        
        else:
            player_positions = self.get_player_positions(player)
            
            if len(player_positions) <= 3:
                for pos in player_positions:
                    for empty_pos in self.get_empty_positions():
                        new_board = self.board.copy()
                        new_board[pos] = ','
                        new_board[empty_pos] = player
                        
                        if self.is_mill(empty_pos, player):
                            opponent_positions = self.get_player_positions(opponent)
                            for opp_pos in opponent_positions:
                                if not self.is_mill(opp_pos, opponent) or all(self.is_mill(p, opponent) for p in opponent_positions):
                                    new_board_after_remove = new_board.copy()
                                    new_board_after_remove[opp_pos] = ','
                                    possible_moves.append((new_board_after_remove, self.pieces_to_place))
                        else:
                            possible_moves.append((new_board, self.pieces_to_place))
            else:
                for pos in player_positions:
                    for adj_pos in self.adjacency[pos]:
                        if self.board[adj_pos] == ',':
                            new_board = self.board.copy()
                            new_board[pos] = ','
                            new_board[adj_pos] = player
                            
                            if self.is_mill(adj_pos, player):
                                opponent_positions = self.get_player_positions(opponent)
                                for opp_pos in opponent_positions:
                                    if not self.is_mill(opp_pos, opponent) or all(self.is_mill(p, opponent) for p in opponent_positions):
                                        new_board_after_remove = new_board.copy()
                                        new_board_after_remove[opp_pos] = ','
                                        possible_moves.append((new_board_after_remove, self.pieces_to_place))
                            else:
                                possible_moves.append((new_board, self.pieces_to_place))
        
        return possible_moves
    
    def evaluate(self):
        """
        Heuristic evaluation function for the current board state.
        A positive value favors 'x' (MAX), a negative value favors '0' (MIN).
        """
        x_pieces = self.board.count('x')
        o_pieces = self.board.count('0')
        
        x_total = x_pieces + self.pieces_to_place[0]
        o_total = o_pieces + self.pieces_to_place[1]
        
        piece_difference = 3 * (x_pieces - o_pieces)
        
        x_mills = 0
        o_mills = 0
        counted_mills = set()
        
        for mill in self.mills:
            mill_str = ''.join(self.board[pos] for pos in mill)
            mill_key = tuple(sorted(mill))
            
            if mill_key not in counted_mills:
                if mill_str == 'xxx':
                    x_mills += 1
                    counted_mills.add(mill_key)
                elif mill_str == '000':
                    o_mills += 1
                    counted_mills.add(mill_key)
        
        mill_difference = 6 * (x_mills - o_mills)
        
        x_mobility = len(self.get_possible_moves('x', '0'))
        o_mobility = len(self.get_possible_moves('0', 'x'))
        mobility_difference = x_mobility - o_mobility
        
        x_potential_mills = self._count_potential_mills('x')
        o_potential_mills = self._count_potential_mills('0')
        potential_mills_difference = 2 * (x_potential_mills - o_potential_mills)
        
        x_blocked = sum(1 for pos in self.get_player_positions('x') if not self.can_move(pos, 'x'))
        o_blocked = sum(1 for pos in self.get_player_positions('0') if not self.can_move(pos, '0'))
        blocked_difference = o_blocked - x_blocked
        
        if o_pieces <= 2 and self.pieces_to_place[1] == 0:
            return 1000
        if x_pieces <= 2 and self.pieces_to_place[0] == 0:
            return -1000
        if o_mobility == 0 and self.pieces_to_place[1] == 0:
            return 1000
        if x_mobility == 0 and self.pieces_to_place[0] == 0:
            return -1000
        
        return piece_difference + mill_difference + mobility_difference + potential_mills_difference + blocked_difference
    
    def _count_potential_mills(self, player):
        """Count the number of potential mills that can be formed in one move."""
        potential_mills = 0
        for mill in self.mills:
            pieces = [self.board[pos] for pos in mill]
            if pieces.count(player) == 2 and pieces.count(',') == 1:
                potential_mills += 1
        return potential_mills
    
    def minimax(self, depth, alpha, beta, is_maximizing, use_alpha_beta=False):
        """
        Minimax algorithm with optional Alpha-Beta pruning.
        
        Args:
            depth: The current depth of the search tree
            alpha: The alpha value for pruning (only used if use_alpha_beta is True)
            beta: The beta value for pruning (only used if use_alpha_beta is True)
            is_maximizing: True if it's MAX's turn, False if it's MIN's turn
            use_alpha_beta: Whether to use Alpha-Beta pruning
            
        Returns:
            A tuple (best_score, best_move) where best_move is a tuple (new_board, new_pieces_to_place)
        """
        if depth == 0:
            return self.evaluate(), None
        
        if is_maximizing:
            player, opponent = 'x', '0'
            best_score = float('-inf')
        else:
            player, opponent = '0', 'x'
            best_score = float('inf')
        
        best_move = None
        possible_moves = self.get_possible_moves(player, opponent)
        
        if not possible_moves:
            return (-1000 if is_maximizing else 1000), None
        
        for move in possible_moves:
            new_board, new_pieces_to_place = move
            
            new_game = NineMensMorrisGame(new_board, new_pieces_to_place)
            
            score, _ = new_game.minimax(depth - 1, alpha, beta, not is_maximizing, use_alpha_beta)
            
            if is_maximizing and score > best_score:
                best_score = score
                best_move = move
                if use_alpha_beta:
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            elif not is_maximizing and score < best_score:
                best_score = score
                best_move = move
                if use_alpha_beta:
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        
        return best_score, best_move
    
    def get_best_move(self, algorithm, depth):
        """
        Get the best move according to the specified algorithm and depth.
        
        Args:
            algorithm: Either "MinMax" or "AlphaBeta"
            depth: The maximum search depth
            
        Returns:
            The best move as a tuple (new_board, new_pieces_to_place)
        """
        use_alpha_beta = (algorithm == "AlphaBeta")
        _, best_move = self.minimax(depth, float('-inf'), float('inf'), True, use_alpha_beta)
        return best_move
    
    def format_board(self, board):
        """Format the board for human-readable output matching the reference image."""
        symbols = []
        for i in range(24):
            if i < len(board):
                if board[i] == 'x':
                    symbols.append('x')
                elif board[i] == '0':
                    symbols.append('0')
                else:
                    symbols.append(' ')
            else:
                symbols.append(' ')
        
        formatted_board = f"""
{symbols[0]}-----------------------{symbols[1]}-----------------------{symbols[2]}
|                       |                       |
|       {symbols[3]}---------------{symbols[4]}---------------{symbols[5]}       |
|       |               |               |       |
|       |       {symbols[6]}-------{symbols[7]}-------{symbols[8]}       |       |
|       |       |               |       |       |
{symbols[9]}-------{symbols[10]}-------{symbols[11]}               {symbols[12]}-------{symbols[13]}-------{symbols[14]}
|       |       |               |       |       |
|       |       {symbols[15]}-------{symbols[16]}-------{symbols[17]}       |       |
|       |               |               |       |
|       {symbols[18]}---------------{symbols[19]}---------------{symbols[20]}       |
|                       |                       |
{symbols[21]}-----------------------{symbols[22]}-----------------------{symbols[23]}
"""
        return formatted_board


def solve_nine_mens_morris(board_state, pieces_to_place, algorithm, depth):
    """
    Solve the Nine Men's Morris game.
    
    Args:
        board_state: A list representing the current state of the board
        pieces_to_place: A tuple (nx, n0) where nx is the number of 'x' pieces to place
                        and n0 is the number of '0' pieces to place
        algorithm: Either "MinMax" or "AlphaBeta"
        depth: The maximum search depth
        
    Returns:
        The best move as a formatted board state
    """
    game = NineMensMorrisGame(board_state, pieces_to_place)
    best_move = game.get_best_move(algorithm, depth)
    
    if best_move:
        best_board, new_pieces_to_place = best_move
        formatted_board = game.format_board(best_board)
        
        x_pieces = best_board.count('x')
        o_pieces = best_board.count('0')
        
        move_info = f"""
        Algorithm: {algorithm}
        Search Depth: {depth}
        
        X pieces on board: {x_pieces}
        O pieces on board: {o_pieces}
        X pieces to place: {new_pieces_to_place[0]}
        O pieces to place: {new_pieces_to_place[1]}
        
        Board representation: {best_board}
        """
        
        return formatted_board + move_info, best_board
    else:
        return "No valid moves available", board_state


if __name__ == "__main__":
    board_state = [",", ",", ",", "", 'x', "", '0', "", 'x', 'x', '0', 'x', ",", "", '0', 'x', '0', 'x', "", '0', ""]
    pieces_to_place = (3, 4)
    algorithm = "AlphaBeta"
    depth = 3
    
    parsed_board = []
    for i in range(24):
        if i < len(board_state) and board_state[i] != "":
            parsed_board.append(board_state[i])
        else:
            parsed_board.append(",")
    
    formatted_board, best_move = solve_nine_mens_morris(parsed_board, pieces_to_place, algorithm, depth)
    
    print("Initial board:")
    print(NineMensMorrisGame(parsed_board, pieces_to_place).format_board(parsed_board))
    print("\nBest move:")
    print(formatted_board)