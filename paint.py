"""Paint, for drawing shapes.

Exercises
1. Add a color.            ✅ added 'V' -> violet
2. Complete circle.        ✅ done
3. Complete rectangle.     ✅ done
4. Complete triangle.      ✅ done (equilateral using first two clicks as base)
5. Add width parameter.    ✅ done (use '[' and ']' to change pen size)
"""

from turtle import *
from freegames import vector
from math import sqrt

# --- Drawing state (add width) ---
state = {'start': None, 'shape': None, 'width': 2}

def _apply_pen():
    """Apply current pen width before drawing."""
    pensize(state['width'])

def line(start, end):
    """Draw line from start to end."""
    _apply_pen()
    up()
    goto(start.x, start.y)
    down()
    goto(end.x, end.y)
    up()

def square(start, end):
    """Draw square from start to end using dx as side length (as in original)."""
    _apply_pen()
    up()
    goto(start.x, start.y)
    down()
    begin_fill()
    for count in range(4):
        forward(end.x - start.x)
        left(90)
    end_fill()
    up()

def circle(start, end):
    """Draw a filled circle with center at start and radius = distance(start, end)."""
    _apply_pen()
    # radius (euclidean distance)
    r = sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)
    if r <= 0:
        return
    up()
    # Move to the point directly below the center by r (turtle.circle draws from right)
    goto(start.x, start.y - r)
    setheading(0)
    down()
    begin_fill()
    turtle.circle(r)  # 'turtle' name exists because we imported '*', but this is explicit
    end_fill()
    up()

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

def triangle(start, end):
    """Draw a closed, filled equilateral triangle using (start,end) as the base."""
    _apply_pen()
    # Base vector and length
    dx = end.x - start.x
    dy = end.y - start.y
    L = sqrt(dx*dx + dy*dy)
    if L == 0:
        return

    # Midpoint of base
    mx = (start.x + end.x) / 2.0
    my = (start.y + end.y) / 2.0

    # Height of equilateral triangle
    h = (sqrt(3) / 2.0) * L

    # Unit perpendicular pointing "up" (positive y preference)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    if py < 0:
        px, py = -px, -py

    # Third vertex
    cx = mx + px * h
    cy = my + py * h

    up()
    goto(start.x, start.y)
    down()
    begin_fill()
    goto(end.x, end.y)
    goto(cx, cy)
    goto(start.x, start.y)
    end_fill()
    up()

def tap(x, y):
    """Store starting point or draw shape."""
    start = state['start']
    if start is None:
        state['start'] = vector(x, y)
    else:
        shape = state['shape']
        end = vector(x, y)
        shape(start, end)
        state['start'] = None

def store(key, value):
    """Store value in state at key."""
    state[key] = value

def inc_width():
    """Increase pen width."""
    state['width'] = min(state['width'] + 1, 30)

def dec_width():
    """Decrease pen width."""
    state['width'] = max(state['width'] - 1, 1)

# ---- Setup & keybindings ----
state['shape'] = line
setup(420, 420, 370, 0)
onscreenclick(tap)
listen()

# edit/undo
onkey(undo, 'u')

# colors (added Violet on 'V')
onkey(lambda: color('black'), 'K')
onkey(lambda: color('white'), 'W')
onkey(lambda: color('green'), 'G')
onkey(lambda: color('blue'), 'B')
onkey(lambda: color('red'), 'R')
onkey(lambda: color('violet'), 'V')  # NEW color

# shapes
onkey(lambda: store('shape', line), 'l')
onkey(lambda: store('shape', square), 's')
onkey(lambda: store('shape', circle), 'c')
onkey(lambda: store('shape', rectangle), 'r')
onkey(lambda: store('shape', triangle), 't')

# width controls (NEW)
onkey(inc_width, ']')
onkey(dec_width, '[')

done()
