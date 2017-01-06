# Tic Tac Toe (Noughts & Crosses)

import pygame, sys
from pygame.locals import *
import random

# Define the colours
WHITE = (255, 255, 255)
BIEGE = (239,210,141)
ORANGE = (255, 119, 0)
RED = (154,3,30)
BLUE = (0,71,119)
LIGHTBLUE = (0,175,181)

# Define constants
SCREENWIDTH = 400
SCREENHEIGHT = 300
BOXBLOCKSIZE = 70
BOARDTOP = 40
LINEWIDTH = 10
WINNINGLINEWIDTH = 5
SCOREBOARDMARGIN = 4
SCOREBOARDHEIGHT = 28

def main():
    # Setup
    pygame.init()
    game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont("Helvetica", 16)
    board_font = pygame.font.SysFont("Helvetica Bold", 72)

    # Set up empty game board and toss coin
    board = reset_board()
    coin_toss = get_coin_toss()
    player_turn = get_player_turn(coin_toss)
    heads_tails_message = True
    pieces = 0
    


    # Initialise variables
    player_score = 0
    computer_score = 0
    ties = 0
    game_won = False
    


    while True: # main game loop
        for event in pygame.event.get():
            if game_won is False:
                if player_turn is True:
                    # Player turn, get the row and column of mouse click and if valid location play a X
                    if event.type == MOUSEBUTTONUP:
                        mouse_x, mouse_y = event.pos

                        row = get_row_clicked(mouse_x, mouse_y)
                        column = get_column_clicked(mouse_x, mouse_y)

                        
                        

                        if row >=0 and column >=0:
                            if (board [row][column] == "-"):
                                board[row][column] = "X"

                                pieces = pieces + 1
                                game_won, start_line, end_line = check_winning_line(board, "X")
                                if game_won is True:
                                    player_score = player_score + 1
                                elif pieces == 9:
                                    game_won = True
                                    ties = ties + 1    
                                else:
                                    player_turn = False

                        heads_tails_message = False

            else:
                # Return key pressed when game over, reset board and toss a coin
                key_pressed = pygame.key.get_pressed()
                if key_pressed[pygame.K_RETURN]:
                    game_won = False
                    board = reset_board()
                    coin_toss = get_coin_toss()
                    player_turn = get_player_turn(coin_toss)
                    heads_tails_message = True
                    pieces = 0




        # Computer turn
        if player_turn is False and game_won is False:            
            calculate_computer_turn(board)
            pieces = pieces + 1
            game_won, start_line, end_line = check_winning_line(board, "O")
            if game_won is True:
                computer_score = computer_score + 1
            elif pieces == 9:
                game_won = True
                ties = ties + 1 
                
            else:
                player_turn = True



            
            
            

        if event.type == QUIT:
            pygame.quit()     
            sys.exit()


        # Draw screen elements
        game_screen.fill(BIEGE)
        draw_board(game_screen)
        
        for row in range(3):
            for col in range(3):
                x_o = board[row][col]
                if x_o == "X" or x_o == "O":
                    text = board_font.render(x_o, True, (BLUE))
                    text_rect = text.get_rect()
                    board_left = calculate_board_left()
                    text_rect.centerx = board_left + BOXBLOCKSIZE * (col + 1) - BOXBLOCKSIZE / 2 + LINEWIDTH * col
                    text_rect.centery = BOARDTOP + BOXBLOCKSIZE * (row + 1) - BOXBLOCKSIZE / 2 + LINEWIDTH * row
                    
                    game_screen.blit(text, text_rect)

        if game_won is True:
            draw_winning_line(game_screen, start_line, end_line)
            display_game_won_message(game_screen, score_font, player_turn, pieces)
                    
        display_scores(game_screen, score_font, player_score, computer_score, ties)

        if heads_tails_message is True:
            display_heads_tails_message(game_screen, score_font, coin_toss)

        pygame.display.update()
        clock.tick(60)





