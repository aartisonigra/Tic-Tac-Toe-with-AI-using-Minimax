import pygame
import sys
import math

pygame.init()

# Constants
WIDTH = 600
HEIGHT = 700
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
FONT = pygame.font.SysFont(None, 60)

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (84, 84, 84)
BUTTON_HOVER = (100, 100, 100)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI Minimax")

# Game board
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    screen.fill(BG_COLOR)
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * 200), (WIDTH, i * 200), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * 200, 0), (i * 200, 600), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * 200 + 100), int(row * 200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + SPACE),
                                 (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + 200 - SPACE),
                                 (col * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_WIDTH)

def draw_text(text):
    label = FONT.render(text, True, TEXT_COLOR)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 610))

def draw_restart_button():
    pygame.draw.rect(screen, BUTTON_COLOR, (200, 650, 200, 40))
    label = pygame.font.SysFont(None, 40).render("Restart", True, TEXT_COLOR)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, 655))

def is_winner(player):
    for row in board:
        if row.count(player) == 3:
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

def empty_cells():
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == 0]

def minimax(board, depth, is_max):
    if is_winner(2): return 1
    if is_winner(1): return -1
    if not empty_cells(): return 0

    if is_max:
        best = -math.inf
        for (r, c) in empty_cells():
            board[r][c] = 2
            best = max(best, minimax(board, depth + 1, False))
            board[r][c] = 0
        return best
    else:
        best = math.inf
        for (r, c) in empty_cells():
            board[r][c] = 1
            best = min(best, minimax(board, depth + 1, True))
            board[r][c] = 0
        return best

def ai_move():
    best_score = -math.inf
    move = None
    for (r, c) in empty_cells():
        board[r][c] = 2
        score = minimax(board, 0, False)
        board[r][c] = 0
        if score > best_score:
            best_score = score
            move = (r, c)
    if move:
        board[move[0]][move[1]] = 2

def restart_game():
    global board, game_over, winner
    board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    winner = None
    draw_lines()
    draw_figures()

# Game state
draw_lines()
player = 1  # 1 for human, 2 for AI
game_over = False
winner = None

while True:
    draw_figures()
    if game_over and winner:
        draw_text(f"{'Player' if winner == 1 else 'AI'} Wins!")
    draw_restart_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < 600:
                mouseX = x // 200
                mouseY = y // 200
                if board[mouseY][mouseX] == 0:
                    board[mouseY][mouseX] = player
                    if is_winner(player):
                        game_over = True
                        winner = player
                    else:
                        ai_move()
                        if is_winner(2):
                            game_over = True
                            winner = 2

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 200 <= event.pos[0] <= 400 and 650 <= event.pos[1] <= 690:
                restart_game()

    pygame.display.update()
