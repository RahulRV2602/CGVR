import glfw
from OpenGL.GL import *
import numpy as np


# Vertex Shader
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""


# Fragment Shader
fragment_shader_source = """
#version 330 core

out vec4 FragColor;

void main()
{
    FragColor = vec4(0.2, 0.6, 1.0, 1.0);
}
"""


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    # Check compilation status
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError("Shader compilation failed:\n" + error)

    return shader


def create_shader_program():
    vertex_shader = compile_shader(
        vertex_shader_source,
        GL_VERTEX_SHADER
    )

    fragment_shader = compile_shader(
        fragment_shader_source,
        GL_FRAGMENT_SHADER
    )

    program = glCreateProgram()

    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)

    glLinkProgram(program)

    # Check linking status
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        raise RuntimeError("Shader linking failed:\n" + error)

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program


def main():

    # Initialize GLFW
    if not glfw.init():
        raise Exception("GLFW initialization failed")

    # OpenGL version
    glfw.window_hint(
        glfw.CONTEXT_VERSION_MAJOR, 3
    )
    glfw.window_hint(
        glfw.CONTEXT_VERSION_MINOR, 3
    )
    glfw.window_hint(
        glfw.OPENGL_PROFILE,
        glfw.OPENGL_CORE_PROFILE
    )

    # Create window
    window = glfw.create_window(
        800,
        600,
        "OpenGL Shader Program",
        None,
        None
    )

    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)

    # Triangle vertices
    vertices = np.array([
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.0,  0.5, 0.0
    ], dtype=np.float32)

    # Create VAO and VBO
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    glBufferData(
        GL_ARRAY_BUFFER,
        vertices.nbytes,
        vertices,
        GL_STATIC_DRAW
    )

    # Vertex attribute
    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        3 * vertices.itemsize,
        ctypes.c_void_p(0)
    )

    glEnableVertexAttribArray(0)

    # Create shader program
    shader_program = create_shader_program()

    # Rendering loop
    while not glfw.window_should_close(window):

        # Clear screen
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # Use shader program
        glUseProgram(shader_program)

        # Draw triangle
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swap buffers
        glfw.swap_buffers(window)

        # Process events
        glfw.poll_events()

    # Cleanup
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)

    glfw.terminate()


if __name__ == "__main__":
    main()