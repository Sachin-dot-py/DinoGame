# NOTE: Before running the game:
# 1. Install the "PressStart2P-Regular.ttf" font (stored in the assets folder) on your system
# 2. Install the "playsound" module using pip
# Font from Google Fonts - https://fonts.google.com/specimen/Press+Start+2P

import turtle
import random
import time  # For time.time
import multiprocessing  # To play sound in thread to stop it as required
import os
import urllib.request

try:
    from playsound import playsound  # To play sound effects
except:  # If module is not found on system
    print("The 'playsound' module was not found on your system. Attempting to install the module using pip.")
    os.system("pip install playsound")

SELECTED_MAP = "dino"  # Default map
ASSETS_MAPPING = {"dino": {
    'background': ['assets/General/poster.gif'],
    'text_color_1': 'black',
    'text_color_2': 'black',
    'text_color_3': 'gray',
    'y_level': -200,
    'soundtrack': 'assets/General/soundtrack.wav',
    'default_sprite': 'assets/ClassicMap/DinoIdle.gif',
    'run': ["assets/ClassicMap/DinoLeftUp.gif", "assets/ClassicMap/DinoRightUp.gif"],
    'duck': ["assets/ClassicMap/DinoDuckLeftUp.gif", "assets/ClassicMap/DinoDuckRightUp.gif"],
    'jump': ["assets/ClassicMap/DinoIdle.gif"],
    'bird': ["assets/ClassicMap/BirdFlapUp.gif", "assets/ClassicMap/BirdFlapDown.gif"],
    'obstacles': ['assets/ClassicMap/1Big.gif', 'assets/ClassicMap/1Small.gif', 'assets/ClassicMap/2Big.gif',
                  'assets/ClassicMap/2Big1Small1Big.gif',
                  'assets/ClassicMap/2Small.gif', 'assets/ClassicMap/3Big.gif', 'assets/ClassicMap/3Small.gif']
},
    "forest": {
        'background': [f'assets/ForestMap/Background/Forest{n}.gif' for n in range(1, 300)],
        'text_color_1': 'white',
        'text_color_2': 'white',
        'text_color_3': 'red',
        'y_level': -400,
        'soundtrack': 'assets/General/ForestSoundtrack.wav',
        'default_sprite': 'assets/ForestMap/run1.gif',
        'run': [f"assets/ForestMap/run{n}.gif" for n in range(2, 13, 2)],
        'duck': [f"assets/ForestMap/duck{n}.gif" for n in range(1, 5)],
        'jump': ["assets/ForestMap/jump.gif"],
        'bird': ["assets/ForestMap/bird flap up.gif", "assets/ForestMap/bird flap down.gif"],
        'obstacles': ['assets/ForestMap/rock 1.gif', 'assets/ForestMap/rock 2.gif', 'assets/ForestMap/rock 3.gif',
                      'assets/ForestMap/rock 4.gif', 'assets/ForestMap/Logs.gif', 'assets/ForestMap/Barrel2.gif',
                      'assets/ForestMap/Snake.gif', 'assets/ForestMap/TreeStump.gif']
    },
    "suburb": {
        'background': [f'assets/SuburbMap/Background/Suburb{n}.gif' for n in range(1, 360)],
        'text_color_1': 'red',
        'text_color_2': 'red',
        'text_color_3': 'black',
        'y_level': -190,
        'soundtrack': 'assets/General/SuburbSoundtrack.wav',
        'default_sprite': 'assets/SuburbMap/idle.gif',
        'run': [f"assets/SuburbMap/run {n}.gif" for n in range(1, 7)],
        'duck': ["assets/SuburbMap/duck 1.gif", "assets/SuburbMap/duck 2.gif", "assets/SuburbMap/duck 3.gif"],
        'jump': ["assets/SuburbMap/sonic jump.gif"],
        'bird': ["assets/SuburbMap/Helicopter1.gif", "assets/SuburbMap/Helicopter2.gif"],
        'obstacles': ['assets/SuburbMap/FireDispenser.gif', 'assets/SuburbMap/Rocket1.gif',
                      'assets/SuburbMap/Rocket2.gif', 'assets/SuburbMap/Barrel1.gif']
    }
}


