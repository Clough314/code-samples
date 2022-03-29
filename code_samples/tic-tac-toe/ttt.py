import pygame as pg
import enum
import numpy as np
from math import pi
from copy import deepcopy


# GAME STATE

class Board:

    def __init__(self):
        self.board = np.zeros([3, 3], dtype=int)

    def play(self, row, col, mark):
        self.board[row][col] = mark

def get_winner(board):
    cs = np.sum(board, 0)
    rs = np.sum(board, 1)
    d1s = np.trace(board)
    d2s = np.trace(np.flip(board, 0))
    if np.any(cs == 3) or np.any(rs == 3) or d1s == 3 or d2s ==3:
        return 1
    elif np.any(cs == -3) or np.any(rs == -3) or d1s == -3 or d2s == -3:
        return -1
    else:
        return 0

def draw_grid(surface):
    pg.draw.line(surface, FG, (180, 0), (180, 540), 5)
    pg.draw.line(surface, FG, (360, 0), (360, 540), 5)
    pg.draw.line(surface, FG, (0, 180), (540, 180), 5)
    pg.draw.line(surface, FG, (0, 360), (540, 360), 5)
    for i in [n + 1 for n in range(8)]:
        pg.draw.line(surface, FG, (60 * i, 0), (60 * i, 540))
        pg.draw.line(surface, FG, (0, 60 * i), (540, 60 * i))

def draw_X(surface, board, cell):
    x = 180 * board[1] + 60 * cell[1] + 10
    y = 180 * board[0] + 60 * cell[0] + 10
    pg.draw.line(surface, FG, (x, y), (x + 40, y + 40), 5)
    pg.draw.line(surface, FG, (x + 40, y), (x, y + 40), 5)

def draw_O(surface, board, cell):
    pg.draw.arc(surface, FG, (
        180 * board[1] + 60 * cell[1] + 10,
        180 * board[0] + 60 * cell[0] + 10,
        40, 40), 0, 2 * pi, 5)

def draw_big_X(surface, board):
    x = 180 * board[1] + 30
    y = 180 * board[0] + 30
    pg.draw.line(surface, FG, (x, y), (x + 120, y + 120), 10)
    pg.draw.line(surface, FG, (x + 120, y), (x, y + 120), 10)

def draw_big_O(surface, board):
    pg.draw.arc(surface, FG, (
        180 * board[1] + 30,
        180 * board[0] + 30,
        120, 120), 0, 2 * pi, 10) 

def draw_mark(surface, mark, board, cell):
    if mark == 1:
        draw_X(surface, board, cell)
    elif mark == -1:
        draw_O(surface, board, cell)
    else:
        pass

def draw_big_mark(surface, mark, board):
    if mark == 1:
        draw_big_X(surface, board)
    elif mark == -1:
        draw_big_O(surface, board)
    else:
        pass


# MINIMAX

weights = np.array([[3, 2, 3], [2, 4, 2], [3, 2, 3]], dtype=int)

def legal_moves(board):
    return [(cr, cc) for cr in range(3) for cc in range(3) if not board[cr][cc]]

def heuristic(boards, board_winners):
    winner = get_winner(board_winners)
    if winner:
        return winner * 9999
    else:
        value = 0
        for board in boards.ravel():
            value += np.sum(board.board * weights)
        return value + np.sum(board_winners * weights * 10)

def minimax(boards, board_winners, depth, player, active_board, a, b):
    if depth == 0:
        return (None, heuristic(boards, board_winners))
    if player == 1:
        br, bc = active_board[0], active_board[1]
        best_value = -9999
        best_move = None
        for move in legal_moves(boards[br][bc].board):
            boards_ = deepcopy(boards)
            boards_[br][bc].board[move[0]][move[1]] = player
            board_winners_ = deepcopy(board_winners)
            board_winners_[br][bc] = get_winner(boards_[br][bc].board)
            value = minimax(boards_, board_winners_, depth - 1, player * -1, (move[0], move[1]), a, b)[1]
            if value >= best_value:
                best_value = value
                best_move = move
            if value >= b:
                break
            a = max(a, value)
        return (best_move, best_value)
    else:
        br, bc = active_board[0], active_board[1]
        best_value = 9999
        best_move = None
        for move in legal_moves(boards[br][bc].board):
            boards_ = deepcopy(boards)
            boards_[br][bc].board[move[0]][move[1]] = player
            board_winners_ = deepcopy(board_winners)
            board_winners_[br][bc] = get_winner(boards_[br][bc].board)
            value = minimax(boards_, board_winners_, depth - 1, player * -1, (move[0], move[1]), a, b)[1]
            if value <= best_value:
                best_value = value
                best_move = move
            if value <= a:
                break
            b = min(b, value)
        return (best_move, best_value)


# MAIN LOOP

pg.init()

screen = pg.display.set_mode([540, 540])

boards = np.array([
    [Board(), Board(), Board()],
    [Board(), Board(), Board()],
    [Board(), Board(), Board()]], dtype=Board)

board_winners = np.zeros([3, 3], dtype=int)

BG = (0, 0, 0)
FG = (255, 255, 255)
draw_grid(screen)
pg.display.flip()

mark = 1
active_board = None
running = True

def get_open_board(board_winners):
    for i in range(3):
        for j in range(3):
            if board_winners[i][j] == 0:
                return (i, j)

# This mostly implements game rules.
# I'd structure this much differently now; legal states should be generated
# by a Game object rather than coupled to the minimax algorithm.
while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONUP:

            pos = pg.mouse.get_pos()
            br, bc = (pos[1] // 180, pos[0] // 180)
            cr, cc = (pos[1] // 60 % 3, pos[0] // 60 % 3)
            if ((br, bc) == active_board or None == active_board) and not board_winners[br][bc]:
                boards[br][bc].play(cr, cc, mark)
                winner = get_winner(boards[br][bc].board)
                if not winner:
                    draw_mark(screen, mark, (br, bc), (cr, cc))
                else:
                    draw_big_mark(screen, mark, (br, bc))
                    board_winners[br][bc] = winner
                if not get_winner(boards[cr][cc].board):
                    active_board = (cr, cc)
                else:
                    active_board = None
                if get_winner(board_winners):
                    running = False
                    print(get_winner(board_winners))
                mark *= -1
                pg.display.flip()

                if active_board == None:
                    active_board = get_open_board(board_winners)
                move, value = minimax(boards, board_winners, 6, -1, active_board, -9999, 9999)
                br, bc = active_board
                cr, cc = move
                if ((br, bc) == active_board or None == active_board) and not board_winners[br][bc]:
                    boards[br][bc].play(cr, cc, mark)
                    winner = get_winner(boards[br][bc].board)
                    if not winner:
                        draw_mark(screen, mark, (br, bc), (cr, cc))
                    else:
                        draw_big_mark(screen, mark, (br, bc))
                        board_winners[br][bc] = winner
                    if not get_winner(boards[cr][cc].board):
                        active_board = (cr, cc)
                    else:
                        active_board = None
                    if get_winner(board_winners):
                        running = False
                        print(get_winner(board_winners))
                    mark *= -1
                    pg.display.flip()
        else:
            pass
