import turtle
import time
import sys
import pygame

#from playsound import playsound
pygame.mixer.init()
pygame.mixer.music.load("bounce-8111.mp3")

print("lets play a game, grab someone or use both hands")
print(" ")
time.sleep(2)
print("This is Pong, created by yours truly, Mr Singh")
print(" ")
time.sleep(3)
print("W-up, S-down, Player 1")
time.sleep(2.5)
print("Up arrow key and Down arrow key, Player 2")
print(" ")
time.sleep(2.5)
print("Wanna play? Its first to 7, Y/N")
answer = input().lower()


def ping():
    if answer == "y":
        win = turtle.Screen()
        win.title("Pong Made By Adit")
        turtle.Screen().bgcolor("black")
        win.setup(width=900, height=600)
        win.tracer(0)

        score_1 = 0
        score_2 = 0

        ui = turtle.Turtle()
        ui.speed(0)
        ui.color("white")
        ui.penup()
        ui.hideturtle()
        ui.goto(0, 0)
        ui = turtle.textinput("Choose Difficlty Level", "EASY, MEDIUM, HARD").lower()
        print(ui)

        paddle_1 = turtle.Turtle()
        paddle_1.speed(100)
        paddle_1.shape("square")
        paddle_1.color("white")
        paddle_1.shapesize(stretch_wid=5, stretch_len=1)
        paddle_1.penup()
        paddle_1.goto(-400, 0)

        paddle_2 = turtle.Turtle()
        paddle_2.speed(100)
        paddle_2.shape("square")
        paddle_2.color("white")
        paddle_2.shapesize(stretch_wid=5, stretch_len=1)
        paddle_2.penup()
        paddle_2.goto(400, 0)

        ball = turtle.Turtle()
        ball.speed(0)
        ball.shape("square")
        ball.color("white")
        ball.penup()
        ball.goto(0, 0)
        ball.dx = 0.1
        ball.dy = 0.1

        # simple discretised minimax for paddle 2 (ai)
        search_depth = 1
        if ui == "easy":
            search_depth = 1
        if ui == "medium":
            search_depth = 2
        if ui == "hard":
            search_depth = 3

        if ui == "medium":
            ball.dx = 0.5
            ball.dy = 0.5

        if ui == "hard":
            ball.dx = 0.7
            ball.dy = 0.7

        print(f"speed = {ball.dx}, {ball.dy}")
        print(f"you are on {ui} mode, watch out, get ready, fingers on designated keys")
        time.sleep(4)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)

        pen = turtle.Turtle()
        pen.speed(0)
        pen.color("white")
        pen.hideturtle()
        pen.penup()
        pen.goto(0, 200)
        pen.write("Player 1:0  Player 2:0", align="center", font=("Courier", 28, "italic"))

        def paddle_1_up():
            y = paddle_1.ycor()
            y += 20
            paddle_1.sety(y)

        def paddle_1_down():
            y = paddle_1.ycor()
            y -= 20
            paddle_1.sety(y)

        def paddle_2_up():
            y = paddle_2.ycor()
            y += 20
            paddle_2.sety(y)

        def paddle_2_down():
            y = paddle_2.ycor()
            y -= 20
            paddle_2.sety(y)

        def clamp_paddle(y):
            if y > 260:
                y = 260
            if y < -260:
                y = -260
            return y

        def discretise(value, step):
            return round(value / step) * step

        def evaluate_state(bx, by, dx, dy, paddle_y):
            # keep paddle near ball and prefer being on the right side of its flight
            dist = abs(by - paddle_y)
            heading = 1 if dx > 0 else -1
            aim_bonus = -dist if heading > 0 else 0
            edge_penalty = 50 if bx > 380 and heading > 0 else 0
            return aim_bonus - dist - edge_penalty

        def next_ball(bx, by, dx, dy):
            bx += dx
            by += dy
            if by > 290:
                by = 290
                dy *= -1
            if by < -290:
                by = -290
                dy *= -1
            return bx, by, dx, dy

        def minimax(bx, by, dx, dy, paddle_y, depth, alpha, beta, maximizing):
            bx = discretise(bx, 10)
            by = discretise(by, 10)
            dx = discretise(dx, 0.1)
            dy = discretise(dy, 0.1)
            paddle_y = discretise(paddle_y, 10)

            if depth == 0 or bx > 430 or bx < -430:
                return evaluate_state(bx, by, dx, dy, paddle_y)

            if maximizing:
                best = -1e9
                for move in (-20, 0, 20):
                    new_paddle = clamp_paddle(paddle_y + move)
                    nbx, nby, ndx, ndy = next_ball(bx, by, dx, dy)
                    # bounce off paddle if we are in range in this simulation
                    if nbx > 390 and (new_paddle - 50 < nby < new_paddle + 40):
                        nbx = 390
                        ndx *= -1
                    score = minimax(nbx, nby, ndx, ndy, new_paddle, depth - 1, alpha, beta, False)
                    if score > best:
                        best = score
                    if best > alpha:
                        alpha = best
                    if beta <= alpha:
                        break
                return best
            else:
                worst = 1e9
                for move in (-20, 0, 20):
                    new_paddle = clamp_paddle(paddle_y + move)
                    nbx, nby, ndx, ndy = next_ball(bx, by, dx, dy)
                    if nbx < -390:
                        nbx = -390
                        ndx *= -1
                    score = minimax(nbx, nby, ndx, ndy, new_paddle, depth - 1, alpha, beta, True)
                    if score < worst:
                        worst = score
                    if worst < beta:
                        beta = worst
                    if beta <= alpha:
                        break
                return worst

        def ai_move():
            best_move = 0
            best_score = -1e9
            for move in (-20, 0, 20):
                new_paddle = clamp_paddle(paddle_2.ycor() + move)
                nbx, nby, ndx, ndy = next_ball(ball.xcor(), ball.ycor(), ball.dx, ball.dy)
                if nbx > 390 and (new_paddle - 50 < nby < new_paddle + 40):
                    nbx = 390
                    ndx *= -1
                score = minimax(nbx, nby, ndx, ndy, new_paddle, search_depth, -1e9, 1e9, True)
                if score > best_score:
                    best_score = score
                    best_move = move
            paddle_2.sety(clamp_paddle(paddle_2.ycor() + best_move))

        win.listen()
        win.onkeypress(paddle_1_up, "w")
        win.onkeypress(paddle_1_down, "s")

        while True:
            try:
                win.update()
                ai_move()
                ball.setx(ball.xcor() + ball.dx)
                ball.sety(ball.ycor() + ball.dy)
            except turtle.Terminator:
                break  #window closed, stop loop

            if ball.ycor() > 290:
                ball.sety(290)
                ball.dy *= -1
                pygame.mixer.music.play()

            if ball.ycor() < -290:
                ball.sety(-290)
                ball.dy *= -1
                pygame.mixer.music.play()

            if ball.xcor() > 430:
                ball.goto(0, 0)
                ball.dx *= -1
                score_1 += 1
                pen.clear()
                pen.write("Player 1:{}  Player 2:{}".format(score_1, score_2),
                          align="center", font=("Courier", 28, "italic"))
                pygame.mixer.music.play()

            if ball.xcor() < -430:
                ball.goto(0, 0)
                ball.dx *= -1
                score_2 += 1
                pen.clear()
                pen.write("Player 1:{}  Player 2:{}".format(score_1, score_2),
                          align="center", font=("Courier", 28, "italic"))
                pygame.mixer.music.play()

            if ball.xcor() > 390 and (paddle_2.ycor() - 50 < ball.ycor() < paddle_2.ycor() + 40):
                ball.setx(390)
                ball.dx *= -1
                pygame.mixer.music.play()

            if ball.xcor() < -390 and (paddle_1.ycor() - 50 < ball.ycor() < paddle_1.ycor() + 40):
                ball.setx(-390)
                ball.dx *= -1
                pygame.mixer.music.play()

            if score_1 == 7:
                time.sleep(2)
                pen.clear()
                pen.write(f"well done player 1, you won, better luck next time player 2   {score_1}:{score_2}",
                          align="center", font=("Courier", 18, "italic"))
                time.sleep(7)
                turtle.clearscreen()
                restart = turtle.Turtle()
                restart.speed(0)
                restart.color("white")
                restart.penup()
                restart.hideturtle()
                restart.goto(0, 0)
                restart = turtle.textinput("Y/N", "Woul You Like To Play Again?").lower()
                if restart == "y":
                    ping()
                else:
                    print("alrighty, farewell")
                    exit()

            elif score_2 == 7:
                time.sleep(2)
                pen.clear()
                pen.write(f"well done player 2, you won, better luck next time player 1   {score_2}:{score_1}",
                          align="center", font=("Courier", 18, "italic"))
                time.sleep(7)
                turtle.clearscreen()
                restart = turtle.Turtle()
                restart.speed(0)
                restart.color("white")
                restart.penup()
                restart.hideturtle()
                restart.goto(0, 0)
                restart = turtle.textinput("Y/N", "Woul You Like To Play Again?").lower()
                if restart == "y":
                    ping()
                else:
                    print("alrighty, farewell")
                    exit()

    if answer == "n":
        print("come again, goodbye")


ping()
