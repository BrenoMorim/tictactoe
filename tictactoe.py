"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    count_X = 0
    count_O = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_X += 1
            elif board[i][j] == O:
                count_O += 1
    if count_X <= count_O:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.append((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = initial_state()

    for r in range(3):
        for c in range(3):
            result_board[r][c] = board[r][c]

    i, j = action[0], action[1]
    if result_board[i][j] != EMPTY:
        raise ValueError("This spot is already taken")
    
    result_board[i][j] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Check if any of the players won
    for player in [X, O]:
        
        # Check horizontally
        for i in range(3):
            won = True
            for j in range(3):
                if board[i][j] != player:
                    won = False
            if won:
                return player            

        # Check vertically
        for i in range(3):
            won = True
            for j in range(3):
                if board[j][i] != player:
                    won = False
            if won:
                return player

        # Check diagonally
        won = True
        for i in range(3):
            if board[i][i] != player:
                won = False
        if won:
            return player

        # Check reverse diagonal
        won = True
        for i in range(3):
            if board[i][2 - i] != player:
                won = False
        if won:
            return player

    # If there's no winner
    return None
    

def count_turns(board):
    """
    Helper function that returns how many times the players have made a move
    """
    turns = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != None:
                turns += 1
    return turns


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # It means the board was entirely filled
    if count_turns(board) == 9:
        return True
    elif winner(board):
        return True
    else:
        return False
    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    winner_player = winner(board)

    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Base case
    if count_turns(board) == 0:
        return (1, 1)

    if terminal(board):
        return None

    def recursive_minimax(node, depth):
        """
        Uses recursion to return the value of a state, analyzing the possible outcomes in
        depth. If it's a max player, returns the max value reachable through an action, otherwise
        returns the min value attainable (min player).
        """
        if depth == 0 or terminal(node.state):
            return utility(node.state)
        
        # Tries to maximize the score
        if player(node.state) == X:
            value = -1000
            # Gets the possible next moves
            for child_node in [Node(result(node.state, action), node, action) for action in actions(node.state)]:
                    value = max(value, recursive_minimax(child_node, depth - 1))
            return value
        
        # Tries to minimize the score
        else:
            value = 1000
            # Gets the possible next moves
            for child_node in [Node(result(node.state, action), node, action) for action in actions(node.state)]:
                    value = min(value, recursive_minimax(child_node, depth - 1))
            return value

    # The nodes containing the possible actions
    nodes = [Node(result(board, action), None, action) for action in actions(board)]
    # The value of each node
    values = [recursive_minimax(node, 9) for node in nodes]
    
    # Max player
    if player(board) == X:
        index = values.index(max(values))
    # Min player
    else:
        index = values.index(min(values))

    # Gets what action was the first to be taken, starting from the current state,
    # in order to generate the desirable outcome
    node = nodes[index]
    while node.parent != None:
        node = node.parent
    return node.action
     
# Node class, just like the one used for the last project

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
