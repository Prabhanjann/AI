import random

# Constants
PLAYER = 'X'  # Human
AI = 'O'      # System
EMPTY = '-'

# Initialize board
def create_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]

# Display board
def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

# Check for winner
def check_winner(board):
    lines = []

    # Rows, Columns
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])

    # Diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line.count(line[0]) == 3 and line[0] != EMPTY:
            return line[0]
    return None

# Check if board is full
def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == AI:
        return 10 - depth
    elif winner == PLAYER:
        return depth - 10
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    score = minimax(board, depth + 1, False)
                    board[r][c] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER
                    score = minimax(board, depth + 1, True)
                    board[r][c] = EMPTY
                    best_score = min(score, best_score)
        return best_score

# Best move for AI
def best_move(board):
    best_score = float('-inf')
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(board, 0, False)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

# User move
def user_move(board):
    while True:
        try:
            r, c = map(int, input("Enter row and column (0-2): ").split())
            if board[r][c] == EMPTY:
                return r, c
            else:
                print("Cell already taken.")
        except:
            print("Invalid input.")

# System random move (for system vs system)
def random_move(board, symbol):
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == EMPTY]
    return random.choice(empty_cells)

# Game loop
def play_game(mode):
    board = create_board()
    print_board(board)

    current = PLAYER if mode == 'user_vs_system' else AI

    while True:
        if mode == 'user_vs_user':
            print(f"{current}'s turn")
            r, c = user_move(board)

        elif mode == 'user_vs_system':
            if current == PLAYER:
                print("Your turn")
                r, c = user_move(board)
            else:
                print("System's turn")
                r, c = best_move(board)

        elif mode == 'system_vs_system':
            print(f"{current}'s turn")
            r, c = best_move(board) if current == AI else random_move(board, PLAYER)

        board[r][c] = current
        print_board(board)

        winner = check_winner(board)
        if winner:
            print(f"{winner} wins!")
            break
        elif is_full(board):
            print("It's a draw!")
            break

        current = AI if current == PLAYER else PLAYER

# Choose mode
def main():
    print("Choose mode:")
    print("1. User vs System")
    print("2. System vs System")
    print("3. User vs User")
    choice = input("Enter choice (1-3): ")

    if choice == '1':
        play_game('user_vs_system')
    elif choice == '2':
        play_game('system_vs_system')
    elif choice == '3':
        play_game('user_vs_user')
    else:
        print("Invalid choice.")

main()