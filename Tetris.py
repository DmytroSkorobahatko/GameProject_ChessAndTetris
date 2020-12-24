import pygame as pg
import Field
import sys


def settingsTetris():
    global bgColor, linesColor, FPS, game_screen, screen, bg, clock, speed_counter, game_pause
    global score_points, score, game_over_text, score_text, record_text, game, game_start
    global font1, font2, speed, speed_limit, super_speed_counter, font3

    # bgColor = (0, 0, 0)
    # linesColor = (40, 40, 240)

    # creating game window
    game = Field.Field(17, 10, 30)
    SIZE = (game.width * game.tile, game.height * game.tile)
    FPS = 60
    GAME_SIZE = (512, 512)

    pg.init()
    pg.font.init()
    game_screen = pg.display.set_mode(GAME_SIZE)
    pg.display.set_caption("Tetris")
    screen = pg.Surface(SIZE)
    bg = pg.Surface((300, 512))
    clock = pg.time.Clock()

    speed_counter, speed, speed_limit, super_speed_counter = 0, 100, 2000, 0
    game_pause, game_start = False, True
    score_points = {
        0: 0,
        1: 100,
        2: 200,
        3: 400,
        4: 800
    }
    score = 0

    font1 = pg.font.SysFont("Castellar", 52)
    font2 = pg.font.SysFont("Castellar", 36)
    font3 = pg.font.SysFont("Castellar", 24)
    game_over_text = font1.render("GAME OVER!!!", True, (255, 255, 255))
    score_text = font2.render("SCORE: ", True, (255, 255, 255))
    record_text = font2.render("RECORD: ", True, (255, 255, 255))

    with open('Record.txt', 'w') as f:
        f.write(str(0))


def get_record():
    with open('Record.txt') as f:
        return f.readline()


def set_record(record, score):
    rec = max(int(record), int(score))
    with open('Record.txt', 'w') as f:
        f.write(str(rec))


def startGame(colorsTetris):
    # global bgColor, linesColor
    global FPS, game_screen, screen, bg, clock, speed_counter, game_pause
    global score_points, score, game_over_text, score_text, record_text, game, game_start
    global font1, font2, speed, speed_limit, super_speed_counter, font3
    settingsTetris()
    bgColor, linesColor = colorsTetris[0], colorsTetris[1]
    run = True
    end_game = False
    while run:
        game_screen.blit(screen, (0, 0))
        game_screen.blit(bg, (300, 0))
        screen.fill(bgColor)

        # if not end_game:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if not end_game:
                    if event.key == pg.K_LEFT:
                        game.go_side(-1)
                    if event.key == pg.K_RIGHT:
                        game.go_side(1)
                    if event.key == pg.K_UP:
                        game.rotate()
                    if event.key == pg.K_DOWN:
                        speed_limit = 100
                    if event.key == pg.K_r:
                        if not game_start:
                            game.field = [[0 for i in range(game.width + 1)] for j in range(game.height + 1)]
                            game_start = True
                            end_game = False
                elif event.key == pg.K_r:
                    if not game_start:
                        game.field = [[0 for i in range(game.width + 1)] for j in range(game.height + 1)]
                        game_start = True
                        end_game = False
                if event.key == pg.K_SPACE:
                    if not game_pause:
                        speed = 0
                        game_pause = True
                    else:
                        speed = 100
                        game_pause = False

                if event.key == pg.K_ESCAPE:
                    run = False

        record = get_record()

        if end_game:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        if not game_start:
                            game.field = [[0 for i in range(game.width + 1)] for j in range(game.height + 1)]
                            game_start = True
                            end_game = False
                    if event.key == pg.K_ESCAPE:
                        run = False

        if game.figure == None and game_start:
            game.new_figure()

        # break lines
        line = game.height - 1
        del_lines = 0
        for row in range(game.height - 1, -1, -1):
            counter = 0
            for i in range(game.width):
                if game.field[row][i] != 0:
                    counter += 1
                game.field[line][i] = game.field[row][i]
            if counter < game.width:
                line -= 1
            else:
                del_lines += 1
                speed += 3

        # calc score
        score += score_points[del_lines]

        # draw field
        grid = [pg.Rect(x * game.tile, y * game.tile, game.tile, game.tile) for x in range(game.width) for y in
                range(game.height)]
        [pg.draw.rect(screen, linesColor, i, 1) for i in grid]

        # draw text
        game_screen.blit(score_text, (310, 100))
        game_screen.blit(record_text, (310, 200))
        game_screen.blit(font2.render(str(score), True, (255, 255, 255)), (310, 150))
        game_screen.blit(font2.render(str(record), True, (255, 255, 255)), (310, 250))

        game_screen.blit(font3.render('R to restart', True, (255, 255, 255)), (310, 512 - 32 - 32 - 32))
        game_screen.blit(font3.render('ESC to exit', True, (255, 255, 255)), (310, 512 - 32 - 32))
        game_screen.blit(font3.render('SPACE to pause', True, (255, 255, 255)), (310, 512 - 32))

        # draw figure
        if game_start:
            fig = game.figure
            fig_im = fig.image()
            fig_rec = pg.Rect(0, 0, game.tile, game.tile)
            for i in range(4):
                fig_rec.x = (fig.x + fig_im[i] % 4) * game.tile
                fig_rec.y = (fig.y + fig_im[i] // 4) * game.tile
                pg.draw.rect(screen, fig.color, fig_rec)
                pg.draw.rect(screen, bgColor, fig_rec, 1)

        # move down
        if game_start:
            speed_counter += speed
            if speed_limit == 100:
                super_speed_counter += 1
            if speed_counter > speed_limit:
                speed_counter = 0
                if super_speed_counter > 6:
                    speed_limit = 2000
                    super_speed_counter = 0
                game.move_down()

                for i in range(4):
                    if fig.y + fig_im[i] // 4 > game.height - 2 or game.field[fig.y + fig_im[i] // 4 + 1][
                        fig.x + fig_im[i] % 4] != 0:
                        for j in range(4):
                            game.field[fig.y + fig_im[j] // 4][fig.x + fig_im[j] % 4] = fig.color
                        game.new_figure()
                # time.sleep(0.1)

        # draw field
        for y, raw in enumerate(game.field):
            for x, col in enumerate(raw):
                if col != 0:
                    fig_rec.x = x * game.tile
                    fig_rec.y = y * game.tile
                    pg.draw.rect(screen, col, fig_rec)
                    pg.draw.rect(screen, bgColor, fig_rec, 1)

        # end game
        for i in range(game.width):
            if game.field[0][i] != 0:
                set_record(record, score)
                game.figure = None
                game_start = False
                end_game = True
                game_screen.blit(game_over_text, (30, (game.height / 2) * game.tile))
                speed_counter, speed, speed_limit, super_speed_counter = 0, 100, 2000, 0
                score = 0

        if not game_start:
            game_screen.blit(game_over_text, (30, (game.height / 2) * game.tile))

        pg.display.flip()
        clock.tick(FPS)

