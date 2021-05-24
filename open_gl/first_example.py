import os
import glfw

# import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
"""GLUT is the OpenGL Utility Toolkit, a window system independent toolkit 
for writing OpenGL programs. It implements a simple windowing application 
programming interface (API) for OpenGL. GLUT makes it considerably easier 
to learn about and explore OpenGL Programming."""


class RenderWindow:
    """GLFW Rendering window class."""

    def __init__(self):
        # Save current working directory
        cwd = os.getcwd()

        # Initialize glfw
        glfw.init()

        # Restore cwd
        os.chdir(cwd)

        # Version hints
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE,
                         glfw.OPENGL_CORE_PROFILE)

        # Make window
        self.width, self.height = 640, 480
        self.aspect = self.width/float(self.height)
        self.win = glfw.create_window(
            self.width, self.height, 'Simpleglfw', None, None)

        # Make the context current
        glfw.make_context_current(self.win)

        # Initialize GL
        glViewport(0, 0, self.width, self.height)  # Set the viewport
        # update the depth buffer, it is not updated if the depth test is disabled.
        glEnable(GL_DEPTH_TEST)
        # Specify clear values for the color buffers
        glClearColor(0.5, 0.5, 0.5, 1.0)

        # Register some event callbacks for user interface
        glfw.set_mouse_button_callback(self.win, self.on_mouse_button)
        glfw.set_key_callback(self.win, self.on_keyboard)
        glfw.set_window_size_callback(self.win, self.on_size)

    def on_mouse_button(self, win, button, action, mods):
        """print 'mouse_button: ' win, button, action, mods"""
        pass

    def on_keyboard(self, win, key, scancode, action, mods):
        """Called every time a keyboard event happens."""
        if action == glfw.PRESS:
            # ESC to quit
            if key == glfw.KEY_ESCAPE:
                self.exit_now = True
            else:
                # toggle cut
                # will be passed to the fragment shader
                self.scene.show_circle = not self.scene.show_circle

    def on_size(self, win, width, height):
        """Handler for the window-resizing event."""
        self.width = width
        self.height = height
        self.aspect = width/float(height)
        glViewport(0, 0, self.width, self.height)


# Using GLUT
def draw():
    # clear buffers to preset values
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glutSwapBuffers()


def main2():
    """"""
    width, height = 500, 400

    glutInit()  # initialize the GLUT library.
    glutInitDisplayMode(GLUT_RGBA)  # sets the initial display mode.
    glutInitWindowSize(width, height)
    # set the initial window position and size respectively.
    glutInitWindowPosition(200, 200)
    window = glutCreateWindow("Open Window in Python")
    glutDisplayFunc(draw)
    glutIdleFunc(draw)  # sets the global idle callback
    glutMainLoop()  # enters the GLUT event processing loop.


def main():
    """"""
    rw = RenderWindow()


if __name__ == "__main__":
    main()
