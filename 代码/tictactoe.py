"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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


def player(board):#实现方法：计算棋盘上的X和O哪一个多，少的下一步下棋
    """
    返回下一步哪一个角色下棋
    """
    x_counter = 0
    o_counter = 0

    for row in board:
        for val in row:
            if val == "X":
                x_counter += 1
            if val == "O":
                o_counter += 1
    if x_counter == 0:
        return X
    elif x_counter > o_counter:
        return O
    elif x_counter == o_counter:
        return X


def actions(board):#计算所有可能下一步的取值
    """
    返回所有可能下一步的集合
    """
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
   返回下一步之后的面板
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise InvalidMove("Box is already filled!")
    else:
        new_board = deepcopy(board)
        new_board[i][j] = player(new_board)
        return new_board


def winner(board):
    """
    返回赢家
    """
    # 行
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O

    # 列
    for col in range(len(board[0])):
        if board[0][col] == X and board[1][col] == X and board[2][col] == X:
            return X
        if board[0][col] == O and board[1][col] == O and board[2][col] == O:
            return O

    # 斜着
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O

    #反斜线
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O

    return None


def terminal(board):
    """
    判断是否结束
    """
    if winner(board) is not None:
        return True
    else:
        empty_counter = 0
        for row in board:
            empty_counter += row.count(EMPTY)
        if empty_counter == 0:
            return True
        else:
            return False


def utility(board):
    """
    静态估值函数f的取值,X赢返回1,O赢返回-1,否则0
    """
    verdict = winner(board)
    if verdict == X:
        return 1
    elif verdict == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    返回最优下一步
    """
    if terminal(board):
        return None
        
    if player(board) == O:
        move = min_value(board)[1]
    else:
        move = max_value(board)[1]
    return move

def max_value(board):
    if terminal(board):
        return [utility(board), None]
    v = float('-inf')
    best_move = None
    for action in actions(board):
        hypothetical_value = min_value(result(board, action))[0]
        if hypothetical_value > v:
            v = hypothetical_value
            best_move = action
    return [v, best_move]


def min_value(board):
    if terminal(board):
        return [utility(board), None]
    v = float('inf')
    best_move = None
    for action in actions(board):
        hypothetical_value = max_value(result(board, action))[0]
        if hypothetical_value < v:
            v = hypothetical_value
            best_move = action
    return [v, best_move]



class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidMove(Error):
    """Exception raised for invalid move.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
