import math

from material import Material
import numpy as np
from OpenGL.GL import *
import pyrr


class Billboard:
    def __init__(self, pos, width, height):
        self.pos = pos
        half_w = width / 2
        half_h = height / 2
        vertices = (
            0, -half_w, half_h, 0, 0, -1, 0, 0,
            0, -half_w, -half_h, 0, 1, -1, 0, 0,
            0, half_w, -half_h, 1, 1, -1, 0, 0,

            0, -half_w, half_h, 0, 0, -1, 0, 0,
            0, half_w, -half_h, 1, 1, -1, 0, 0,
            0, half_w, half_h, 1, 0, -1, 0, 0
        )

        self.texture = Material('gfx/greenlight.png')

        self.vertex_count = len(vertices) // 8
        vertices = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # Texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # Normal
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def render(self, player_pos, model_matrix_location):
        direction_from_player = self.pos - player_pos
        angle = np.arctan2(-direction_from_player[1], direction_from_player[0])
        dist2d = math.sqrt(direction_from_player[0] ** 2 + direction_from_player[1] ** 2)
        angle2 = np.arctan2(direction_from_player[2], dist2d)

        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_y_rotation(theta=angle2, dtype=np.float32)
        )
        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_z_rotation(theta=angle, dtype=np.float32)
        )
        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_translation(vec=self.pos, dtype=np.float32)
        )

        glUniformMatrix4fv(model_matrix_location, 1, GL_FALSE, model_transform)

        self.texture.enable()
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
        self.texture.destroy()