# Draw the board
def draw_board(screen):
    grid_size = calculate_grid_size()
    board_left = calculate_board_left()
    first_vertical_line_x = board_left + BOXBLOCKSIZE
    second_vertical_line_x = board_left + BOXBLOCKSIZE + LINEWIDTH + BOXBLOCKSIZE

    first_vertical_line_rect = pygame.Rect(first_vertical_line_x, BOARDTOP, LINEWIDTH, grid_size)
    pygame.draw.rect(screen, ORANGE, first_vertical_line_rect)

    second_vertical_line_rect = pygame.Rect(second_vertical_line_x, BOARDTOP, LINEWIDTH, grid_size)
    pygame.draw.rect(screen, ORANGE, second_vertical_line_rect)

    first_horizontal_line_y = BOARDTOP + BOXBLOCKSIZE
    second_vertical_line_y = BOARDTOP + BOXBLOCKSIZE + LINEWIDTH + BOXBLOCKSIZE

    first_horizontal_line_rect = pygame.Rect(board_left, first_horizontal_line_y, grid_size, LINEWIDTH)
    pygame.draw.rect(screen, ORANGE, first_horizontal_line_rect)

    second_horizontal_line_rect = pygame.Rect(board_left, second_vertical_line_y, grid_size, LINEWIDTH)
    pygame.draw.rect(screen, ORANGE, second_horizontal_line_rect)

# Calculate grid size
def calculate_grid_size():
    return BOXBLOCKSIZE * 3 + LINEWIDTH * 2

# Calculate board left
def calculate_board_left():
    grid_size = calculate_grid_size()
    return (SCREENWIDTH - grid_size) / 2

# Check column clicked
def get_column_clicked(x, y):
    board_left = calculate_board_left()

    column = -1
    
    col_1_left = board_left
    col_1_right = col_1_left + BOXBLOCKSIZE
    col_2_left = col_1_right + LINEWIDTH
    col_2_right = col_2_left + BOXBLOCKSIZE
    col_3_left = col_2_right + LINEWIDTH
    col_3_right = col_3_left + BOXBLOCKSIZE

    if x > col_1_left and x < col_1_right:
        column = 0
    elif x > col_2_left and x < col_2_right:
        column = 1
    elif x > col_3_left and x < col_3_right:
        column = 2

    return column

# Check row clicked
def get_row_clicked(x, y):

    row = -1
    
    row_1_top = BOARDTOP
    row_1_bottom = row_1_top + BOXBLOCKSIZE
    row_2_top = row_1_bottom + LINEWIDTH
    row_2_bottom = row_2_top + BOXBLOCKSIZE
    row_3_top = row_2_bottom + LINEWIDTH
    row_3_bottom = row_3_top + BOXBLOCKSIZE 

    if y > row_1_top and y <row_1_bottom:
        row = 0
    elif y > row_2_top and y <row_2_bottom:
        row = 1
    elif y > row_3_top and y <row_3_bottom:
        row = 2

    return(row)     
            
# Reset the board array
def reset_board():
    row_1 = ["-", "-", "-"]
    row_2 = ["-", "-", "-"]
    row_3 = ["-", "-", "-"]
    board = [row_1, row_2, row_3]
    return board


# Computer Turn
def calculate_computer_turn(board):
    win_move = False
    block_move = False
    middle_free = False
    

    # Check winning positions
    win_move, win_row, win_col = check_row(board, "O")

    if win_move is False:
        win_move, win_row, win_col = check_column(board, "O")

    if win_move is False:
        win_move, win_row, win_col = check_diagonal_1(board, "O")

    if win_move is False:        
         win_move, win_row, win_col = check_diagonal_2(board, "O")
    
    if win_move is True:
        board[win_row][win_col] = "O"


    # If no winning positions, check blocking positions
    if win_move is False:
        block_move, block_row, block_col = check_row(board, "X")

    if win_move is False and block_move is False:
        block_move, block_row, block_col = check_column(board, "X")

    if win_move is False and block_move is False:  
        block_move, block_row, block_col = check_diagonal_1(board, "X")

    if win_move is False and block_move is False:     
        block_move, block_row, block_col = check_diagonal_2(board, "X")

    if block_move is True:
        board[block_row][block_col] = "O"


    # If no winning positions or blocking positions, check middle is free
    if win_move is False and block_move is False:
        middle_free = check_middle(board)

    if middle_free is True:
        board[1][1] = "O"


    # If no winning positions or blocking positions or middle, pick random free space
    if win_move is False and block_move is False and middle_free is False:
        random_row, random_column = get_random_space(board)
        board[random_row][random_column] = "O"

            


