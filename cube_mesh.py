from OpenGL.GL import *
import numpy as np


class CubeMesh:
    def __init__(self):
        # x, y, z, s, t
        vertices = (
            -0.5, -0.5, -0.5, 0, 0,
            0.5, -0.5, -0.5, 1, 0,
            0.5, 0.5, -0.5, 1, 1,

            0.5, 0.5, -0.5, 1, 1,
            -0.5, 0.5, -0.5, 0, 1,
            -0.5, -0.5, -0.5, 0, 0,

            -0.5, -0.5, 0.5, 0, 0,
            0.5, -0.5, 0.5, 1, 0,
            0.5, 0.5, 0.5, 1, 1,

            0.5, 0.5, 0.5, 1, 1,
            -0.5, 0.5, 0.5, 0, 1,
            -0.5, -0.5, 0.5, 0, 0,

            -0.5, 0.5, 0.5, 1, 0,
            -0.5, 0.5, -0.5, 1, 1,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5, -0.5, -0.5, 0, 1,
            -0.5, -0.5, 0.5, 0, 0,
            -0.5, 0.5, 0.5, 1, 0,

            0.5, 0.5, 0.5, 1, 0,
            0.5, 0.5, -0.5, 1, 1,
            0.5, -0.5, -0.5, 0, 1,

            0.5, -0.5, -0.5, 0, 1,
            0.5, -0.5, 0.5, 0, 0,
            0.5, 0.5, 0.5, 1, 0,

            -0.5, -0.5, -0.5, 0, 1,
            0.5, -0.5, -0.5, 1, 1,
            0.5, -0.5, 0.5, 1, 0,

            0.5, -0.5, 0.5, 1, 0,
            -0.5, -0.5, 0.5, 0, 0,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5, 0.5, -0.5, 0, 1,
            0.5, 0.5, -0.5, 1, 1,
            0.5, 0.5, 0.5, 1, 0,

            0.5, 0.5, 0.5, 1, 0,
            -0.5, 0.5, 0.5, 0, 0,
            -0.5, 0.5, -0.5, 0, 1
        )

        self.vertices = np.array(vertices, dtype=np.float32)

        self.vertex_count = len(vertices) // 5

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

    def update(self):
        pass

    def render(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
