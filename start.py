import pygame
import random
import time

# размер автомобиля
sport_h = 150
sport_w = 85

# размер отображения
dh = 550
dw = 800

# цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (53, 115, 255)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
pause = False

score_game = 0

game_display = pygame.display.set_mode((dw, dh))
clock = pygame.time.Clock()


# настройка игры
def game_init():
    pygame.init()
    pygame.display.set_caption('Гоночки')


def display(count, x, y, message_format='Счёт: %d'):
    """display the score"""
    font = pygame.font.SysFont("comicsansms", 20)
    text = font.render(message_format % count, True, black)
    game_display.blit(text, (x, y))


def things(thingX, thingY, thingW, thingH, color):
    """draw random things (car or anything)"""
    pygame.draw.rect(game_display, color, [thingX, thingY, thingW, thingH])


def line(lineX, lineY, lineW, lineH, color):
    """draw way lines """
    pygame.draw.rect(game_display, color, [lineX, lineY, lineW, lineH])


def load_image(x, y, image_name):
    img = pygame.image.load(image_name)
    game_display.blit(img, (x, y))


def text_object(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    """display message after crash"""
    largeText = pygame.font.SysFont("comicsansms", 115)
    textSurf, textRect = text_object(text, largeText)
    textRect.center = ((dw / 2), (dh / 2))
    game_display.blit(textSurf, textRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()


def crash(x, y):
    car_crash = pygame.image.load('images/carcrash.png')
    game_display.blit(car_crash, ((x - 45), (y - 30)))
    crash_sound = pygame.mixer.Sound("music/crash.wav")
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()
    largeText = pygame.font.SysFont("comicsansms", 90)
    textSurf, textRect = text_object("Авария :(", largeText)
    textRect.center = ((dw / 2), (dh / 4))
    game_display.blit(textSurf, textRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Ещё раз", 150, 250, 100, 50, green, bright_green, game_loop)
        button("Выход", 550, 250, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, ic, ac, action=None):
    """message, dimension, active/inactive color"""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(game_display, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()

    else:
        pygame.draw.rect(game_display, ic, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_object(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    game_display.blit(textSurf, textRect)


def quitgame():
    pygame.quit()
    quit()


def game_unpause():
    global pause
    pause = False


def game_pause():
    pygame.mixer.music.pause()

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        largeText = pygame.font.SysFont("comicsansms", 90)
        textSurf, textRect = text_object("Пауза.", largeText)
        textRect.center = ((dw / 2), (dh / 4))
        game_display.blit(textSurf, textRect)

        button("Cтарт!", 150, 250, 100, 50, green, bright_green, game_unpause)
        button("Выход", 550, 250, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    pygame.mixer.music.load("music/atlanta.wav")
    pygame.mixer.music.play(-1)

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        game_display.fill(white)

        largeText = pygame.font.SysFont("comicsansms", 80)
        textSurf, textRect = text_object("Let's Ride :)", largeText)
        textRect.center = ((dw / 2), (dh / 2))
        game_display.blit(textSurf, textRect)

        button("Старт!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Выход", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause
    global score_game

    pygame.mixer.music.load('music/coffee_stains.wav')
    pygame.mixer.music.play(-1)

    x = (dw * 0.45)
    y = (dh * 0.75)

    x_change = 0
    y_change = 0
    speed_change = 0

    thing_width = 70
    thing_height = 140

    thing_startx = random.randrange(100, dw - 200)
    thing_starty = -600
    thing_speed = 4

    lineX = 400
    lineY = 0
    lineW = 20
    lineH = 450
    line_speed = 10

    tree_y_right = 600
    tree_y_left = 300
    tree_h = 600
    tree_speed = 10

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5

                if event.key == pygame.K_p:
                    pause = True
                    game_pause()

            if event.type == pygame.KEYUP:
                x_change = 0
        x += x_change

        game_display.fill(white)

        line(150, 0, 20, dh, blue)
        line(dw - 150, 0, 20, dh, blue)

        load_image(thing_startx, thing_starty, 'images/car.png')
        load_image(80, tree_y_left, 'images/trees.jpg')
        load_image(700, tree_y_right, 'images/trees.jpg')
        load_image(x, y, 'images/car1.png')

        thing_starty += thing_speed
        lineY += line_speed
        tree_y_left += tree_speed
        tree_y_right += tree_speed

        display(dodged, 5, 25)
        display(thing_speed * 60, 5, 50, "spd: %d px/s")
        display(score_game, 5, 5, "Общий счёт: %d")

        if x > dw - sport_w - 150 or x < 150:
            crash(x, y)

        if thing_starty > dh:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(170, dw - thing_width - 150)
            dodged += 1
            score_game += 1
            thing_speed += 1 / 20  # ускорение

        if lineY > dh:
            lineY = 0 - lineH
            thing_speed += 1 / 15

        if tree_y_left > dh:
            tree_y_left = 0 - tree_h
            thing_speed += 1 / 15

        if tree_y_right > dh:
            tree_y_right = 0 - tree_h
            thing_speed += 1 / 15

        #авария
        if y < (thing_starty + thing_height) and y + sport_h >= thing_starty + thing_height:
            if x > thing_startx and x < (thing_startx + thing_width) or x + sport_w > thing_startx \
                    and x + sport_w < thing_startx + thing_width:
                crash(x, y)

        pygame.display.update()
        clock.tick(60)


def main():
    game_init()
    game_intro()
    game_loop()
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