# Two pieces in a row with one space available
def check_row(board, piece):
    
    
    play_row = -1
    play_col = -1
    make_move = False
    
    for row in range(3):
        if board[row] == [piece, piece, "-"]:
            play_row = row
            play_col = 2
            make_move = True
        elif board[row] == [piece, "-", piece]:
            play_row = row
            play_col = 1
            make_move = True
        elif board[row] == ["-", piece, piece]:
            play_row = row
            play_col = 0
            make_move = True

    return make_move, play_row, play_col


# Two pieces in a column with one space available
def check_column(board, piece):

    play_row = -1
    play_col = -1
    space_row = -1
    make_move = False
    
    for col in range(3):
        space_count = 0
        piece_count = 0
        for row in range(3):
            if board[row][col] == piece:
                piece_count = piece_count + 1
            elif board[row][col] == "-":
                space_count = space_count + 1
                space_row = row
                  
        if piece_count == 2 and space_count == 1:
            play_row = space_row
            play_col = col
            make_move = True
    
    return make_move, play_row, play_col


# Two pieces in a diagonal top left to bottom right with one space available
def check_diagonal_1(board, piece):
    play_row = -1
    play_col = -1
    piece_count = 0
    space_count = 0
    space_row_col = -1
    make_move = False
    
    for row_col in range(3):
        if board[row_col][row_col] == piece:
            piece_count = piece_count + 1   
        elif board[row_col][row_col] == "-":
            space_count = space_count + 1
            space_row_col = row_col

    if piece_count == 2 and space_count == 1:
        play_row = space_row_col
        play_col = space_row_col
        make_move = True

    return make_move, play_row, play_col


# Two pieces in a diagonal bottom left to top right with one space available
def check_diagonal_2(board, piece):
    play_row = -1
    play_col = -1
    piece_count = 0
    space_count = 0
    space_col = -1
    make_move = False
    
    for col in range(3):
        if board[2 - col][col] == piece:
            piece_count = piece_count + 1
        elif board[2 - col][col] == "-":
            space_count = space_count + 1
            space_col = col
                  
    if piece_count == 2 and space_count == 1:
        play_col = space_col
        play_row = 2 - space_col
        make_move = True

    return make_move, play_row, play_col


# Check if middle is free
def check_middle(board):
    middle_free = False
    
    if board[1][1] == "-":
        middle_free = True

    return middle_free


# Get random free space
def get_random_space(board):
    rand_row = random.randint(0,2)
    rand_col = random.randint(0,2)

    while (board[rand_row][rand_col] != "-"):
        rand_row = random.randint(0,2)
        rand_col = random.randint(0,2)

    return rand_row, rand_col


