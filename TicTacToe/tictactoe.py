''' Tic-Tac-Toe Game using Pygame

This module implements a simple Tic-Tac-Toe game with a graphical interface using the Pygame library. It allows two players to take turns and play the game on the window. It also includes a single-player mode where the computer AI makes moves against the human player.

Author: Your Name

Instructions:
- Press 1 for Single player
- Press 2 for Double player
- Press spacebar to reset the game
'''

import copy
import random
import pygame

# pylint: disable=E1101
pygame.init()

dis_height = 600
dis_width = 800

board = pygame.image.load('/workspaces/TicTacToe/TicTacToe/board.jpg')
x_icon = pygame.image.load('/workspaces/TicTacToe/TicTacToe/x_icon3.png')
o_icon = pygame.image.load('/workspaces/TicTacToe/TicTacToe/o_icon.png')

display = pygame.display.set_mode((dis_width, dis_height))

pygame.display.set_caption('TikTakToe by Logan')

clock = pygame.time.Clock()

board_values = [[0,0,0], [0,0,0], [0,0,0]]

pieces_on_board = []

score_x = 0
score_o = 0
score_updated = False
move_count = 0

game_over = False

is_two_player = True

class Piece(object):
    def __init__(self, x, y, isX):
        self.x = x
        self.y = y
        self.isX = isX

        self.xTrue = self.x - (self.x % 200)
        self.yTrue = self.y - (self.y % 200) 

        if isX:
            self.image = x_icon
        else:
            self.image = o_icon
    
    def draw(self, display):
        display.blit(self.image, (self.xTrue, self.yTrue))


def redraw_game_window(score_x, score_o):
    display.blit(board, (0,0))
    pygame.draw.rect(display, (192,192,192), [600, 0, 200, 600])
    font = pygame.font.Font('/workspaces/TicTacToe/TicTacToe/Teko-Light.ttf', 50)
    instructions_font = pygame.font.Font('/workspaces/TicTacToe/TicTacToe/Teko-Light.ttf', 24)
    title = font.render('Tic-Tac-Toe', 1, (0, 153, 255))
    author = font.render('By Logan Dye', 1 , (0,153,255))
    if move_count % 2 == 0:
        turn = 'X'
    else:
        turn = 'O'
    
    instructions_txt1 = instructions_font.render('Press 1 for Single player', 1 , (0,128,128))
    instructions_txt2 = instructions_font.render('Press 2 for Double player', 1, (0,128,128))
    instructions_txt3 = instructions_font.render('Press spacebar to reset', 1, (0,128,128))
    turn_text = font.render(turn + "'s Turn", 1, (255,102,0))
    score_heading = font.render('Score', 1, (0,128,128)) 
    score_text = font.render(f'X: {str(score_x)}   O: {str(score_o)}', 1, (0,128,128))
    game_over_text = font.render('Game Over', 1, (255, 0,51))
    if game_over:
        display.blit(game_over_text, (dis_width - game_over_text.get_width() - 30, 10 + turn_text.get_height() + score_heading.get_height() + score_text.get_height() + title.get_height()))
    display.blit(title, (dis_width - title.get_width() -17, 10))
    display.blit(turn_text, (dis_width - turn_text.get_width() -45, 5 + title.get_height()))
    display.blit(score_heading, (dis_width - score_heading.get_width() - 62, turn_text.get_height()+ title.get_height()))
    display.blit(score_text, (dis_width - score_text.get_width() - 40, turn_text.get_height() + score_heading.get_height()+ title.get_height() - 20))
    display.blit(instructions_txt1, (dis_width - instructions_txt1.get_width() - 27, 50 + game_over_text.get_height() + turn_text.get_height() + score_text.get_height()+ title.get_height() + score_heading.get_height()))
    display.blit(instructions_txt2, (dis_width - instructions_txt2.get_width() - 20, 50 + game_over_text.get_height() + turn_text.get_height() + score_text.get_height()+ title.get_height() + instructions_txt1.get_height() + score_heading.get_height()))
    display.blit(instructions_txt3, (dis_width - instructions_txt3.get_width() - 27, 50 + game_over_text.get_height() + turn_text.get_height() + score_text.get_height()+ title.get_height() + instructions_txt1.get_height() + instructions_txt2.get_height() + score_heading.get_height()))


    display.blit(author, (dis_width - author.get_width() - 10, 530))



    for piece in pieces_on_board:
        piece.draw(display)

    pygame.display.update()


