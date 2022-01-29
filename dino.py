# NOTE: Before running the game:
# 1. Install the "PressStart2P-Regular.ttf" font (stored in the assets folder) on your system
# 2. Install the "playsound" module using pip
# Assets from Itch.io - https://halestorm512.itch.io/chrome-dinosaur-game-remake
# Font from Google Fonts - https://fonts.google.com/specimen/Press+Start+2P

import turtle
import random
import time  # For time.time
import multiprocessing  # To play sound in thread to stop it as required
import os
try:
    from playsound import playsound  # To play sound effects
except:  # If module is not found on system
    print("The 'playsound' module was not found on your system. Attempting to install the module using pip.")
    os.system("pip install playsound")


def new_shape(file, hide=False):
    t = turtle.Turtle()
    t.shape(file)
    t.penup()
    if hide: t.hideturtle()
    return t


def jump():
    global JUMP, DUCK, SPEED
    if not JUMP:
        playsound("assets/jump sound.wav", block=False)
        DUCK = False
        JUMP = True
        SPEED = 270


def duck():
    global JUMP, DUCK
    if not DUCK and not JUMP:
        DUCK = True
        JUMP = False


def unduck():
    global DUCK
    DUCK = False


def get_high_score():
    try:
        with open("score.txt", "r") as f:
            score = int(f.read())
    except:
        score = 0
    return score


def save_high_score():
    score = get_high_score()
    if SCORE > score:
        with open("score.txt", "w") as f:
            f.write(str(SCORE))
        return True
    return False


def update_score():
    high_score = get_high_score()
    if SCORE > high_score:
        high_score = SCORE

    turtle.tracer(0, 0)
    global scorepen
    try:
        scorepen.clear()
    except:
        scorepen = turtle.Turtle()
        scorepen.hideturtle()
        scorepen.penup()

    scorepen.goto(280, 420)
    scorepen.color("black")
    scorepen.write(f"HIGH:{high_score:05} SCORE:{SCORE:05}", align="center", font=("Press Start 2P", 25, "normal"))

    turtle.tracer(1, 1)


