import os
import glfw
import numpy
import math

import glutils

import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
"""GLUT is the OpenGL Utility Toolkit, a window system independent toolkit 
for writing OpenGL programs. It implements a simple windowing application 
programming interface (API) for OpenGL. GLUT makes it considerably easier 
to learn about and explore OpenGL Programming."""

# Uniform variables are used to communicate with your vertex or fragment shader from "outside"

str_vector_shader = """
#version 330 core

layout(location = 0) in vec3 aVert; // vertex atribute

// declare uniform variables
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform float uTheta; // rotation angle

out vec2 vTexCoord;

void main() {
    // rotation transform
    mat4 rot = mat4(
        vec4(cos(uTheta), sin(uTheta), 0.0, 0.0),
        vec4(-sin(uTheta), cos(uTheta), 0.0, 0.0),
        vec4(0.0, 0.0, 1.0, 0.0),
        vec4(0.0, 0.0, 0.0, 1.0)
    );
    // transform vertex
    gl_Position = uPMatrix * uMVMatrix * rot * vec4(aVert, 1.0);
    // Set texture coordinate
    vTexCoord = aVert.xy + vec2(0.5, 0.5);
}
"""

str_fragment_shader = """
#version 330 core

in vec2 vTexCoord;

uniform sampler2D tex2D;
uniform bool showCircle;

out vec4 fragColor;

void main() {
    if (showCircle) {
        // discard fragment outside circle
        if (distance(vTexCoord, vec2(0.5, 0.5)) > 0.5) {
            discard;
        }
        else {
            fragColor = texture(tex2D, vTexCoord);
        }
    } else {
        fragColor = texture(tex2D, vTexCoord);
    }
}
"""


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

        # Create 3D
        self.scene = Scene()

        # Exit Flag
        self.exit_now = False

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

    def run(self):
        """Main loop"""
        glfw.set_time(0)  # resets the GLFW timer to 0
        t = 0.0  # timer to redraw the graphics at regular intervals
        while not glfw.window_should_close(self.win) and not self.exit_now:
            # Update every x seconds
            curr_time = glfw.get_time()
            if curr_time - t > 0.1:  # change 0.1 to adjust the rendering frame rate
                # Update time
                t = curr_time
                # Clear and get ready for the next frame
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # Build projection matrix
                p_matrix = glutils.perspective(45.0, self.aspect, 0.1, 100.0)
                mv_matrix = glutils.lookAt(
                    [0.0, 0.0, -2.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0])

                # render
                self.scene.render(p_matrix, mv_matrix)
                self.scene.step()

                glfw.swap_buffers(self.win)
                # Checks for any UI events
                glfw.poll_events()

        glfw.terminate()


class Scene:
    """Initializing and drawing the 3D geometry."""

    def __init__(self):
        # Compile and load the shaders.
        self.program = glutils.loadShaders(
            str_vector_shader, str_fragment_shader)

        glUseProgram(self.program)

        # Connect the variables in the Python code with those in the shaders
        # Returns the location of a uniform variable
        self.p_matrix_uniform = glGetUniformLocation(self.program, 'uPMatrix')
        self.mv_matrix_uniform = glGetUniformLocation(
            self.program, 'uMVMatrix')

        # Texture
        self.tex2D = glGetUniformLocation(self.program, 'tex2D')

        # Define triangle strip vertices
        vertex_data = numpy.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            -0.5, 0.5, 0.0,
            0.5, 0.5, 0.0,
        ], numpy.float32)

        # Set up vertex array object(VAO)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        # Vertices
        self.vertex_buffer = glGenBuffers(1)  # Create VBO
        # VBO is a memory buffer in the high speed memory of your video card
        # designed to hold information about vertices
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        # Set buffer data
        glBufferData(GL_ARRAY_BUFFER, 4*len(vertex_data),
                     vertex_data, GL_STATIC_DRAW)
        # Enable vertex array
        glEnableVertexAttribArray(0)
        # Set buffer data pointer
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        # Unbind VAO
        glBindVertexArray(0)
        # Loads the image as an OpenGL texture
        self.tex_id = glutils.loadTexture('star.png')

        self.t = 0  # time
        self.show_circle = False

    def step(self):
        """Update variables to make the square rotate."""
        # Increment angle
        self.t = (self.t + 1) % 360
        # Set shader angle in radians
        glUniform1f(glGetUniformLocation(
            self.program, 'uTheta'), math.radians(self.t))  # set angle in the shader program

    def render(self, p_matrix, vm_matrix):
        # Use shader
        glUseProgram(self.program)  # use shader program

        # Set projection matrix
        glUniformMatrix4fv(self.p_matrix_uniform, 1, GL_FALSE, p_matrix)

        # Set modelview matrix
        glUniformMatrix4fv(self.mv_matrix_uniform, 1, GL_FALSE, vm_matrix)

        # Show circle? set the current value of show_circle in the fragment shader
        glUniform1i(glGetUniformLocation(
            self.program, 'showCircle'), self.show_circle)

        # Enable texture
        glActiveTexture(GL_TEXTURE0)  # activate texture unit 0
        glBindTexture(GL_TEXTURE_2D, self.tex_id)
        glUniform1i(self.tex2D, 0)

        # Bind VAO
        glBindVertexArray(self.vao)
        # Draw
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        # Unbind VAO
        glBindVertexArray(0)


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
    print("Starting simpleglfw. Press any key to toggle cut. Press ESC to quit.")
    rw = RenderWindow()
    rw.run()


if __name__ == "__main__":
    main()
