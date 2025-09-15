"""
Paint (Turtle) — Modified for assignment
----------------------------------------
Based on Grant Jenks' Free Python Games "paint" example.
This version is self-contained (no external dependencies) and adds:
  • A new color ("violet") bound to key "v".
  • Circle drawing mode ("c"): click once to set center, click again to set radius.
  • Completed/closed & filled rectangle ("r") drawn from first corner to opposite corner.
  • Completed/closed & filled triangle ("t") using the first two clicks as the base.
  • Square ("s") and line ("l") preserved; shapes are filled (except line).

Usage
-----
• Left click: 
    - 1st click: mark the starting point
    - 2nd click: draw the currently selected shape and reset
• Keys (colors):
    - k: black, w: white, g: green, b: blue, r: red, v: violet (NEW)
• Keys (shapes):
    - l: line, s: square, c: circle (NEW mode), r: rectangle (completed), t: triangle (completed)
• u: undo last turtle action

Documentation Standard
----------------------
- Module and function docstrings follow Google-style docstrings (PEP 257 aligned).
- Simple type hints are included.

Tested on Python 3.10+.
"""
from __future__ import annotations

import math
import turtle
from typing import Callable, Optional, Tuple

Point = Tuple[float, float]

# --- Global drawing state ---
start: Optional[Point] = None    # First click (varies by shape: corner, center, base start, etc.)
shape: str = 'line'              # Current shape key: 'line'|'square'|'circle'|'rectangle'|'triangle'
current_color: str = 'black'     # Current pen/fill color

# --- Helpers ---
def goto(p: Point) -> None:
    """Move turtle to a point without drawing.

    Args:
        p: (x, y) coordinates.
    """
    turtle.up()
    turtle.goto(p[0], p[1])
    turtle.down()


def set_color(name: str) -> None:
    """Set current pen and fill color.

    Args:
        name: Any turtle color name, e.g., 'red', 'violet'.
    """
    global current_color
    current_color = name
    turtle.color(current_color)


# --- Shape primitives ---
def draw_line(a: Point, b: Point) -> None:
    """Draw a line from a to b.

    Args:
        a: Start point.
        b: End point.
    """
    turtle.color(current_color)
    goto(a)
    turtle.down()
    turtle.begin_fill()  # Line has no fill but begin/end keeps API consistent
    turtle.goto(b[0], b[1])
    turtle.end_fill()
    turtle.up()


def draw_square(a: Point, b: Point) -> None:
    """Draw a filled, axis-aligned square using a as lower-left corner and side from a->b.

    Side length is max(|dx|, |dy|) so the square uses the larger span.

    Args:
        a: First click; one corner.
        b: Second click; determines side length.
    """
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    side = max(abs(dx), abs(dy))

    # Align so that a is treated as the lower-left corner
    x = a[0]
    y = a[1]
    if dx < 0:
        x = a[0] - side
    if dy < 0:
        y = a[1] - side

    turtle.color(current_color, current_color)
    goto((x, y))
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(side)
        turtle.left(90)
    turtle.end_fill()
    turtle.up()


def draw_rectangle(a: Point, b: Point) -> None:
    """Draw a completed, closed, filled rectangle using opposite corners a and b.

    Args:
        a: One corner (from first click).
        b: Opposite corner (from second click).
    """
    x1, y1 = a
    x2, y2 = b
    x_left = min(x1, x2)
    y_bottom = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    turtle.color(current_color, current_color)
    goto((x_left, y_bottom))
    turtle.begin_fill()
    turtle.setheading(0)
    turtle.forward(width)
    turtle.left(90)
    turtle.forward(height)
    turtle.left(90)
    turtle.forward(width)
    turtle.left(90)
    turtle.forward(height)
    turtle.end_fill()
    turtle.up()


