import turtle
def square(length):
    for squ in range(4):
        turtle.fd(length)
        turtle.right(90)
def triangle(size):
    for tri in range(3):
        turtle.forward(size)
        turtle.right(120)
def circle(radius,extent=360):
    turtle.circle(radius,extent)
def rectangle(length,breath):
    for rect in range(4):
        turtle.forward(length)
        turtle.right(90)
        turtle.forward(breath)
        turtle.right(90)
if __name__ == "__main__":
    turtle.speed(3)
    square(100)
    turtle.penup()
    turtle.goto(-150, 0)
    turtle.pendown()
    triangle(100)
    turtle.penup()
    turtle.goto(150, 0)
    turtle.pendown()
    circle(50)
    turtle.penup()
    turtle.goto(0, -150)
    turtle.pendown()
    rectangle(120, 60)
    turtle.done()