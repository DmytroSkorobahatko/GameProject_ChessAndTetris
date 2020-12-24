import pygame, sys
import ChessEngine
from Tetris import startGame

# https://www.youtube.com/watch?v=EnYui0e73Rs

WIDTH = HEIGHT = 512
DIMENSION = 8  # 8 x 8 - common in chess
SQ_SIZE = HEIGHT // DIMENSION
FPS = 30
IMAGES = {}
COLORS = [(255, 255, 255), (200, 200, 200)]


def LoadImages():
    pieces = ["bp", "bR", "bN", "bB", "bK", "bQ", "wp", "wR", "wN", "wB", "wK", "wQ"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # IMAGE['wP']  ==   "wp.png" (SQ_SIZE x SQ_SIZE)


# chess #########################

def playChess():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill(pygame.Color("white"))
    pygame.display.set_caption("Chess game?")
    pygame.display.update()
    clock = pygame.time.Clock()
    game = ChessEngine.Game()
    validMoves = game.getValidMove()
    moveMade = False
    animate = True
    LoadImages()
    # drawMenu(window) ### does not work for now
    run = True
    sqSelected = ()  # no square
    playerClicks = []  # track 1st and 2nd player [(0, 0), (1, 1)]
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN:  # mouse down checker ######
                location = pygame.mouse.get_pos()  # location[x, y]
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # same
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 1 and game.board[sqSelected[0]][sqSelected[1]] == "--":
                    sqSelected = ()
                    playerClicks = []
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], game.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        game.makeMove(move)
                        moveMade = True
                        animate = True
                    sqSelected = ()  # clear move
                    playerClicks = []

            elif e.type == pygame.KEYDOWN:  # keys down checker #####
                if e.key == pygame.K_z:
                    game.undoMove()
                    moveMade = True
                    animate = False
                if e.key == pygame.K_r:
                    game = ChessEngine.Game()
                    validMoves = game.getValidMove()
                    sqSelected = ()
                    playerClicks = []
                    animate = False
                    moveMade = False
                if e.key == pygame.K_ESCAPE:
                    run = False

        if moveMade:
            if animate:
                animation(game.moveLog[-1], window, game.board, clock)
            validMoves = game.getValidMove()
            moveMade = False
            animate = False

        drawGame(window, game, sqSelected, validMoves)
        clock.tick(FPS)
        pygame.display.flip()


# graphics ##########################################

def drawGame(window, game, sqSelected, validMoves):
    drawBoard(window)
    highlightCells(window, game, sqSelected, validMoves)
    drawPieces(window, game.board)


def drawBoard(window):
    colors = [pygame.Color(COLORS[0]), pygame.Color(COLORS[1])]
    # colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(window, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(window, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                window.blit(IMAGES[piece], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlightCells(window, game, sqSelected, validMoves):
    if sqSelected != ():
        r, c = sqSelected
        if game.board[r][c][0] == ("w" if game.whiteMove else "b"):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(pygame.Color("blue"))
            window.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.startCol == c and move.startRow == r:
                    window.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))


