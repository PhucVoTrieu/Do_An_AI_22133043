import pygame
import sys
import time


import tictactoe as ttt


pygame.init()

size = width, height = 600, 450
hover_btn_sound = pygame.mixer.Sound("hover_btn_sound.mp3")
winning_sound = pygame.mixer.Sound("winning_sound.mp3")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.SysFont("Trebuchet MS",20,bold=True)
largeFont = pygame.font.SysFont("Trebuchet MS",40,bold=True)
moveFont = pygame.font.SysFont("Trebuchet MS",60,bold=True)

user = None
board = ttt.initial_state()
ai_turn = False

playXbtn_sound_played = False
tile_sound_played = False
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)
    
    # Let user choose a player.
    if user is None:
        # Draw backgroudn
        back_ground = pygame.image.load("tic_tac_toe_background.png")
        back_ground= pygame.transform.scale(back_ground,(width,height))
        screen.blit(back_ground,(0,0))
        
        # Draw title
        # title = largeFont.render("Play Tic-Tac-Toe", True, white)
        # titleRect = title.get_rect()
        # titleRect.center = ((width / 2), 50)
        # screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2)+130, width / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton,5,15)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2)+130, width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center 
        pygame.draw.rect(screen,white, playOButton,5,15)
        screen.blit(playO, playORect)

        
        #check if button is hovered
        mouse = pygame.mouse.get_pos()
        
        if playXButton.collidepoint(mouse):
            
            if playXbtn_sound_played == False:
                playXbtn_sound_played = True
                hover_btn_sound.play()
                
            pygame.draw.rect(screen,(255,255,150),playXButton,0,15)
            playX = mediumFont.render("Play as X", True, black)
            playXRect = playX.get_rect()
            playXRect.center = playXButton.center
            screen.blit(playX, playXRect)
        elif playOButton.collidepoint(mouse):
            pygame.draw.rect(screen,(255,255,150),playOButton,0,15)
            playO = mediumFont.render("Play as O", True, black)
            playORect = playO.get_rect()
            playORect.center = playOButton.center 
            screen.blit(playO, playORect)
        else: playXbtn_sound_played = False
        
        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O

    else:
        back_ground = pygame.image.load("game_background.png")
        back_ground= pygame.transform.scale(back_ground,(width,height))
        screen.blit(back_ground,(0,0))
        
        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),  # vi` 3x3 nen phai dich di 3/2 kich thuoc o 
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                        tile_origin[0] + j * (tile_size+5),
                        tile_origin[1] + i * (tile_size+5),
                        tile_size, tile_size
                    )
                pygame.draw.rect(screen, white, rect,3,10)
                
                if board[i][j] != ttt.EMPTY:
                    move = moveFont.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = ttt.terminal(board)
        player = ttt.current_player(board)
 
        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Your turn"
        else:
            title = f"Opponent thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and user == player and not game_over:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3): 
                        if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                            board = ttt.result(board, (i, j))
                            hover_btn_sound.play()
        # Hover effect for tiles
        for i in range(3):
            for j in range(3): 
                mouse = pygame.mouse.get_pos()
                if tiles[i][j].collidepoint(mouse):
                    rect = pygame.Rect(
                        tile_origin[0] + j * (tile_size+5),
                        tile_origin[1] + i * (tile_size+5),
                        tile_size, tile_size
                    )
                    pygame.draw.rect(screen, (255,0,0), rect,3,10)
                
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, (255,0,0))
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton,0,10)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False

    pygame.display.flip()






