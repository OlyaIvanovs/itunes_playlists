import turtle
import math


class Spiro():
    """A class that draws a spirograph."""

    def __init__(self, xc, yc, color, R, r, l):
        self.turtle = turtle.Turtle()
        self.turtle.shape('turtle')  # the cursor shape
        self.step = 5  # step in degrees
        self.drawing_complete = False  # drawing complete flag

        # Set the parameters
        self._set_params(xc, yc, color, R, r, l)

        # Innitialize the drawing
        self.restart()

    def _set_params(self, xc, yc, color, R, r, l):
        """Set up the spirograph's parameters."""
        self.xc, self.yc = xc, yc  # the coords of the curve's center
        # Store radiuses big(R) and small(r) circles
        self.R, self.r = int(R), int(r)
        self.l = l
        self.color = color
        # Reduce r/R to its smallest form by dividing with greatest common divisor(GCD)
        gcd_val = math.gcd(self.r, self.R)
        # periodicity of the curve (in n_rot revolutions the curve starts repeating itself)
        self.n_rot = self.r//gcd_val
        self.k = r/float(R)  # ratio of radii
        self.turtle.color(*color)  # set color
        self.angle = 0  # set current angle

    def restart(self):
        """Reset the drawing params and gets it ready for a redraw."""
        self.drawing_complete = False
        self.turtle.showturtle()
        # Go to the first point
        self.turtle.up()  # lift up the pen
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + 1*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - 1*k*math.sin((1-k)*a/k))
        # move turtle to an absolute position
        self.turtle.setpos(self.xc + x, self.yc + y)
        self.turtle.down()  # set the pen down

    def draw(self):
        """Draws the curve in one continuous line."""
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.n_rot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + 1*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - 1*k*math.sin((1-k)*a/k))
            self.turtle.setpos(self.xc + x, self.yc + y)
        # Drawing is done so hide the turtle cursor
        self.turtle.hideturtle()

    def update(self):
        """Update by one step"""
        # Skip the rest of the steps if done
        if self.drawing_complete:
            return
        self.a += self.step  # increment angle
        # Draw a step
        R, k, l = self.R, self.k, self.l
        # Set the angle
        a = math.radians(self.a)
        x = self.R*((1-k)*math.cos(a) + 1*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - 1*k*math.sin((1-k)*a/k))
        self.setpos(self.xc + x, self.yc + y)
        # Set the flag if drawing is complete
        if self.a >= 360*self.n_rot:
            self.drawing_complete = True
            self.turtle.hideturtle()  # hide cursor


def main():
    spiro = Spiro(0, 0, (0.0, 0.0, 0.0), 300, 100, 0.9)
    spiro.draw()
    turtle.mainloop()


if __name__ == '__main__':
    main()
