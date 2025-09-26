# pong_smooth.py — Pong with smooth paddle movement (Python turtle)

import turtle
import time

# ========= Screen =========
wn = turtle.Screen()
wn.title("Pong (smooth)")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # we will call wn.update() each frame

# ========= Settings & State =========
PADDLE_SPEED = 10     # pixels per frame for paddles
DT = 0.01             # frame delay (lower = faster)
# ========= Settings & State =========
PADDLE_SPEED = 10     # pixels per frame for paddles
DT = 0.01             # frame delay (lower = faster)

left_score = 0
right_score = 0

# key-hold flags (must exist before handlers use them)
l_hold_up = False
l_hold_down = False
r_hold_up = False
r_hold_down = False

# ========= Helpers =========
def make_paddle(x):
    p = turtle.Turtle()
    p.speed(0)
    p.shape("square")
    p.color("white")
    p.shapesize(stretch_wid=5, stretch_len=1)  # 20px * 5 = 100px tall
    p.penup()
    p.goto(x, 0)
    return p

def clamp_paddle(p):
    """Keep paddle on screen."""
    y = max(-250, min(250, p.ycor()))
    p.sety(y)

def clamp_paddle(p):
    """Keep paddle on screen."""
    y = max(-250, min(250, p.ycor()))
    p.sety(y)

# ========= Scoreboard =========
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 260)

def update_scoreboard():
    score_pen.clear()
    score_pen.write(f"{left_score} : {right_score}", align="center", font=("Courier", 24, "normal"))

update_scoreboard()

# ========= Paddles & Ball =========
paddle_l = make_paddle(-350)
paddle_r = make_paddle(350)

ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 3
ball.dy = 3

# ========= Key Handlers (press/release set flags) =========
def l_up_press():
    global l_hold_up; l_hold_up = True
def l_up_release():
    global l_hold_up; l_hold_up = False
def l_down_press():
    global l_hold_down; l_hold_down = True
def l_down_release():
    global l_hold_down; l_hold_down = False

def r_up_press():
    global r_hold_up; r_hold_up = True
@@ -89,39 +106,47 @@ wn.onkeypress(quit_game, "q")
while True:
    wn.update()

    # ---- Smooth paddle motion based on held keys ----
    l_v = (PADDLE_SPEED if l_hold_up else 0) - (PADDLE_SPEED if l_hold_down else 0)
    r_v = (PADDLE_SPEED if r_hold_up else 0) - (PADDLE_SPEED if r_hold_down else 0)

    if l_v:
        paddle_l.sety(paddle_l.ycor() + l_v)
        clamp_paddle(paddle_l)
    if r_v:
        paddle_r.sety(paddle_r.ycor() + r_v)
        clamp_paddle(paddle_r)

    # ---- Ball movement ----
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # ---- Wall bounce (top/bottom) ----
    if ball.ycor() > 290:
        ball.sety(290); ball.dy *= -1
    if ball.ycor() < -290:
        ball.sety(-290); ball.dy *= -1

    # ---- Missed paddles → reset ----
    if ball.xcor() > 390:
        ball.goto(0, 0); ball.dx *= -1
    if ball.xcor() < -390:
        ball.goto(0, 0); ball.dx *= -1
    if ball.xcor() > 390:
        left_score += 1
        update_scoreboard()
        ball.goto(0, 0)
        ball.dx *= -1
        time.sleep(0.2)
    if ball.xcor() < -390:
        right_score += 1
        update_scoreboard()
        ball.goto(0, 0)
        ball.dx *= -1
        time.sleep(0.2)

    # ---- Paddle collisions ----
    # Right paddle
    if (340 < ball.xcor() < 350) and (abs(ball.ycor() - paddle_r.ycor()) < 50):
        ball.setx(340); ball.dx *= -1
    # Left paddle
    if (-350 < ball.xcor() < -340) and (abs(ball.ycor() - paddle_l.ycor()) < 50):
        ball.setx(-340); ball.dx *= -1

    time.sleep(DT)  # control frame rate
