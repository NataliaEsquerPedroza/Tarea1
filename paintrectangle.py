from turtle import *
from freegames import vector
from math import sqrt

def rectangle(start, end):
    """Draw a closed, filled rectangle using opposite corners start and end."""
    _apply_pen()
    x1, y1 = start.x, start.y
    x2, y2 = end.x, end.y
    left_x = min(x1, x2)
    bottom_y = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)

    up()
    goto(left_x, bottom_y)
    setheading(0)
    down()
    begin_fill()
    forward(w); left(90)
    forward(h); left(90)
    forward(w); left(90)
    forward(h)
    end_fill()
    up()
