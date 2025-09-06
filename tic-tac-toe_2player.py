import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 3
SQUARE_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 4

# Colors
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
O_COLOR = (0, 0, 139)
X_COLOR = (220, 20, 60)
WIN_COLOR = (0, 128, 0)
BUTTON_COLOR = (50, 150, 250)
BUTTON_HOVER = (30, 130, 230)
CELL_COLOR1 = (255, 255, 200)  # Light yellow
CELL_COLOR2 = (230, 230, 230)  # Light gray

# Fonts
pygame.font.init()
FONT = pygame.font.SysFont(None, 150)
BUTTON_FONT = pygame.font.SysFont(None, 40)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Game state
board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = "X"
winner = None
game_over = False

# Buttons
play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 60)

def draw_grid_background():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            color = CELL_COLOR1 if (row + col) % 2 == 0 else CELL_COLOR2
            pygame.draw.rect(screen, color, rect)

    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)

def draw_marks():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            mark = board[row][col]
            if mark != "":
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                color = O_COLOR if mark == "O" else X_COLOR
                text = FONT.render(mark, True, color)
                rect = text.get_rect(center=(x, y))
                screen.blit(text, rect)

def check_winner():
    for row in board:
        if row[0] != "" and row.count(row[0]) == GRID_SIZE:
            return row[0]

    for col in range(GRID_SIZE):
        col_vals = [board[row][col] for row in range(GRID_SIZE)]
        if col_vals[0] != "" and col_vals.count(col_vals[0]) == GRID_SIZE:
            return col_vals[0]

    if board[0][0] != "" and all(board[i][i] == board[0][0] for i in range(GRID_SIZE)):
        return board[0][0]
    if board[0][GRID_SIZE - 1] != "" and all(board[i][GRID_SIZE - 1 - i] == board[0][GRID_SIZE - 1] for i in range(GRID_SIZE)):
        return board[0][GRID_SIZE - 1]

    return None

def is_board_full():
    return all(board[row][col] != "" for row in range(GRID_SIZE) for col in range(GRID_SIZE))

def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=8)
    text_surf = BUTTON_FONT.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def reset_game():
    global board, current_player, winner, game_over
    board = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"
    winner = None
    game_over = False

# Main loop
running = True
while running:
    screen.fill(BG_COLOR)
    draw_grid_background()
    draw_marks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE
            if board[mouseY][mouseX] == "":
                board[mouseY][mouseX] = current_player
                winner = check_winner()
                if winner is None and not is_board_full():
                    current_player = "O" if current_player == "X" else "X"
                else:
                    game_over = True

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if play_again_button.collidepoint(event.pos):
                reset_game()
            elif quit_button.collidepoint(event.pos):
                running = False

    # Show result
    if winner:
        win_text = FONT.render(f"{winner} Wins!", True, WIN_COLOR)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    elif is_board_full() and not winner:
        draw_text = FONT.render("Draw!", True, WIN_COLOR)
        screen.blit(draw_text, draw_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

    # Draw buttons
    if game_over:
        mouse_pos = pygame.mouse.get_pos()
        draw_button(play_again_button, "Play Again", mouse_pos)
        draw_button(quit_button, "Quit", mouse_pos)

    pygame.display.update()

pygame.quit()
sys.exit()
