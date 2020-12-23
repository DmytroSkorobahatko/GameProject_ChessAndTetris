import pygame, sys
import ChessEngine

# https://www.youtube.com/watch?v=EnYui0e73Rs

WIDTH = HEIGHT = 512
DIMENSION = 8  # 8 x 8 - common in chess
SQ_SIZE = HEIGHT // DIMENSION
FPS = 30
IMAGES = {}
COLORS = [(255, 255, 255), (100, 100, 100)]


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
                    sqSelected = ()  # clear move
                    playerClicks = []

            elif e.type == pygame.KEYDOWN:  # keys down checker #####
                if e.key == pygame.K_z:
                    game.undoMove()
                    moveMade = True

                if e.key == pygame.K_ESCAPE:
                    run = False

        if moveMade:
            validMoves = game.getValidMove()
            moveMade = False

        drawGame(window, game)
        clock.tick(FPS)
        pygame.display.flip()


# graphics #####################

def drawGame(window, game):
    drawBoard(window)
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


# options #######################################

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
    bWidth = 100
    bHeight = 20
    bx = WIDTH // 2 - bWidth
    by = HEIGHT // 3 - bHeight

    run = True
    click = False
    while run:
        screen.fill("black")
        screen.blit(bg_image, pygame.Rect(0, 0, WIDTH, HEIGHT))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(bx, by * 1, bWidth, bHeight)
        button_2 = pygame.Rect(bx, by + bHeight * 2, bWidth, bHeight)

        if button_1.collidepoint((mx, my)):
            if click:
                cellColor("white", "gray")
                run = False
        if button_2.collidepoint((mx, my)):
            if click:
                cellColor((100, 200, 200), (100, 100, 200))
                run = False

        pygame.draw.rect(screen, (0, 0, 0), button_1)
        draw_text('white / gray', font, txt_color, screen, bx, by * 1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)
        draw_text('blue / cyan', font, txt_color, screen, bx, by + bHeight * 2)

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


# man menu ######################################

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
    bWidth = 100
    bHeight = 20
    bx = WIDTH // 2 - bWidth
    by = HEIGHT // 3 - bHeight

    click = False
    while True:
        screen.fill("black")
        screen.blit(bg_image, pygame.Rect(0, 0, WIDTH, HEIGHT))

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(bx, by * 1, bWidth, bHeight)
        button_2 = pygame.Rect(bx, by + bHeight * 2, bWidth, bHeight)

        if button_1.collidepoint((mx, my)):
            if click:
                playChess()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (0, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)
        draw_text('Play chess', font, txt_color, screen, bx, by * 1)
        draw_text('Options', font, txt_color, screen, bx, by + bHeight * 2)

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