# Check winning line
def check_winning_line(board, piece):
    winning_line = False
    start_line = [-1, -1]
    end_line = [-1, -1]

    if board[0] == [piece, piece, piece]:
        start_line = [0, 0]
        end_line = [0, 2]
        winning_line = True
    elif board[1] == [piece, piece, piece]:
        start_line = [1, 0]
        end_line = [1, 2]
        winning_line = True
    elif board[2] == [piece, piece, piece]:
        start_line = [2, 0]
        end_line = [2, 2]
        winning_line = True
    elif board[0][0] == piece and board[1][0] == piece and board[2][0] == piece:
        start_line = [0, 0]
        end_line = [2, 0]
        winning_line = True
    elif board[0][1] == piece and board[1][1] == piece and board[2][1] == piece:
        start_line = [0, 1]
        end_line = [2, 1]
        winning_line = True
    elif board[0][2] == piece and board[1][2] == piece and board[2][2] == piece:
        start_line = [0, 2]
        end_line = [2, 2]
        winning_line = True
    elif board[0][0] == piece and board[1][1] == piece and board[2][2] == piece:
        start_line = [0, 0]
        end_line = [2, 2]
        winning_line = True
    elif board[2][0] == piece and board[1][1] == piece and board[0][2] == piece:
        start_line = [2, 0]
        end_line = [0, 2]
        winning_line = True

    return winning_line, start_line, end_line

# Draw winning line
def draw_winning_line(screen, start_line, end_line):
    board_left = calculate_board_left()

    start_x = board_left + BOXBLOCKSIZE * (start_line[1] + 1) - BOXBLOCKSIZE / 2 + LINEWIDTH * start_line[1]
    start_y = BOARDTOP + BOXBLOCKSIZE * (start_line[0] + 1) - BOXBLOCKSIZE / 2 + LINEWIDTH * start_line[0]

    end_x = board_left + BOXBLOCKSIZE * (end_line[1] + 1) - BOXBLOCKSIZE / 2 + LINEWIDTH * end_line[1]
    end_y = BOARDTOP + BOXBLOCKSIZE * (end_line[0] + 1) - BOXBLOCKSIZE / 2 + LINEWIDTH * end_line[0]

    pygame.draw.line(screen, RED, (start_x, start_y), (end_x, end_y), WINNINGLINEWIDTH)


# Display scores
def display_scores(screen, font, player, computer, ties):

    scoreboard_background_rect = (0, 0, SCREENWIDTH, SCOREBOARDHEIGHT)
    pygame.draw.rect(screen, BLUE, scoreboard_background_rect)
    
    player_text = "Player: " + str(player)
    text = font.render(player_text, True, (WHITE))
    screen.blit(text, [SCOREBOARDMARGIN, SCOREBOARDMARGIN])

    computer_text = "Computer: " + str(computer)
    text = font.render(computer_text, True, (WHITE))
    text_rect = text.get_rect()
    screen.blit(text, [SCREENWIDTH - text_rect.width - SCOREBOARDMARGIN , SCOREBOARDMARGIN])

    tie_text = "Ties: " + str(ties)
    text = font.render(tie_text, True, (WHITE))
    text_rect = text.get_rect()
    screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2 , SCOREBOARDMARGIN])


# Display result of heads or tails
def display_heads_tails_message(screen, font, heads_tails):
    if heads_tails == "Heads":
        display_text = "It's heads - player goes first"
    else:
        display_text = "It's tails - computer goes first"

    text = font.render(display_text, True, (BLUE))
    text_rect = text.get_rect()
    screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2 , SCREENHEIGHT - SCOREBOARDMARGIN - text_rect.height])


def display_game_won_message(screen, font, player_win, pieces):
    if pieces == 9:
        display_text = "Game tied - press RETURN to continue"    
    elif player_win is True:
        display_text = "PLAYER wins - press RETURN to continue"
    else:
        display_text = "COMPUTER wins - press RETURN to continue"
    
    text = font.render(display_text, True, (BLUE))
    text_rect = text.get_rect()
    screen.blit(text, [(SCREENWIDTH - text_rect.width) / 2 , SCREENHEIGHT - SCOREBOARDMARGIN - text_rect.height])
    

# Heads or tails
def get_coin_toss():
    coin_toss = random.choice(["Heads", "Tails"])

    return coin_toss

# Is it player turn, if it was heads
def get_player_turn(coin_toss_result):
    if coin_toss_result == "Heads":
        player_turn = True
    else:
        player_turn = False

    return player_turn
    
    
            
if __name__ == "__main__":
    main()
