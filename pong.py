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
def r_up_release():
    global r_hold_up; r_hold_up = False
def r_down_press():
    global r_hold_down; r_hold_down = True
def r_down_release():
    global r_hold_down; r_hold_down = False

# ========= Bind Keys =========
wn.listen()
wn.onkeypress(l_up_press, "w")
wn.onkeyrelease(l_up_release, "w")
wn.onkeypress(l_down_press, "s")
wn.onkeyrelease(l_down_release, "s")

wn.onkeypress(r_up_press, "Up")
wn.onkeyrelease(r_up_release, "Up")
wn.onkeypress(r_down_press, "Down")
wn.onkeyrelease(r_down_release, "Down")

# Optional: press 'q' to close the window
def quit_game():
    wn.bye()
wn.onkeypress(quit_game, "q")

# ========= Game Loop =========
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

    # ---- Paddle collisions ----
    # Right paddle
    if (340 < ball.xcor() < 350) and (abs(ball.ycor() - paddle_r.ycor()) < 50):
        ball.setx(340); ball.dx *= -1
    # Left paddle
    if (-350 < ball.xcor() < -340) and (abs(ball.ycor() - paddle_l.ycor()) < 50):
        ball.setx(-340); ball.dx *= -1

    time.sleep(DT)  # control frame rate