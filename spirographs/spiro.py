import turtle
import math
import random
import argparse
from datetime import datetime
from PIL import Image


class Spiro():
    """A class that draws a spirograph."""

    def __init__(self, xc, yc, color, R, r, l):
        self.turtle = turtle.Turtle()
        self.turtle.shape('turtle')  # the cursor shape
        self.step = 5  # step in degrees
        self.drawing_complete = False  # drawing complete flag
        # Set the parameters
        self.set_params(xc, yc, color, R, r, l)
        # Innitialize the drawing
        self.restart()

    def set_params(self, xc, yc, color, R, r, l):
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
        self.angle += self.step  # increment angle
        # Draw a step
        R, k, l = self.R, self.k, self.l
        # Set the angle
        a = math.radians(self.angle)
        x = self.R*((1-k)*math.cos(a) + 1*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - 1*k*math.sin((1-k)*a/k))
        self.turtle.setpos(self.xc + x, self.yc + y)
        # Set the flag if drawing is complete
        if self.angle >= 360*self.n_rot:
            self.drawing_complete = True
            self.turtle.hideturtle()  # hide cursor

    def clear(self):
        """Clear the curve"""
        self.turtle.clear()


class SpiroAnimator:
    """Class for animating spirographs"""

    def __init__(self, n):
        self.delta_t = 10  # timer value in milliseconds
        # Get the window's dimensions
        self.window_width = turtle.window_width()
        self.window_height = turtle.window_height()
        # create the spiro objects
        self.spiros = []
        for i in range(n):
            # Generate random params
            rparams = self._get_random_params()
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        turtle.ontimer(self.update, self.delta_t)

    def _get_random_params(self):
        """Generate random parameters."""
        R = random.randint(50, min(self.window_width, self.window_height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-self.window_width//2, self.window_width//2)
        yc = random.randint(-self.window_height//2, self.window_height//2)
        color = (random.random(), random.random(), random.random())
        return (xc, yc, color, R, r, l)

    def restart(self):
        """Restart spiro drawing programm."""
        for spiro in self.spiros:
            spiro.clear()
            rparams = self._get_random_params()
            spiro.set_params(*rparams)
            spiro.restart()

    def update(self):
        """Update all spiros."""
        completed = 0  # the number of spiros being drawn
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawing_complete:
                completed += 1
        # Restart if all spiros are complete
        if completed == len(self.spiros):
            self.restart()
        turtle.exitonclick()
        turtle.ontimer(self.update, self.delta_t)

    def toggle_turtles(self):
        """Toggle the turtle cursor on and off."""
        for spiro in self.spiros:
            if spiro.turtle.isvisible():
                spiro.turtle.hideturtle()
            else:
                spiro.turtle.showturtle()


def save_drawings():
    """Save drawings as PNG files"""
    turtle.hideturtle()
    # Generate unique filenames
    date_str = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    filename = 'spiro' + date_str
    print(f"Saving drawing to {filename}.eps/png")
    # Get tkinter canvas
    canvas = turtle.getcanvas()
    # save the drawing as a postscript image
    canvas.postscript(file=f"{filename}.eps")
    # Use Pillow to convert the postscript image file to PNG
    img = Image.open(f"{filename}.eps")
    img.save(f"{filename}.png", 'png')
    # Show the turtle cursor
    turtle.showturtle()


def main():
    print("generating spirograph...")
    # Create parser
    desc_str = """
    This program draws Spirographs using the Turtle module.
    When run with no arguments, this program draws randow Spirographs.
    R: radius of outer circle
    r: radius of inner circle
    l: ratio of hole distance to r
    """
    parser = argparse.ArgumentParser(description=desc_str)
    parser.add_argument('--sparams', nargs=3, dest='sparams',
                        required=False, help="The three args in sparams: R, r, l.")
    args = parser.parse_args()

    # Set up turtle params
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title("Spirographs!")
    # Add the key handle to save our drawings
    turtle.onkey(save_drawings, "s")
    turtle.listen()
    turtle.hideturtle()

    # Check for any arguments sparams and draw Spirograph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        color = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, color, *params)
        spiro.draw()
    else:
        # Create the animation object
        spiro_anim = SpiroAnimator(4)
        turtle.onkey(spiro_anim.toggle_turtles, "t")  # toggle turtles on t
        turtle.onkey(spiro_anim.restart, "w")  # restart on space

    # Start the turtle main loop
    turtle.mainloop()


if __name__ == '__main__':
    main()
