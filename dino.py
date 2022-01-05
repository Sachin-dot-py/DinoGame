# NOTE: Install the "PressStart2P-Regular.ttf" font on your system and install the "playsound" module using pip prior to running the game.
# Assets from Itch.io - https://halestorm512.itch.io/chrome-dinosaur-game-remake
# Sound Effects from ___ - _______________
# Font from Google Fonts - https://fonts.google.com/specimen/Press+Start+2P

import turtle
import random
import time
import playsound # To play sound effects

def new_shape(file, hide=False):
    t = turtle.Turtle()
    t.shape(file)
    t.penup()
    if hide: t.hideturtle()
    return t

def jump():
    global JUMP, DUCK, SPEED
    if not JUMP:
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

    turtle.tracer(0,0)
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

    turtle.tracer(1,1)

def update():
    start = time.time()
    global dino, bird, cacti, paths, BIRD_YCORS, GAME_SPEED, JUMP, SPEED, SHAPE, UPDATES, SCORE, FIRSTGAME
    GAME_SPEED = (5 + SCORE % 1000 // 300) # Game speed starts from slow every 1000 points so that game speed does not get too fast and unplayable
    turtle.tracer(0,0)
    for path in paths:
        path.setx(path.xcor() - GAME_SPEED)
        if path.xcor() <= -1000:
            path.goto(1000, -300)

    if UPDATES % 13 == 0:
        SCORE += 1

        if FIRSTGAME:
            if SCORE == 30:
                string = ""
                for char in "Press SPACE to jump!":
                    string += char
                    tutorialpen.write(string, align="right", font=("Press Start 2P", 25, "normal"))
                    turtle.tracer(1,1)
                    turtle.tracer(0,0)
                    tutorialpen.clear()
                time.sleep(4)
                tutorialpen.clear()
            elif bird.xcor() < 500 and bird.xcor() > -500:
                string = ""
                for char in "Press DOWN KEY to duck!":
                    string += char
                    tutorialpen.write(string, align="right", font=("Press Start 2P", 25, "normal"))
                    turtle.tracer(1,1)
                    turtle.tracer(0,0)
                    tutorialpen.clear()
                time.sleep(4)
                tutorialpen.clear()
                FIRSTGAME = False

        turtle.ontimer(update_score, 1)

        if DUCK and dino.ycor() == -200:
            if SHAPE == "DinoDuckLeftUp.gif": # Change turtle leg
                SHAPE = "DinoDuckRightUp.gif"
                dino.shape("DinoDuckRightUp.gif")
            else:
                SHAPE = "DinoDuckLeftUp.gif"
                dino.shape("DinoDuckLeftUp.gif")
        else:
            if JUMP:
                SHAPE = "DinoIdle.gif"
                dino.shape("DinoIdle.gif")
            elif SHAPE == "DinoLeftUp.gif": # Change turtle leg
                SHAPE = "DinoRightUp.gif"
                dino.shape("DinoRightUp.gif")
            else:
                SHAPE = "DinoLeftUp.gif"
                dino.shape("DinoLeftUp.gif")

        if bird.shape() == "BirdFlapUp.gif":
            bird.shape("BirdFlapDown.gif")
        else:
            bird.shape("BirdFlapUp.gif")

    if JUMP:
        SPEED = SPEED - 13.2 # Gravity
        dino.sety(dino.ycor() + SPEED/8) # Divide speed by 8 since we update every 8 ms to make the jump look more natural

        if dino.ycor() < -200: # Stop jumping as dino has reached ground
            dino.sety(-200)
            JUMP = False

    bird.setx(bird.xcor() - GAME_SPEED)

    if (bird.xcor() - 40 < dino.xcor() < bird.xcor() + 40) and (bird.ycor() - 90 < dino.ycor() < bird.ycor() + 90):
        if not (bird.ycor() == -120 and DUCK):
            gameover()
            return

    if bird.xcor() < -515 and SCORE >= 100:
        if random.randint(500, 700) == 500: # Randomise duration between birds
            if FIRSTGAME:
                bird.goto(cacti[-1].xcor() + 1000, -120) # Go a random distance after last cactus at ducking position for tutorial
            else:
                bird.goto(cacti[-1].xcor() + random.randint(1000, 1200), random.choice(BIRD_YCORS)) # Go a random distance after last cactus at one of the possible y-coordinates

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

    cloud.setx(cloud.xcor() - 2)
    if cloud.xcor() <= -530:
        cloud.setx(530)
        cloud.sety(random.randint(250, 450))

    turtle.tracer(1,1)
    UPDATES += 1

    # Normalise update speed so that when code takes longer to execute, the updates don't get slower
    ms_elapsed = int(round(time.time() - start, 3) * 1000)
    if ms_elapsed > 8:
        update()
    else:
        turtle.ontimer(update, 8 - ms_elapsed)

def gameover():
    save_high_score()
    turtle.tracer(0,0)

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

    turtle.tracer(1,1)
    turtle.onscreenclick(restart)
    turtle.listen()

def restart(x, y):
    global paths, dino, bird, cacti, cacti_gifs, SCORE, JUMP, DUCK, UPDATES, SPEED, GAME_SPEED, SHAPE, scorepen, gameoverpen
    turtle.onscreenclick(None)
    SCORE = 0
    JUMP = False
    DUCK = False
    UPDATES = 0
    SPEED = 0
    GAME_SPEED = 20
    SHAPE = "DinoIdle.gif"

    turtle.tracer(0,0)
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
    turtle.tracer(1,1)
    update()

def init_game():
    global paths, dino, bird, cacti, cloud, cacti_gifs, screen, BIRD_YCORS, SCORE, JUMP, DUCK, UPDATES, SPEED, GAME_SPEED, SHAPE, scorepen, tutorialpen, FIRSTGAME

    # Initialise game variables
    SCORE = 0
    JUMP = False
    DUCK = False
    FIRSTGAME = True
    UPDATES = 0
    SPEED = 0
    GAME_SPEED = 20
    SHAPE = "DinoIdle.gif"
    BIRD_YCORS = [-200, 0, -120] # Different y-coordinates that the bird can fly in
    cacti = []
    paths = []

    tutorialpen.clear()

    turtle.tracer(0,0)
    paths.append(new_shape("path.gif")) # Initialise first path sprite
    paths[0].goto(0, -300)
    paths.append(new_shape("path.gif")) # Initialise second path sprite
    paths[1].goto(1000, -300)
    dino = new_shape("DinoIdle.gif") # Setup dino
    dino.goto(-400, -200)
    bird = new_shape("BirdFlapUp.gif") # Setup bird
    bird.goto(-550, -120)
    cacti.append(new_shape("1Big.gif"))
    cacti[0].goto(2000, -250)
    cacti.append(new_shape("1Big.gif"))
    cacti[1].goto(2500, -250)
    cacti.append(new_shape(random.choice(cacti_gifs)))
    cacti[2].goto(3000, -250)
    cloud = new_shape("cloud.gif")
    cloud.goto(random.randint(-300, 400), random.randint(250, 450)) # Put cloud in random position
    turtle.tracer(1,1)

    screen.onkey(jump, "space")
    screen.onkeypress(duck, "Down")
    screen.onkeyrelease(unduck, "Down")
    screen.listen()
    update()

def skip_tutorial(*args):
    global SKIPPED
    SKIPPED = True
    for t in turtle.turtles(): # Clear everything to start game
        t.hideturtle()
    turtle.onscreenclick(None)
    init_game()

def storyline(part=1):
    global tutorialpen, screen, path, babydino, dino, kingbird, SKIPPED
    if SKIPPED: return
    if part == 1:
        turtle.tracer(0,0)
        turtle.onscreenclick(skip_tutorial)
        tutorialpen = turtle.Turtle()
        tutorialpen.hideturtle()
        tutorialpen.penup()
        tutorialpen.goto(300, -400)
        tutorialpen.write("Click anywhere to skip.", align="center", font=("Press Start 2P", 15, "normal"))
        tutorialpen.goto(490, 350)

        path = new_shape("path.gif")
        path.goto(0, -300)

        dino = new_shape("DinoIdle.gif")
        dino.goto(-400, -200)
        babydino = new_shape("BabyDinoIdle.gif")
        babydino.goto(-330, -232)
        kingbird = new_shape("KingBirdFlapDownRight.gif")
        kingbird.goto(-560, 550)
        turtle.tracer(1,1)
        turtle.ontimer(lambda: storyline(part=2), 2000)
    elif part == 2:
        babydino.speed(1) # Baby dino walks forward
        turtle.delay(10)
        for i in range(200):
            babydino.forward(1)
            if i % 20 == 0:
                if babydino.shape() == "BabyDinoRightUp.gif":
                    babydino.shape("BabyDinoLeftUp.gif")
                else:
                    babydino.shape("BabyDinoRightUp.gif")
        babydino.shape("BabyDinoIdle.gif")
        turtle.ontimer(lambda: storyline(part=3), 3500)
    elif part == 3:
        turtle.tracer(1,1) # King bird swoops down on baby dino
        kingbird.speed(1)
        turtle.delay(8)
        kingbird.goto(babydino.pos())

        for i in range(800): # Move baby dino and king bird together out of the frame to the right
            turtle.tracer(0,0)
            babydino.goto(babydino.xcor() + 1, babydino.ycor() + 0.75)
            kingbird.goto(kingbird.xcor() + 1, kingbird.ycor() + 0.75)
            if i % 150 == 0: # Flap wing of king bird
                if kingbird.shape() == "KingBirdFlapUpRight.gif":
                    kingbird.shape("KingBirdFlapDownRight.gif")
                else:
                    kingbird.shape("KingBirdFlapUpRight.gif")
            turtle.tracer(1,1)
        turtle.tracer(0,0)

        string = "" # Let players know the aim of the game
        for char in "Help the Dino save his son!":
            string += char
            turtle.tracer(0,0)
            tutorialpen.clear()
            tutorialpen.write(string, align="right", font=("Press Start 2P", 25, "normal"))
            turtle.tracer(1,1)

        if not SKIPPED: turtle.ontimer(skip_tutorial, 4000)

if __name__ == '__main__':
    # Setup screen
    screen = turtle.Screen()
    screen.setup(1300, 600)
    screen.setworldcoordinates(-500, -500, 500, 500)
    screen.title("DINO GAME - 404 Not Found")
    turtle.hideturtle()
    turtle.bgcolor("light gray")

    dino_gifs = ['DinoIdle.gif', 'DinoLeftUp.gif', 'DinoRightUp.gif', 'DinoDuckLeftUp.gif', 'DinoDuckRightUp.gif']
    bird_gifs = ["BirdFlapDown.gif","BirdFlapUp.gif"]
    cacti_gifs = ['1Big.gif', '1Small.gif', '2Big.gif', '2Big1Small1Big.gif', '2Small.gif', '3Big.gif', '3Small.gif']
    bg_gifs = ["cloud.gif", "star.gif", "sun.gif"]
    storyline_gifs = ["BabyDinoIdle.gif", "KingBirdFlapDownLeft.gif", "KingBirdFlapDownRight.gif", "KingBirdFlapUpRight.gif", "KingBirdFlapUpLeft.gif", "BabyDinoLeftUp.gif", "BabyDinoRightUp.gif"]
    for gif in cacti_gifs + dino_gifs + bird_gifs + bg_gifs + storyline_gifs + ["path.gif"]:
        turtle.register_shape(gif)

    SKIPPED = False
    storyline()
    turtle.mainloop()
