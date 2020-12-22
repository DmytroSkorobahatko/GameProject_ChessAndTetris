import pygame
import ChessEngine

# https://www.youtube.com/watch?v=EnYui0e73Rs

WIDTH = HEIGHT = 512
DIMENSION = 8  # 8 x 8 - common in chess
SQ_SIZE = HEIGHT // DIMENSION
FPS = 30
IMAGES = {}


def LoadImages():
    pieces = ["bp", "bR", "bN", "bB", "bK", "bQ", "wp", "wR", "wN", "wB", "wK", "wQ"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # IMAGE['wP']  ==   "wp.png" (SQ_SIZE x SQ_SIZE)


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill(pygame.Color("white"))
    pygame.display.set_caption("Chess game?")
    pygame.display.update()
    clock = pygame.time.Clock()
    game = ChessEngine.Game()
    LoadImages()
    # drawMenu(window) ### does not work for now
    run = True
    sqSelected = ()  # no square
    playerClicks = []  # track 1st and 2nd player [(0, 0), (1, 1)]
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()  # location[x, y]
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # same
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], game.board)
                    print(move.getChessNotation())
                    game.makeMove(move)
                    sqSelected = () #clear move
                    playerClicks = []


        drawGame(window, game)

        clock.tick(FPS)
        pygame.display.flip()


# menu don't work :( #
# def drawMenu(window):
#     menu_bg = pygame_menu.baseimage.BaseImage('images/menu_bg.jpg')
#     themes = {
#         'dark': pygame_menu.themes.Theme(menubar_close_button=False, background_color=menu_bg,
#                                          title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE)}
#     menu = pygame_menu.Menu(WIDTH, HEIGHT, title="Chess", theme=themes["dark"])
#     # menu.add_text_input('name :')
#     # menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
#     menu.add_button('Play', item_selected(menu))
#     menu.add_button('Quit', pygame_menu.events.EXIT)
#     menu.add_button('Quit', print(0))
#     menu.enable()
#     menu.mainloop(window)
# def item_selected(arg):
#     arg.disable()  # should close menu


# graphics #################

def drawGame(window, game):
    drawBoard(window)
    drawPieces(window, game.board)


def drawBoard(window):
    colors = [pygame.Color("white"), pygame.Color("gray")]
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


if __name__ == '__main__':
    main()
