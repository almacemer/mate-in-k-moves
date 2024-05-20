import chess
import chess.svg
import time

def save_board_svg(board, id, best_move=None, size=500):
    svg =  chess.svg.board(board=board, 
                          arrows=[chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#008000")], 
                          size=size) if best_move != None else chess.svg.board(board=board, size=size)
    if board.is_checkmate() and board.turn:
       svg =  chess.svg.board(board=board,
                              check=board.king(chess.WHITE), 
                              size=size)
    elif board.is_checkmate() and not board.turn:
       svg =  chess.svg.board(board=board,
                              check=board.king(chess.BLACK), 
                              size=size)
    name = 'static/images/image' + str(id) + '.svg'
    with open(name, 'w') as f:
        f.write(svg)

def evaluate_move(board, move):
    board.push(move)
    if board.is_checkmate():
        board.pop()
        return 9999
    elif board.is_check():
        board.pop()
        return 300
    board.pop()
    if board.is_capture(move):
        return 100
    return 0

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn:
            return float(-9999)
        else:
            return float(9999)
    return 0

def order_moves(board):
  moves = list(board.legal_moves)
  return sorted(moves, key=lambda move: evaluate_move(board, move), reverse=True)

def move_ordering(board, depth, is_maximizing_player, alpha, beta):
    if depth == 0:
        return evaluate_board(board), None
    best_move = None
    if is_maximizing_player:
        best_val = float('-inf')
        ordered_moves = order_moves(board)
        for move in ordered_moves:
            board.push(move)
            eval, _ = move_ordering(board, depth-1, False, alpha, beta)
            if eval > best_val:
                best_val = eval
                best_move = move
            board.pop()
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_val, best_move
    else:
        best_val = float('inf')
        ordered_moves = order_moves(board)
        for move in ordered_moves:
            board.push(move)
            eval, _ = move_ordering(board, depth-1, True, alpha, beta)
            if eval < best_val:
                best_val = eval
                best_move = move
            board.pop()
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_val, best_move
    
def solve_checkmate(fen, k):
    print(fen)
    print(k)
    moves = []
    board = chess.Board(fen)
    max_player = True
    if not board.turn:
        max_player = False
    start = time.time()
    for i in range (k*2-1, 0, -1):
        _, best_move = move_ordering(board, i, max_player, float('-inf'), float('inf'))
        save_board_svg(board, k*2 - i, best_move)
        board.push(best_move)
        moves.append(best_move.uci())
    end = time.time()
    save_board_svg(board, k*2)
    return moves, end-start