def draw_circle(a: Point, b: Point) -> None:
    """Draw a filled circle with center at a and radius = distance(a, b).

    Args:
        a: Center point (first click).
        b: Any point to set the radius (second click).
    """
    cx, cy = a
    r = math.dist(a, b)
    if r <= 0:
        return

    turtle.color(current_color, current_color)
    # Move to the circle start point (center below by r) and draw
    goto((cx, cy - r))
    turtle.setheading(0)
    turtle.begin_fill()
    turtle.circle(r)
    turtle.end_fill()
    turtle.up()


def draw_triangle(a: Point, b: Point) -> None:
    """Draw a completed, closed, filled equilateral triangle using segment (a,b) as the base.

    The third vertex is computed so the triangle is equilateral, oriented by the base's
    perpendicular (chosen to point "up" relative to the screen).

    Args:
        a: Base start point.
        b: Base end point.
    """
    # Base vector and length
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    L = math.hypot(dx, dy)
    if L == 0:
        return

    # Midpoint of base
    mx = (a[0] + b[0]) / 2.0
    my = (a[1] + b[1]) / 2.0

    # Height of an equilateral triangle
    h = (math.sqrt(3) / 2.0) * L

    # Unit perpendicular (choose "up" so that positive y increases)
    # Base unit vector
    ux = dx / L
    uy = dy / L
    # Perpendiculars: (-uy, ux) and (uy, -ux)
    px, py = -uy, ux
    if py < 0:   # flip to favor upwards orientation
        px, py = -px, -py

    # Third vertex
    cx = mx + px * h
    cy = my + py * h

    turtle.color(current_color, current_color)
    turtle.up()
    goto(a)
    turtle.begin_fill()
    turtle.goto(b[0], b[1])
    turtle.goto(cx, cy)
    turtle.goto(a[0], a[1])  # close shape
    turtle.end_fill()
    turtle.up()


# --- Event handlers / UI ---
def on_click(x: float, y: float) -> None:
    """Mouse click handler. First click sets start; second click draws shape.

    Args:
        x: Mouse x-coordinate.
        y: Mouse y-coordinate.
    """
    global start
    if start is None:
        start = (x, y)
    else:
        end = (x, y)
        if shape == 'line':
            draw_line(start, end)
        elif shape == 'square':
            draw_square(start, end)
        elif shape == 'circle':
            draw_circle(start, end)
        elif shape == 'rectangle':
            draw_rectangle(start, end)
        elif shape == 'triangle':
            draw_triangle(start, end)
        start = None  # reset for next shape


def set_shape(name: str) -> Callable[[], None]:
    """Return a no-arg function that sets the current shape to `name` for key binding.

    Args:
        name: One of 'line', 'square', 'circle', 'rectangle', 'triangle'.

    Returns:
        A lambda suitable for turtle.onkey.
    """
    def _setter() -> None:
        global shape
        shape = name
    return _setter


# --- App bootstrap ---
def main() -> None:
    """Initialize turtle screen, register key bindings, and start the mainloop."""
    turtle.setup(width=800, height=600)
    turtle.title("Paint — Modified (Turtle)")
    turtle.hideturtle()
    turtle.speed(0)        # fastest
    turtle.tracer(False)   # draw instantly
    turtle.colormode(255)
    set_color('black')

    screen = turtle.Screen()
    screen.onclick(on_click)

    # Color key bindings
    turtle.onkey(lambda: set_color('black'), 'k')
    turtle.onkey(lambda: set_color('white'), 'w')
    turtle.onkey(lambda: set_color('green'), 'g')
    turtle.onkey(lambda: set_color('blue'), 'b')
    turtle.onkey(lambda: set_color('red'), 'r')
    turtle.onkey(lambda: set_color('violet'), 'v')  # NEW

    # Shape key bindings
    turtle.onkey(set_shape('line'), 'l')
    turtle.onkey(set_shape('square'), 's')
    turtle.onkey(set_shape('circle'), 'c')       # NEW
    turtle.onkey(set_shape('rectangle'), 'r')
    turtle.onkey(set_shape('triangle'), 't')

    # Utilities
    turtle.onkey(turtle.undo, 'u')
    turtle.listen()
    turtle.update()
    turtle.mainloop()


if __name__ == '__main__':
    main()