import pygame

pygame.init()
clock = pygame.time.Clock()
screen_size = 720
screen = pygame.display.set_mode((screen_size,screen_size))
running = True
moving = False
#number of checks
num_square = 8
square_size = screen_size // num_square
turn = 0
holding = False
movable = False

def square_center(col,row):
    x,y = square_size * col + square_size // 2, square_size * row + square_size // 2
    return int(x),int(y)
    

def piece_colrow(piece):
    row, col = piece[0] // square_size, piece[1] // square_size
    return int(row), int(col)

correct_square = False
black_pawns = []
white_pawns =[]


black_pawn_img = pygame.image.load('pawn.png').convert_alpha()
black_pawn_img = pygame.transform.scale(black_pawn_img, (50, 50))

white_pawn_img = pygame.image.load('invertedpawn.png').convert_alpha()
white_pawn_img = pygame.transform.scale(white_pawn_img, (50, 50))

for blackpawns in range(8):
    black_pawns.append(pygame.Vector2(square_center(blackpawns, 6)))
for whitepawns in range(8):
    white_pawns.append(pygame.Vector2(square_center(whitepawns, 1)))


def pawn_rules(piece, curmove, lastmove, color):
    legal_move = False
    colli = False
    if color == "black":
        color = 1
    if color == "white":
        color = -1

    for index, black in enumerate(black_pawns):
        #front collision
        if turn % 2 == 1 and int(curmove.y) == piece_colrow(black)[1] and curmove.x == piece_colrow(black)[0]:
            print(index)
            colli = True
        #diagnal takes
        if turn % 2 == 1 and int(curmove.y) == piece_colrow(black)[1] and curmove.x == piece_colrow(black)[0] and (curmove.x == last_move.x + 1 or curmove.x == lastmove.x -1) and curmove.y == lastmove.y - color:
            legal_move = True
            del black_pawns[index]
            return legal_move
    for index, white in enumerate(white_pawns):
        #front collision
        if turn % 2 == 0 and int(curmove.y) == piece_colrow(white)[1] and curmove.x == piece_colrow(white)[0]:
            print(index)
            colli = True
        #diagnal takes
        if turn % 2 == 0 and int(curmove.y) == piece_colrow(white)[1] and curmove.x == piece_colrow(white)[0] and (curmove.x == last_move.x + 1 or curmove.x == lastmove.x -1) and curmove.y == lastmove.y - color:
            legal_move = True
            del white_pawns[index]
            return legal_move

    if piece and curmove.x == lastmove.x and curmove.y == lastmove.y - color and not colli:
        legal_move = True
        return legal_move
    elif piece and curmove.x == lastmove.x and lastmove.y == 6 and curmove.y == lastmove.y - color*2 and not colli:
        legal_move = True
        return legal_move
    elif piece and curmove.x == lastmove.x and lastmove.y == 1 and curmove.y == lastmove.y - color*2 and not colli:
        legal_move = True
        return legal_move
    elif piece and curmove.x == lastmove.x and lastmove.y == 1 and curmove.y == 0 and color == 1 and not colli:
        legal_move = True
        return legal_move
    else:
        print("Please make a legal move")
        colli = False
        return legal_move

while running:
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    mouse_col = int(mouse_pos.x // square_size)
    mouse_row = int(mouse_pos.y // square_size)


    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 1 is the left mouse button, 2 is middle, 3 is right.
            if event.button == 1:
                moving = True
                if turn % 2 == 0: # if turn odd 
                    last_move = pygame.Vector2(piece_colrow(black_pawns[movable]))
                else:
                    last_move = pygame.Vector2(piece_colrow(white_pawns[movable]))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if moving:
                    moving = False
                    correct_square = False
                    holding = False
                    if turn % 2 == 0: # if turn odd 
                        next_move = pygame.Vector2(piece_colrow(black_pawns[movable]))
                        if pawn_rules(black_pawns[movable], next_move, last_move, "black"):
                            black_pawns[movable] = pygame.Vector2(square_center(next_move.x, next_move.y))
                            turn += 1
                        else:
                            black_pawns[movable] = pygame.Vector2(square_center(last_move.x,last_move.y))
                    else: # if turn even
                        next_move = pygame.Vector2(piece_colrow(white_pawns[movable]))
                        if pawn_rules(white_pawns[movable], next_move, last_move, "white"):
                            white_pawns[movable] = pygame.Vector2(square_center(next_move.x, next_move.y))
                            turn += 1
                        else:
                            white_pawns[movable] = pygame.Vector2(square_center(last_move.x,last_move.y))

    for row in range(num_square):
        for col in range(num_square):
            if (row + col) % 2 == 1:  # row + col = even
                pygame.draw.rect(screen, "white", (square_size * col, square_size * row, square_size, square_size))
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, "black", (square_size * col, square_size * row, square_size, square_size))

            for index, black in enumerate(black_pawns):
                screen.blit(black_pawn_img, (black.x - 25, black.y - 25))
                if turn % 2 == 0:  # if turn odd
                    if mouse_col == piece_colrow(black)[0] and mouse_row == piece_colrow(black)[1] and not holding:
                        correct_square = True
                        movable = index

                if correct_square and moving and turn % 2 == 0:  # if turn odd :
                    black_pawns[movable].x = mouse_pos.x
                    black_pawns[movable].y = mouse_pos.y
                    holding = True

            for index, white in enumerate(white_pawns):
                screen.blit(white_pawn_img, (white.x - 25, white.y - 25))
                if turn % 2 != 0:  # if turn even
                    if mouse_col == piece_colrow(white)[0] and mouse_row == piece_colrow(white)[1] and not holding:
                        correct_square = True
                        movable = index

                if correct_square and moving and turn % 2 != 0:  # if turn even :
                    white_pawns[movable].x = mouse_pos.x
                    white_pawns[movable].y = mouse_pos.y
                    holding = True
                    
    pygame.display.flip()

pygame.quit()