def get_next(cur, asset):
    assets_list = ASSETS_MAPPING[SELECTED_MAP][asset]  # List of gifs for the asset type
    try:
        return assets_list[(assets_list.index(cur) + 1) % len(assets_list)]  # Next gif in assets list
    except:
        return assets_list[0]  # If first time (i.e. cur not found in assets_list)


def new_shape(file, hide=False):
    t = turtle.Turtle()
    t.shape(file)
    t.penup()
    if hide: t.hideturtle()
    return t


def jump():
    global JUMP, DUCK, SPEED
    if not JUMP:
        playsound("assets/General/jump sound.wav", block=False)
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
    global scorepen
    turtle.tracer(0, 0)

    high_score = get_high_score()
    if SCORE > high_score:
        high_score = SCORE

    try:
        scorepen.clear()
    except:
        scorepen = turtle.Turtle()
        scorepen.hideturtle()
        scorepen.penup()

    scorepen.goto(280, 420)
    scorepen.color(ASSETS_MAPPING[SELECTED_MAP]["text_color_1"])
    scorepen.write(f"HIGH:{high_score:05} SCORE:{SCORE:05}", align="center", font=("Press Start 2P", 25, "normal"))

    turtle.tracer(1, 1)


def update():
    global dino, bird, obstacles, paths, BIRD_YCORS, GAME_SPEED, JUMP, SPEED, SHAPE, UPDATES, SCORE, FIRSTGAME, stars, cloud, CLOUDSPEED

    start = time.time()
    if SELECTED_MAP == "suburb":
        GAME_SPEED = 10
    elif SCORE <= 1000:
        GAME_SPEED = (5 + SCORE // 300)  # Caps game speed at 8 so that the game does not get too fast and unplayable

    turtle.tracer(0, 0)

    if SELECTED_MAP != "dino" and UPDATES % 2 == 0:
        turtle.bgpic(get_next(turtle.bgpic(), "background"))

    if (UPDATES % 6.5 == 0) or (SELECTED_MAP == "suburb" and UPDATES % 4 == 0):  # To make this code execution a bit less frequent
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
                    turtle.update()
                    turtle.tracer(0, 0)
                    tutorialpen.clear()
                time.sleep(4)
                tutorialpen.clear()
                FIRSTGAME = False

        turtle.ontimer(update_score, 1)

        if DUCK:
            dino.shape(get_next(dino.shape(), "duck"))  # Switch to duck
        elif JUMP:
            dino.shape(get_next(dino.shape(), "jump"))  # Switch to jump
        else:
            dino.shape(get_next(dino.shape(), "run"))  # Switch gif so that it looks like character is running

        bird.shape(get_next(bird.shape(), "bird"))  # Switch bird gif for flapping

    if JUMP:
        if SELECTED_MAP == "suburb" or SELECTED_MAP == "forest":
            SPEED = SPEED - 18.2  # Gravity
        else:
            SPEED = SPEED - 13.2  # Gravity'
        dino.sety(dino.ycor() + SPEED / 8)  # Divide speed by 8 since we update every 8 ms to make the jump look more natural

        if dino.ycor() < ASSETS_MAPPING[SELECTED_MAP]["y_level"]:  # Stop jumping as dino has reached ground
            dino.sety(ASSETS_MAPPING[SELECTED_MAP]["y_level"])
            JUMP = False

    bird.setx(bird.xcor() - GAME_SPEED)

    if (bird.xcor() - 40 < dino.xcor() < bird.xcor() + 40) and (bird.ycor() - 90 < dino.ycor() < bird.ycor() + 90):
        if not (bird.ycor() == ASSETS_MAPPING[SELECTED_MAP]["y_level"] + 80 and DUCK):
            gameover()
            return

    if bird.xcor() < -515 and SCORE >= 100:
        if random.randint(500, 700) == 500:  # Randomise duration between birds
            if FIRSTGAME:
                bird.goto(obstacles[-1].xcor() + 1000, -120)  # Go a random distance after last obstacle at ducking position for tutorial
            else:
                bird.goto(obstacles[-1].xcor() + random.randint(1000, 1200), random.choice(BIRD_YCORS))  # Go a random distance after last obstacle at one of the possible y-coordinates

    for obstacle in obstacles:
        obstacle.setx(obstacle.xcor() - GAME_SPEED)

        if obstacle.distance(dino) < 55:
            gameover()
            return

        if obstacle.xcor() < -515:
            if bird.xcor() > 500 and obstacles[-1].xcor() < bird.xcor():
                obstacle.setx(bird.xcor() + random.randint(1000, 1200))
            else:
                obstacle.setx(obstacles[-1].xcor() + random.randint(350, 700))
            obstacle.shape(random.choice(ASSETS_MAPPING[SELECTED_MAP]["obstacles"]))
            obstacles.append(obstacles.pop(obstacles.index(obstacle)))

    if SELECTED_MAP in ["suburb", "dino"]:
        for path in paths:
            path.setx(path.xcor() - GAME_SPEED)
            if path.xcor() <= -1000:
                path.goto(1000, path.ycor())

    if SELECTED_MAP == "dino":  # Other maps have sky in their background gif
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
    ms_elapsed = int((time.time() - start) * 1000)

    if ms_elapsed > 8:
        turtle.ontimer(update, 0)
    else:
        turtle.ontimer(update, 8 - ms_elapsed)


def playmusic(file):
    while True:  # Repeat soundtrack until process is terminated
        playsound(file, block=True)


def gameover():
    global p, gameoverpen, SELECTED_MAP, SKIPPED
    p.terminate()
    playsound("assets/General/game over.wav", block=False)
    save_high_score()
    turtle.tracer(0, 0)

    try:
        gameoverpen.clear()
    except:
        gameoverpen = turtle.Turtle()
        gameoverpen.hideturtle()
        gameoverpen.penup()
    scorepen.clear()

    gameoverpen.goto(0, 200)
    gameoverpen.color(ASSETS_MAPPING[SELECTED_MAP]["text_color_2"])
    gameoverpen.write("GAME OVER", align="center", font=("Press Start 2P", 25, "normal"))

    gameoverpen.goto(0, 0)
    gameoverpen.color(ASSETS_MAPPING[SELECTED_MAP]["text_color_3"])
    gameoverpen.write("Click anywhere to play again.", align="center", font=("Press Start 2P", 15, "normal"))

    gameoverpen.goto(0, -60)
    gameoverpen.color(ASSETS_MAPPING[SELECTED_MAP]["text_color_3"])
    gameoverpen.write("Press escape to go back to main menu.", align="center", font=("Press Start 2P", 15, "normal"))

    turtle.tracer(1, 1)
    p = multiprocessing.Process(target=playmusic, args=('assets/General/TitleScreenSoundtrack.wav',))
    p.start()
    if SELECTED_MAP == "dino": SKIPPED = False
    turtle.onscreenclick(restart)
    turtle.onkey(lambda: title_screen(reset=True), "Escape")
    turtle.listen()


def restart(x, y):
    global paths, dino, bird, obstacles, obstacles_gifs, SCORE, JUMP, DUCK, UPDATES, SPEED, GAME_SPEED, SHAPE, scorepen, gameoverpen, CLOUDSPEED, stars, p
    p.terminate()
    playsound("assets/General/button pressed.wav", block=False)
    turtle.onscreenclick(None)
    turtle.onkey(None, "Escape")
    SCORE = 0
    JUMP = False
    DUCK = False
    CLOUDSPEED = random.randint(1, 4)
    UPDATES = 0
    SPEED = 0
    GAME_SPEED = 20
    SHAPE = ASSETS_MAPPING[SELECTED_MAP]["default_sprite"]

    turtle.tracer(0, 0)
    scorepen.clear()
    gameoverpen.clear()
    dino.goto(-400, ASSETS_MAPPING[SELECTED_MAP]["y_level"])
    bird.goto(-530, ASSETS_MAPPING[SELECTED_MAP]["y_level"] + 80)
    obstacles[0].goto(2000, ASSETS_MAPPING[SELECTED_MAP]["y_level"] - 50)
    obstacles[1].goto(2500, ASSETS_MAPPING[SELECTED_MAP]["y_level"] - 50)
    obstacles[2].shape(random.choice(ASSETS_MAPPING[SELECTED_MAP]["obstacles"]))
    obstacles[2].goto(3000, ASSETS_MAPPING[SELECTED_MAP]["y_level"] - 50)

    if SELECTED_MAP == "suburb":
        paths[0].goto(0, -450)
        paths[1].goto(1000, -450)

    if SELECTED_MAP == "dino":
        paths[0].goto(0, -300)
        paths[1].goto(1000, -300)
        cloud.goto(random.randint(-300, 400), random.randint(250, 450))
        for star in stars.keys():
            star.goto(random.randint(0, 500), random.randint(0, 500))  # Put star in random position

    turtle.tracer(1, 1)
    p = multiprocessing.Process(target=playmusic, args=(ASSETS_MAPPING[SELECTED_MAP]["soundtrack"],))
    p.start()
    update()


def init_game():
    global paths, dino, bird, obstacles, cloud, obstacles_gifs, screen, BIRD_YCORS, SCORE, JUMP, DUCK, UPDATES, SPEED, GAME_SPEED, SHAPE, scorepen, tutorialpen, FIRSTGAME, stars, CLOUDSPEED, p
    p = multiprocessing.Process(target=playmusic, args=(ASSETS_MAPPING[SELECTED_MAP]["soundtrack"],))
    p.start()
    # Initialise game variables
    SCORE = 0
    JUMP = False
    DUCK = False
    CLOUDSPEED = random.randint(1, 4)
    UPDATES = 0
    SPEED = 0
    GAME_SPEED = 20
    SHAPE = ASSETS_MAPPING[SELECTED_MAP]["default_sprite"]
    BIRD_YCORS = [ASSETS_MAPPING[SELECTED_MAP]["y_level"], ASSETS_MAPPING[SELECTED_MAP]["y_level"] + 200,
                  ASSETS_MAPPING[SELECTED_MAP]["y_level"] + 80]  # Different y-coordinates that the bird can fly at
    obstacles = []
    paths = []

    tutorialpen.clear()
    tutorialpen.color(ASSETS_MAPPING[SELECTED_MAP]["text_color_3"])

    turtle.tracer(0, 0)

    if SELECTED_MAP == "suburb":
        paths.append(new_shape("assets/SuburbMap/SuburbPath.gif"))  # Initialise first path sprite
        paths[0].goto(0, -450)
        paths.append(new_shape("assets/SuburbMap/SuburbPath.gif"))  # Initialise second path sprite
        paths[1].goto(1000, -450)

    dino = new_shape(ASSETS_MAPPING[SELECTED_MAP]["default_sprite"])  # Setup dino
    dino.goto(-400, ASSETS_MAPPING[SELECTED_MAP]["y_level"])
    bird = new_shape(ASSETS_MAPPING[SELECTED_MAP]["bird"][0])  # Setup bird
    bird.goto(-550, ASSETS_MAPPING[SELECTED_MAP]["y_level"] + 80)
    obstacles.append(new_shape(ASSETS_MAPPING[SELECTED_MAP]["obstacles"][0]))
    obstacles[0].goto(2000, ASSETS_MAPPING[SELECTED_MAP]["y_level"] - 50)
    obstacles.append(new_shape(ASSETS_MAPPING[SELECTED_MAP]["obstacles"][0]))
    obstacles[1].goto(2500, ASSETS_MAPPING[SELECTED_MAP]["y_level"] - 50)
    obstacles.append(new_shape(random.choice(ASSETS_MAPPING[SELECTED_MAP]["obstacles"])))
    obstacles[2].goto(3000, ASSETS_MAPPING[SELECTED_MAP]["y_level"] - 50)

    if SELECTED_MAP == "dino":  # Cloud and stars are not applicable for other maps.
        paths.append(new_shape("assets/ClassicMap/path.gif"))  # Initialise first path sprite
        paths[0].goto(0, -300)
        paths.append(new_shape("assets/ClassicMap/path.gif"))  # Initialise second path sprite
        paths[1].goto(1000, -300)
        cloud = new_shape("assets/ClassicMap/cloud.gif")
        cloud.goto(random.randint(-300, 400), random.randint(250, 450))  # Put cloud in random position
        stars = {}
        for i in range(1, 5):
            star = new_shape("assets/ClassicMap/star.gif")
            star.goto(random.randint(0, 500), random.randint(0, 500))  # Put star in random position
            stars[star] = i  # 'i' will be the speed of the star

    screen.onkey(jump, "space")
    screen.onkeypress(duck, "Down")
    screen.onkeyrelease(unduck, "Down")
    screen.listen()
    turtle.tracer(1, 1)
    update()


def skip_tutorial(*args):
    playsound("assets/General/button pressed.wav", block=False)
    global SKIPPED, FIRSTGAME
    SKIPPED = True  # To skip the storyline
    for t in turtle.turtles():  # Clear everything to start game
        t.hideturtle()
    turtle.onscreenclick(None)
    init_game()


def storyline(part=1):
    global tutorialpen, screen, path, babydino, dino, kingbird, SKIPPED, FIRSTGAME
    if SKIPPED: return
    FIRSTGAME = False

    if part == 1:
        turtle.tracer(0, 0)
        turtle.onscreenclick(skip_tutorial)
        tutorialpen = turtle.Turtle()
        tutorialpen.hideturtle()
        tutorialpen.penup()
        tutorialpen.goto(300, -400)
        tutorialpen.write("Click anywhere to skip.", align="center", font=("Press Start 2P", 15, "normal"))
        tutorialpen.goto(490, 350)

        path = new_shape("assets/ClassicMap/path.gif")
        path.goto(0, -300)

        dino = new_shape("assets/ClassicMap/DinoIdle.gif")
        dino.goto(-400, -200)
        babydino = new_shape("assets/ClassicMap/BabyDinoIdle.gif")
        babydino.goto(-330, -232)
        kingbird = new_shape("assets/ClassicMap/KingBirdFlapDownRight.gif")
        kingbird.goto(-560, 550)
        turtle.tracer(1, 1)
        turtle.ontimer(lambda: storyline(part=2), 2000)
    elif part == 2:
        babydino.speed(1)  # Baby dino walks forward
        turtle.delay(10)
        for i in range(200):
            babydino.forward(1)
            if i % 20 == 0:
                if babydino.shape() == "assets/ClassicMap/BabyDinoRightUp.gif":
                    babydino.shape("assets/ClassicMap/BabyDinoLeftUp.gif")
                else:
                    babydino.shape("assets/ClassicMap/BabyDinoRightUp.gif")
        babydino.shape("assets/ClassicMap/BabyDinoIdle.gif")
        turtle.ontimer(lambda: storyline(part=3), 3500)
    elif part == 3:
        playsound("assets/General/run.wav", block=False)
        turtle.tracer(1, 1)  # King bird swoops down on baby dino
        kingbird.speed(1)
        turtle.delay(8)
        kingbird.goto(babydino.pos())

        for i in range(800):  # Move baby dino and king bird together out of the frame to the right
            turtle.tracer(0, 0)
            babydino.goto(babydino.xcor() + 1, babydino.ycor() + 0.75)
            kingbird.goto(kingbird.xcor() + 1, kingbird.ycor() + 0.75)
            if i % 150 == 0:  # Flap wing of king bird
                if kingbird.shape() == "assets/ClassicMap/KingBirdFlapUpRight.gif":
                    kingbird.shape("assets/ClassicMap/KingBirdFlapDownRight.gif")
                else:
                    kingbird.shape("assets/ClassicMap/KingBirdFlapUpRight.gif")
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
            FIRSTGAME = True  # To skip the later tutorial
            turtle.ontimer(skip_tutorial, 4000)


def titlebutton_clicked(btnid):
    global SELECTED_MAP, background, startbtn, exitbtn, mapsbtn, obstacles_gifs, dino_gifs, bird_gifs, bg_gifs, storyline_gifs, p, s_time
    playsound("assets/General/button pressed.wav", block=False)
    turtle.tracer(0, 0)

    background.hideturtle()
    startbtn.hideturtle()
    exitbtn.hideturtle()
    mapsbtn.hideturtle()
    startbtn.onrelease(None)
    exitbtn.onclick(None)
    mapsbtn.onclick(None)
    if btnid == 0:  # Start button
        SELECTED_MAP = "dino"
        p.terminate()  # Stop music
        dino_gifs = ['assets/ClassicMap/DinoIdle.gif', 'assets/ClassicMap/DinoLeftUp.gif',
                     'assets/ClassicMap/DinoRightUp.gif', 'assets/ClassicMap/DinoDuckLeftUp.gif',
                     'assets/ClassicMap/DinoDuckRightUp.gif']
        bird_gifs = ["assets/ClassicMap/BirdFlapDown.gif", "assets/ClassicMap/BirdFlapUp.gif"]
        obstacles_gifs = ['assets/ClassicMap/1Big.gif', 'assets/ClassicMap/1Small.gif', 'assets/ClassicMap/2Big.gif',
                          'assets/ClassicMap/2Big1Small1Big.gif', 'assets/ClassicMap/2Small.gif',
                          'assets/ClassicMap/3Big.gif', 'assets/ClassicMap/3Small.gif']
        bg_gifs = ["assets/ClassicMap/cloud.gif", "assets/ClassicMap/star.gif"]
        storyline_gifs = ["assets/ClassicMap/BabyDinoIdle.gif", "assets/ClassicMap/KingBirdFlapDownLeft.gif",
                          "assets/ClassicMap/KingBirdFlapDownRight.gif",
                          "assets/ClassicMap/KingBirdFlapUpRight.gif", "assets/ClassicMap/KingBirdFlapUpLeft.gif",
                          "assets/ClassicMap/BabyDinoLeftUp.gif",
                          "assets/ClassicMap/BabyDinoRightUp.gif", "assets/ClassicMap/path.gif"]
        for gif in obstacles_gifs + dino_gifs + bird_gifs + bg_gifs + storyline_gifs:
            turtle.register_shape(gif)

        storyline()
    else:  # Maps button
        turtle.tracer(0, 0)
        background = new_shape("assets/General/MapsMenu.gif")
        background.goto(0, 0)
        turtle.tracer(1, 1)
        turtle.onscreenclick(choose_map)
        s_time = time.time()
        turtle.listen()


def choose_map(x, y):
    global SELECTED_MAP, tutorialpen, FIRSTGAME, SKIPPED, p
    if time.time() - s_time <= 0.5: return  # To prevent misclicks

    if -450 < x < -230 and -280 < y < 230:  # Classic map
        SELECTED_MAP = "dino"
        SKIPPED = False
        turtle.tracer(0, 0)
        titlebutton_clicked(0)
        return
    elif 230 < x < 460 and -280 < y < 210:
        FIRSTGAME = False
        SELECTED_MAP = "forest"
        gifs = ["assets/ForestMap/bird flap up.gif", 'assets/ForestMap/jump.gif',
                "assets/ForestMap/bird flap down.gif", 'assets/ForestMap/rock 1.gif',
                'assets/ForestMap/rock 2.gif', 'assets/ForestMap/rock 3.gif',
                'assets/ForestMap/rock 4.gif', 'assets/ForestMap/Logs.gif',
                'assets/ForestMap/Barrel2.gif', 'assets/ForestMap/Snake.gif',
                'assets/ForestMap/TreeStump.gif']
        gifs += [f"assets/ForestMap/run{n}.gif" for n in range(1, 13)]
        gifs += [f"assets/ForestMap/duck{n}.gif" for n in range(1, 5)]
    elif -115 < x < 115 and -220 < y < 125:
        FIRSTGAME = False
        SELECTED_MAP = "suburb"
        gifs = ["assets/SuburbMap/idle.gif", "assets/SuburbMap/Helicopter1.gif",
                "assets/SuburbMap/Helicopter2.gif", "assets/SuburbMap/SuburbPath.gif",
                'assets/SuburbMap/Barrel1.gif', 'assets/SuburbMap/FireDispenser.gif',
                'assets/SuburbMap/Rocket1.gif', 'assets/SuburbMap/Rocket2.gif',
                "assets/SuburbMap/duck 1.gif", "assets/SuburbMap/duck 2.gif",
                "assets/SuburbMap/duck 3.gif", "assets/SuburbMap/sonic jump.gif"]
        gifs += [f"assets/SuburbMap/run {n}.gif" for n in range(1, 7)]
    else:
        return

    p.terminate()  # Stop music
    playsound("assets/General/button pressed.wav", block=False)
    tutorialpen = turtle.Turtle()
    tutorialpen.hideturtle()
    tutorialpen.penup()
    screen.onclick(None)

    for gif in gifs:
        turtle.register_shape(gif)

    turtle.tracer(0, 0)
    background.hideturtle()
    startbtn.hideturtle()
    exitbtn.hideturtle()
    mapsbtn.hideturtle()
    startbtn.onrelease(None)
    exitbtn.onclick(None)
    mapsbtn.onclick(None)
    init_game()


def title_screen(reset=False):
    global background, startbtn, exitbtn, mapsbtn, gameoverpen, p
    if reset:
        playsound("assets/General/button pressed.wav", block=False)
        turtle.onscreenclick(None)
        turtle.onkey(None, "Escape")
        for t in turtle.turtles():  # Clear everything
            t.hideturtle()
        gameoverpen.clear()
        turtle.bgpic('nopic')
    else:
        p = multiprocessing.Process(target=playmusic, args=('assets/General/TitleScreenSoundtrack.wav',))
        p.start()
    turtle.tracer(0, 0)
    background = new_shape("assets/General/poster.gif")
    background.goto(0, 0)
    startbtn = new_shape("assets/General/StartBtn.gif")
    startbtn.goto(0, -100)
    startbtn.onrelease(lambda x, y: titlebutton_clicked(0))
    mapsbtn = new_shape("assets/General/MapsBtn.gif")
    mapsbtn.goto(0, -210)
    mapsbtn.onclick(lambda x, y: titlebutton_clicked(1))
    exitbtn = new_shape("assets/General/ExitBtn.gif")
    exitbtn.goto(0, -310)
    exitbtn.onclick(lambda x, y: on_close())
    turtle.tracer(1, 1)


def on_close():  # When window close button is clicked
    global p
    try:
        p.terminate()  # Stop the game soundtrack
        save_high_score()  # Save the current high score (if applicable)
    except:
        pass  # If it is prior to the game starting, save_high_score would cause an error
    finally:
        exit()  # End the program


if __name__ == '__main__':
    print("Loading game...")
    soundtrack_assets = {"https://github.com/Sachin-dot-py/DinoGame/blob/main/assets/General/ForestSoundtrack.wav?raw=true": "ForestSoundtrack.wav",
                         "https://github.com/Sachin-dot-py/DinoGame/blob/main/assets/General/SuburbSoundtrack.wav?raw=true": "SuburbSoundtrack.wav",
                         "https://github.com/Sachin-dot-py/DinoGame/blob/main/assets/General/TitleScreenSoundtrack.wav?raw=true": "TitleScreenSoundtrack.wav",
                         "https://github.com/Sachin-dot-py/DinoGame/blob/main/assets/General/soundtrack.wav?raw=true": "soundtrack.wav"}

    # Retrieve the soundtracks if it is not found in the directory
    dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], "assets", "General")
    for n, (url, filename) in enumerate(soundtrack_assets.items(), start=1):
        file_path = os.path.join(dir, filename)
        if not os.path.isfile(file_path):
            if n == 1: print("This might take a minute for the first time executing the game.\n0% Loaded.")
            urllib.request.urlretrieve(url, file_path)
            print(f"{int((n/4)*100)}% Loaded.")

    # Setup screen
    screen = turtle.Screen()
    screen.setup(1300, 600)
    screen.setworldcoordinates(-500, -500, 500, 500)
    screen.title("ERROR RUN - 404 Not Found")
    turtle.hideturtle()
    turtle.bgcolor("light gray")
    root = turtle.getcanvas().winfo_toplevel()  # Accessing root window element
    root.protocol("WM_DELETE_WINDOW", on_close)  # Setting function to be called when close window button is clicked

    general_gifs = ["assets/General/poster.gif", "assets/General/StartBtn.gif", "assets/General/ExitBtn.gif",
                    "assets/General/MapsBtn.gif", "assets/General/MapsMenu.gif"]
    for gif in general_gifs:
        turtle.register_shape(gif)

    SKIPPED = False
    title_screen()
    turtle.mainloop()
