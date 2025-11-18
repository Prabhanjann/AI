import math

PLAYER = 'X'
OPPONENT = 'O'

def check_winner(board):
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8], 
        [0,3,6], [1,4,7], [2,5,8], 
        [0,4,8], [2,4,6]       
    ]
    for combo in win_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    return None

def is_full(board):
    return ' ' not in board

def evaluate(board):
    winner = check_winner(board)
    if winner == PLAYER:
        return 10
    elif winner == OPPONENT:
        return -10
    else:
        return 0

def get_children(board, player):
    children = []
    for i in range(9):
        if board[i] == ' ':
            new_board = board[:]
            new_board[i] = player
            children.append((new_board, i))
    return children

def alpha_beta(board, depth, alpha, beta, maximizing):
    score = evaluate(board)
    if depth == 0 or score in [10, -10] or is_full(board):
        return score

    if maximizing:
        max_eval = -math.inf
        for child, _ in get_children(board, PLAYER):
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for child, _ in get_children(board, OPPONENT):
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board):
    best_val = -math.inf
    best_move = -1
    for child, move in get_children(board, PLAYER):
        move_val = alpha_beta(child, depth=5, alpha=-math.inf, beta=math.inf, maximizing=False)
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move


if __name__ == "__main__":
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    while not is_full(board) and not check_winner(board):
        print("\nCurrent board:")
        print(f"{board[0]} | {board[1]} | {board[2]}")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print(f"{board[6]} | {board[7]} | {board[8]}")

        move = find_best_move(board)
        board[move] = PLAYER
        print(f"\nAI plays at position {move}")

        if check_winner(board) or is_full(board):
            break

        user_move = int(input("Your move (0-8): "))
        if board[user_move] == ' ':
            board[user_move] = OPPONENT
        else:
            print("Invalid move. Try again.")

    print("\nFinal board:")
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    winner = check_winner(board)
    if winner:
        print(f"Winner: {winner}")
    else:
        print("It's a draw!")