def update():
    start = time.time()
    global dino, bird, cacti, paths, BIRD_YCORS, GAME_SPEED, JUMP, SPEED, SHAPE, UPDATES, SCORE, FIRSTGAME, stars, cloud, CLOUDSPEED
    if SCORE <= 1000:
        GAME_SPEED = (5 + SCORE // 300)  # Caps game speed at 8 so that the game does not get too fast and unplayable
    turtle.tracer(0, 0)
    for path in paths:
        path.setx(path.xcor() - GAME_SPEED)
        if path.xcor() <= -1000:
            path.goto(1000, -300)

    if UPDATES % 13 == 0:
        SCORE += 1

        if FIRSTGAME:
            if SCORE == 30:
                string = ""
                for char in "Press SPACE to jump!":  # Instructions on how to jump
                    string += char  # Shows each character one by one for an effect
                    tutorialpen.write(string, align="right", font=("Press Start 2P", 25, "normal"))
                    turtle.tracer(1, 1)
                    turtle.tracer(0, 0)
                    tutorialpen.clear()
                time.sleep(4)
                tutorialpen.clear()
            elif abs(bird.xcor()) < 500:  # When bird comes into frame
                string = ""
                for char in "Press DOWN KEY to duck!":  # Instructions on how to duck
                    string += char  # Shows each character one by one for an effect
                    tutorialpen.write(string, align="right", font=("Press Start 2P", 25, "normal"))
                    turtle.tracer(1, 1)
                    turtle.tracer(0, 0)
                    tutorialpen.clear()
                time.sleep(4)
                tutorialpen.clear()
                FIRSTGAME = False

        turtle.ontimer(update_score, 1)

        if DUCK and dino.ycor() == -200:
            if SHAPE == "assets/DinoDuckLeftUp.gif":  # Change turtle leg
                SHAPE = "assets/DinoDuckRightUp.gif"
                dino.shape("assets/DinoDuckRightUp.gif")
            else:
                SHAPE = "assets/DinoDuckLeftUp.gif"
                dino.shape("assets/DinoDuckLeftUp.gif")
        else:
            if JUMP:
                SHAPE = "assets/DinoIdle.gif"
                dino.shape("assets/DinoIdle.gif")
            elif SHAPE == "assets/DinoLeftUp.gif":  # Change turtle leg
                SHAPE = "assets/DinoRightUp.gif"
                dino.shape("assets/DinoRightUp.gif")
            else:
                SHAPE = "assets/DinoLeftUp.gif"
                dino.shape("assets/DinoLeftUp.gif")

        if bird.shape() == "assets/BirdFlapUp.gif":
            bird.shape("assets/BirdFlapDown.gif")
        else:
            bird.shape("assets/BirdFlapUp.gif")

    if JUMP:
        SPEED = SPEED - 13.2  # Gravity
        dino.sety(dino.ycor() + SPEED/8)  # Divide speed by 8 since we update every 8 ms to make the jump look more natural

        if dino.ycor() < -200:  # Stop jumping as dino has reached ground
            dino.sety(-200)
            JUMP = False

    bird.setx(bird.xcor() - GAME_SPEED)

    if (bird.xcor() - 40 < dino.xcor() < bird.xcor() + 40) and (bird.ycor() - 90 < dino.ycor() < bird.ycor() + 90):
        if not (bird.ycor() == -120 and DUCK):
            gameover()
            return

    if bird.xcor() < -515 and SCORE >= 100:
        if random.randint(500, 700) == 500:  # Randomise duration between birds
            if FIRSTGAME:
                bird.goto(cacti[-1].xcor() + 1000, -120)  # Go a random distance after last cactus at ducking position for tutorial
            else:
                bird.goto(cacti[-1].xcor() + random.randint(1000, 1200), random.choice(BIRD_YCORS))  # Go a random distance after last cactus at one of the possible y-coordinates

    for cactus in cacti:
        cactus.setx(cactus.xcor() - GAME_SPEED)

        if cactus.distance(dino) < 55:
            gameover()
            return

        if cactus.xcor() < -515:
            if bird.xcor() > 500 and cacti[-1].xcor() < bird.xcor():
                cactus.setx(bird.xcor() + random.randint(1000, 1200))
            else:
                cactus.setx(cacti[-1].xcor() + random.randint(350, 700))
            cactus.shape(random.choice(cacti_gifs))
            cacti.append(cacti.pop(cacti.index(cactus)))

    cloud.setx(cloud.xcor() - CLOUDSPEED)
    if cloud.xcor() <= -530:
        cloud.setx(530)
        cloud.sety(random.randint(250, 450))
        CLOUDSPEED = random.randint(1, 4)

    for star, speed in stars.items():
        if star.xcor() < -520:  # Reset stars that exited the screen
            star.goto(520, random.randint(0, 500))
        star.setx(star.xcor() - speed)  # Move stars

    turtle.tracer(1, 1)
    UPDATES += 1

    # Normalise update speed so that when code takes longer to execute, the updates don't get slower
    ms_elapsed = int(round(time.time() - start, 3) * 1000)
    if ms_elapsed > 8:
        update()
    else:
        turtle.ontimer(update, 8 - ms_elapsed)


def gameover():
    p.terminate()
    playsound("assets/game over.wav", block=False)
    save_high_score()
    turtle.tracer(0, 0)

    global gameoverpen
    try:
        gameoverpen.clear()
    except:
        gameoverpen = turtle.Turtle()
        gameoverpen.hideturtle()
        gameoverpen.penup()

    gameoverpen.goto(0, 200)
    gameoverpen.color("black")
    gameoverpen.write("GAME OVER", align="center", font=("Press Start 2P", 25, "normal"))

    gameoverpen.goto(0, 0)
    gameoverpen.color("gray")
    gameoverpen.write("Click anywhere to play again.", align="center", font=("Press Start 2P", 15, "normal"))

    turtle.tracer(1, 1)
    turtle.onscreenclick(restart)
    turtle.listen()


def restart(x, y):
    playsound("assets/button pressed.wav", block=False)
    global paths, dino, bird, cacti, cacti_gifs, SCORE, JUMP, DUCK, UPDATES, SPEED, GAME_SPEED, SHAPE, scorepen, gameoverpen, CLOUDSPEED, stars, p
    turtle.onscreenclick(None)
    SCORE = 0
    JUMP = False
    DUCK = False
    CLOUDSPEED = random.randint(1, 4)
    UPDATES = 0
    SPEED = 0
    GAME_SPEED = 20
    SHAPE = "assets/DinoIdle.gif"

    turtle.tracer(0, 0)
    scorepen.clear()
    gameoverpen.clear()
    paths[0].goto(0, -300)
    paths[1].goto(1000, -300)
    dino.goto(-400, -200)
    bird.goto(-530, -120)
    cacti[0].goto(2000, -250)
    cacti[1].goto(2500, -250)
    cacti[2].shape(random.choice(cacti_gifs))
    cacti[2].goto(3000, -250)
    cloud.goto(random.randint(-300, 400), random.randint(250, 450))
    for star, speed in stars.items():
        star.goto(random.randint(0, 500), random.randint(0, 500))  # Put star in random position
    turtle.tracer(1, 1)
    p = multiprocessing.Process(target=playsound, args=("assets/soundtrack.wav",))
    p.start()
    update()


def init_game():
    global paths, dino, bird, cacti, cloud, cacti_gifs, screen, BIRD_YCORS, SCORE, JUMP, DUCK, UPDATES, SPEED, GAME_SPEED, SHAPE, scorepen, tutorialpen, FIRSTGAME, stars, CLOUDSPEED, p
    p = multiprocessing.Process(target=playsound, args=("assets/soundtrack.wav",))
    p.start()
    # Initialise game variables
    SCORE = 0
    JUMP = False
    DUCK = False
    FIRSTGAME = True
    CLOUDSPEED = random.randint(1, 4)
    UPDATES = 0
    SPEED = 0
    GAME_SPEED = 20
    SHAPE = "DinoIdle.gif"
    BIRD_YCORS = [-200, 0, -120]  # Different y-coordinates that the bird can fly in
    cacti = []
    paths = []

    tutorialpen.clear()
    tutorialpen.color("gray")

    turtle.tracer(0, 0)
    paths.append(new_shape("assets/path.gif"))  # Initialise first path sprite
    paths[0].goto(0, -300)
    paths.append(new_shape("assets/path.gif"))  # Initialise second path sprite
    paths[1].goto(1000, -300)
    dino = new_shape("assets/DinoIdle.gif")  # Setup dino
    dino.goto(-400, -200)
    bird = new_shape("assets/BirdFlapUp.gif")  # Setup bird
    bird.goto(-550, -120)
    cacti.append(new_shape("assets/1Big.gif"))
    cacti[0].goto(2000, -250)
    cacti.append(new_shape("assets/1Big.gif"))
    cacti[1].goto(2500, -250)
    cacti.append(new_shape(random.choice(cacti_gifs)))
    cacti[2].goto(3000, -250)

    cloud = new_shape("assets/cloud.gif")
    cloud.goto(random.randint(-300, 400), random.randint(250, 450))  # Put cloud in random position
    stars = {}
    for i in range(1, 5):
        star = new_shape("assets/star.gif")
        star.goto(random.randint(0, 500), random.randint(0, 500))  # Put star in random position
        stars[star] = i  # 'i' will be the speed of the star

    screen.onkey(jump, "space")
    screen.onkeypress(duck, "Down")
    screen.onkeyrelease(unduck, "Down")
    screen.listen()
    turtle.tracer(1, 1)
    update()


def skip_tutorial(*args):
    playsound("assets/button pressed.wav", block=False)
    global SKIPPED, FIRSTGAME
    SKIPPED = True  # To skip the storyline
    for t in turtle.turtles():  # Clear everything to start game
        t.hideturtle()
    turtle.onscreenclick(None)
    init_game()
    FIRSTGAME = False  # To skip the later tutorial


def storyline(part=1):
    global tutorialpen, screen, path, babydino, dino, kingbird, SKIPPED
    if SKIPPED: return

    if part == 1:
        turtle.tracer(0, 0)
        turtle.onscreenclick(skip_tutorial)
        tutorialpen = turtle.Turtle()
        tutorialpen.hideturtle()
        tutorialpen.penup()
        tutorialpen.goto(300, -400)
        tutorialpen.write("Click anywhere to skip.", align="center", font=("Press Start 2P", 15, "normal"))
        tutorialpen.goto(490, 350)

        path = new_shape("assets/path.gif")
        path.goto(0, -300)

        dino = new_shape("assets/DinoIdle.gif")
        dino.goto(-400, -200)
        babydino = new_shape("assets/BabyDinoIdle.gif")
        babydino.goto(-330, -232)
        kingbird = new_shape("assets/KingBirdFlapDownRight.gif")
        kingbird.goto(-560, 550)
        turtle.tracer(1, 1)
        turtle.ontimer(lambda: storyline(part=2), 2000)
    elif part == 2:
        babydino.speed(1)  # Baby dino walks forward
        turtle.delay(10)
        for i in range(200):
            babydino.forward(1)
            if i % 20 == 0:
                if babydino.shape() == "assets/BabyDinoRightUp.gif":
                    babydino.shape("assets/BabyDinoLeftUp.gif")
                else:
                    babydino.shape("assets/BabyDinoRightUp.gif")
        babydino.shape("assets/BabyDinoIdle.gif")
        turtle.ontimer(lambda: storyline(part=3), 3500)
    elif part == 3:
        playsound("assets/run.wav", block=False)
        turtle.tracer(1, 1)  # King bird swoops down on baby dino
        kingbird.speed(1)
        turtle.delay(8)
        kingbird.goto(babydino.pos())

        for i in range(800):  # Move baby dino and king bird together out of the frame to the right
            turtle.tracer(0, 0)
            babydino.goto(babydino.xcor() + 1, babydino.ycor() + 0.75)
            kingbird.goto(kingbird.xcor() + 1, kingbird.ycor() + 0.75)
            if i % 150 == 0:  # Flap wing of king bird
                if kingbird.shape() == "assets/KingBirdFlapUpRight.gif":
                    kingbird.shape("assets/KingBirdFlapDownRight.gif")
                else:
                    kingbird.shape("assets/KingBirdFlapUpRight.gif")
            turtle.tracer(1, 1)
        turtle.tracer(0, 0)

        string = ""  # Let players know the aim of the game
        for char in "Help the Dino save his son!":
            string += char
            turtle.tracer(0, 0)
            tutorialpen.clear()
            tutorialpen.write(string, align="right", font=("Press Start 2P", 25, "normal"))
            turtle.tracer(1, 1)

        if not SKIPPED:
            turtle.ontimer(skip_tutorial, 4000)


def startbtn_clicked(*args):
    global background, startbtn, exitbtn
    playsound("assets/button pressed.wav", block=False)
    turtle.tracer(0, 0)

    background.hideturtle()
    startbtn.hideturtle()
    exitbtn.hideturtle()
    startbtn.onclick(None)
    exitbtn.onclick(None)
    storyline()


def title_screen():
    global background, startbtn, exitbtn
    turtle.tracer(0, 0)
    background = new_shape("assets/poster.gif")
    background.goto(0, 0)
    startbtn = new_shape("assets/StartBtn.gif")
    startbtn.goto(0, -100)
    startbtn.onrelease(startbtn_clicked)
    exitbtn = new_shape("assets/ExitBtn.gif")
    exitbtn.goto(0, -210)
    exitbtn.onclick(lambda x, y: exit)
    turtle.tracer(1, 1)


def on_close():  # When window close button is clicked
    try:
        p.terminate()  # Stop the game soundtrack
        save_high_score()
    except:
        pass  # If it is prior to the game starting
    finally:
        exit()


if __name__ == '__main__':
    # Setup screen
    screen = turtle.Screen()
    screen.setup(1300, 600)
    screen.setworldcoordinates(-500, -500, 500, 500)
    screen.title("ERROR RUN - 404 Not Found")
    turtle.hideturtle()
    turtle.bgcolor("light gray")
    root = turtle.getcanvas().winfo_toplevel()  # Accessing root window element
    root.protocol("WM_DELETE_WINDOW", on_close)  # Setting function to be called when close window button is clicked

    dino_gifs = ['assets/DinoIdle.gif', 'assets/DinoLeftUp.gif', 'assets/DinoRightUp.gif', 'assets/DinoDuckLeftUp.gif', 'assets/DinoDuckRightUp.gif']
    bird_gifs = ["assets/BirdFlapDown.gif", "assets/BirdFlapUp.gif"]
    cacti_gifs = ['assets/1Big.gif', 'assets/1Small.gif', 'assets/2Big.gif', 'assets/2Big1Small1Big.gif', 'assets/2Small.gif', 'assets/3Big.gif', 'assets/3Small.gif']
    bg_gifs = ["assets/cloud.gif", "assets/star.gif"]
    storyline_gifs = ["assets/BabyDinoIdle.gif", "assets/KingBirdFlapDownLeft.gif", "assets/KingBirdFlapDownRight.gif", "assets/KingBirdFlapUpRight.gif", "assets/KingBirdFlapUpLeft.gif", "assets/BabyDinoLeftUp.gif", "assets/BabyDinoRightUp.gif"]
    other_gifs = ["assets/path.gif", "assets/poster.gif", "assets/StartBtn.gif", "assets/ExitBtn.gif"]
    for gif in cacti_gifs + dino_gifs + bird_gifs + bg_gifs + storyline_gifs + other_gifs:
        turtle.register_shape(gif)

    SKIPPED = False
    title_screen()
    turtle.mainloop()
