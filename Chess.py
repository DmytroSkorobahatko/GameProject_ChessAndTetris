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


def drawGame(window):
    LoadImages()
    drawBoard(window)
    drawPieces(window)


def drawBoard(window):
    pass


def drawPieces(window):
    pass


def main():
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    window.fill(pygame.Color("white"))

    pygame.display.set_caption("Chess game?")
    pygame.display.update()
    clock = pygame.time.Clock()

    g = ChessEngine.Game()
    LoadImages()

    # drawMenu(window) ### does not work for now
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()