def is_game_over(board_values):
    zero_found = False
    for i in board_values:
        for j in i:
            if j == 0:
                zero_found = True


    if not zero_found:
        return True
    

    #Check horizontle wins
    for i in board_values:
        if i[0] == i[1] and i[0] == i[2] and i[0] != 0:
            if i[0] == 1:
                global score_x
                score_x += 1
            else:
                global score_o
                score_o += 1
            return True
    
    #Check verticle wins
    if board_values[0][0] == board_values[1][0] and board_values[0][0] == board_values[2][0] and board_values[0][0] != 0:
        if board_values[0][0] == 1:
            score_x += 1
        else:
            score_o += 1
        return True 
    
    if board_values[0][1] == board_values[1][1] and board_values[0][1] == board_values[2][1] and board_values[0][1] != 0:
        if board_values[0][1] == 1:
            score_x += 1
        else:
            score_o += 1
        
        return True
    
    if board_values[0][2] == board_values[1][2] and board_values[0][2] == board_values[2][2] and board_values[0][2] != 0:
        if board_values[0][2] == 1:
            score_x += 1
        else:
            score_o += 1
        
        return True
    
    #Check diagonal wins
    if board_values[0][0] == board_values[1][1] and board_values[0][0] == board_values[2][2] and board_values[0][0] != 0:
        if board_values[0][0] == 1:
            score_x += 1
        else:
            score_o += 1
        
        return True
    
    if board_values[0][2] == board_values[1][1] and board_values[0][2] == board_values[2][0] and board_values[0][2] != 0:
        if board_values[0][2] == 1:
            score_x += 1
        else:
            score_o += 1
        return True
    
    


    return False


def computer_move(val):

    for i in range(3):
        for j in range(3):
            board_copy = copy.deepcopy(board_values)
            if board_copy[i][j] == 0:               
                board_copy[i][j] = val
                if is_game_over(board_copy):
                    if val == -1:
                        pieces_on_board.append(Piece(j*200, i*200, False))
                    else:
                        pieces_on_board.append(Piece(j*200, i*200, True))
                    return board_copy
                
    op_val = val * -1
    for i in range(3):
        for j in range(3):
            board_copy = copy.deepcopy(board_values)
            if board_copy[i][j] == 0:
                board_copy[i][j] = op_val
                if is_game_over(board_copy):
                    if val == -1:
                        pieces_on_board.append(Piece(j*200, i*200, False))
                    else:
                        pieces_on_board.append(Piece(j*200, i*200, True))
                    board_copy[i][j] = val
                    return board_copy
    move = random_move()
    if move is not None:
        x, y = move
        board_copy = copy.deepcopy(board_values)
        board_copy[y][x] = val
        if val == -1:
            pieces_on_board.append(Piece(x*200, y*200, False)) 
        else:
            pieces_on_board.append(Piece(x*200, y*200, True))
        return board_copy
    return board_values
def random_move():
    valid_moves = []
    for i in range(3):
        for j in range(3):
            if board_values[i][j] == 0:
                valid_moves.append((j,i))
    if len(valid_moves) > 0:
        return random.choice(valid_moves)
    else:
        return None


run = True
while run:
    clock.tick(50)

    if not game_over:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        if is_two_player:
            if click != (0,0,0):
                if move_count % 2 == 0:
                    if board_values[mouse_y // 200][mouse_x // 200] == 0:
                        pieces_on_board.append(Piece(mouse_x, mouse_y, True))
                        board_values[mouse_y // 200][mouse_x // 200] = 1
                        move_count += 1
                        game_over = is_game_over(board_values)
                else:
                    if board_values[mouse_y // 200][mouse_x // 200] == 0:
                        pieces_on_board.append(Piece(mouse_x, mouse_y, False))
                        board_values[mouse_y // 200][mouse_x // 200] = -1
                        move_count += 1
                        game_over = is_game_over(board_values)


        else:
            if move_count % 2 == 0:
                if click != (0,0,0):
                    if board_values[mouse_y // 200][mouse_x // 200] == 0:
                        pieces_on_board.append(Piece(mouse_x, mouse_y, True))
                        board_values[mouse_y // 200][mouse_x // 200] = 1
                        move_count += 1
                        print(board_values)
                        game_over = is_game_over(board_values)
            else:
                board_values = computer_move(-1)
                move_count += 1
                game_over = is_game_over(board_values)
                print(board_values)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        board_values = [[0,0,0], [0,0,0], [0,0,0]]
        pieces_on_board.clear()
        move_count = 0
        game_over = False
        score_updated= False
    
    if keys[pygame.K_1]:
        is_two_player = False
    if keys[pygame.K_2]:
        is_two_player = True

    redraw_game_window(score_x, score_o)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