def animation(move, window, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerCell = 3
    framesCount = (abs(dR) + abs(dC)) * framesPerCell
    for frame in range(framesCount + 1):
        r, c = (move.startRow + dR * frame / framesCount, move.startCol + dC * frame / framesCount)
        drawBoard(window)
        drawPieces(window, board)
        color = COLORS[(move.endRow + move.endCol) % 2]
        endCell = pygame.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(window, color, endCell)
        if move.pieceCaptured != "--":
            window.blit(IMAGES[move.pieceCaptured], endCell)
        window.blit(IMAGES[move.pieceMoved], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(FPS)


# options ######################################################

def cellColor(color1, color2):
    global COLORS
    COLORS = [color1, color2]


def options():
    pygame.init()
    pygame.display.set_caption('game base')
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    font = pygame.font.SysFont("menu_font", 32)
    bg_image = pygame.transform.scale(pygame.image.load("images/menu_bg2.jpg"), (WIDTH, HEIGHT))
    txt_color = (200, 200, 200)
    bWidth = WIDTH // 4
    bHeight = HEIGHT // 20
    bx = WIDTH // 2 - bWidth
    by = HEIGHT // 6 - bHeight
    dy = 1.5
    dx = 0.5

    run = True
    click = False
    while run:
        screen.fill("black")
        screen.blit(bg_image, pygame.Rect(0, 0, WIDTH, HEIGHT))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(bx, by * 1, bWidth, bHeight)
        button_2 = pygame.Rect(bx, by + bHeight * dy, bWidth, bHeight)
        button_3 = pygame.Rect(bx, by + bHeight * 2 * dy, bWidth, bHeight)
        button_extra_1 = pygame.Rect(bx, by + bHeight * 4 * dy, bWidth, bHeight)
        button_extra_2 = pygame.Rect(bx, by + bHeight * 5 * dy, bWidth, bHeight)

        if button_1.collidepoint((mx, my)):
            if click:
                cellColor("white", "gray")
                run = False
        if button_2.collidepoint((mx, my)):
            if click:
                cellColor((100, 200, 200), (100, 100, 200))
                run = False
        if button_3.collidepoint((mx, my)):
            if click:
                cellColor((250, 240, 200), (150, 100, 50))
                run = False
        if button_extra_1.collidepoint((mx, my)):
            if click:
                cellColor((250, 250, 250), (250, 250, 250))
                run = False
        if button_extra_2.collidepoint((mx, my)):
            if click:
                cellColor((5, 5, 10), (5, 5, 5))
                run = False

        # pygame.draw.rect(screen, (0, 0, 0), button_1)
        # pygame.draw.rect(screen, (0, 0, 0), button_2)
        # pygame.draw.rect(screen, (0, 0, 0), button_3)
        draw_text('white / gray', font, txt_color, screen, bx, by * 1)
        draw_text('blue / cyan', font, txt_color, screen, bx, by + bHeight * dy)  # dy = 1.5
        draw_text('white / brown', font, txt_color, screen, bx, by + bHeight * 2 * dy)  # dy = 1.5
        draw_text("Cells color", font, txt_color, screen, bx - bWidth * dx, by - bHeight * dy)  # dy = 1.5 dx = 0.5
        draw_text("Extra options", font, txt_color, screen, bx - bWidth * dx, by + bHeight * 3 * dy)
        draw_text('white board', font, txt_color, screen, bx, by + bHeight * 4 * dy)
        draw_text('night mode', font, txt_color, screen, bx, by + bHeight * 5 * dy)

        clock = pygame.time.Clock()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)


#
# tetris ###########################################
#

def playTetris():
    startGame()


#
# man menu ##################################################
#

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu():
    pygame.init()
    pygame.display.set_caption('game base')
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    font = pygame.font.SysFont("menu_font", 32)
    bg_image = pygame.transform.scale(pygame.image.load("images/menu_bg2.jpg"), (WIDTH, HEIGHT))
    txt_color = (200, 200, 200)
    bWidth = WIDTH // 3
    bHeight = HEIGHT // 20
    bx = WIDTH // 2 - bWidth
    by = HEIGHT // 3 - bHeight

    click = False
    while True:
        screen.fill("black")
        screen.blit(bg_image, pygame.Rect(0, 0, WIDTH, HEIGHT))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(bx, by * 1, bWidth, bHeight)
        button_2 = pygame.Rect(bx, by + bHeight * 2, bWidth, bHeight)
        button_3 = pygame.Rect(bx, by - bHeight * 2, bWidth, bHeight)

        if button_1.collidepoint((mx, my)):
            if click:
                playChess()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                playTetris()
        pygame.draw.rect(screen, (0, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)
        draw_text('Play chess', font, txt_color, screen, bx, by * 1)
        draw_text('Options', font, txt_color, screen, bx, by + bHeight * 2)
        draw_text('Play Tetris', font, txt_color, screen, bx, by - bHeight * 2)
        draw_text('by Nick Komarov', pygame.font.SysFont("menu_font", 24), txt_color, screen, bx + bWidth * 0.8, by - bHeight * 2)

        clock = pygame.time.Clock()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
