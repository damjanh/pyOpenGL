from OpenGL.GL import *
import numpy as np


class Mesh:
    def __init__(self, filename):
        # x, y, z, s, t, nx, ny, nz
        vertices = self.load_mesh(filename)
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

    def load_mesh(self, filename) -> list[float]:
        v = []
        vt = []
        vn = []
        vertices = []

        with open(filename, 'r') as file:
            line = file.readline()
            while line:
                words = line.split(' ')
                if words[0] == 'v':
                    v.append(self.read_vertex_date(words))
                elif words[0] == 'vt':
                    vt.append(self.read_texcoord_data(words))
                elif words[0] == 'vn':
                    vn.append(self.read_normal_data(words))
                elif words[0] == 'f':
                    self.read_face_data(words, v, vt, vn, vertices)
                line = file.readline()

        return vertices

    def read_vertex_date(self, words: list[str]) -> list[float]:
        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]

    def read_texcoord_data(self, words: list[str]) -> list[float]:
        return [
            float(words[1]),
            float(words[2])
        ]

    def read_normal_data(self, words: list[str]) -> list[float]:
        return [
            float(words[1]),
            float(words[2]),
            float(words[3])
        ]

    def read_face_data(
            self,
            words: list[str],
            v: list[list[float]],
            vt: list[list[float]],
            vn: list[list[float]],
            vertices: list[float]) -> None:
        triangle_count = len(words) - 3

        for i in range(triangle_count):
            self.make_corner(words[1], v, vt, vn, vertices)
            self.make_corner(words[2 + i], v, vt, vn, vertices)
            self.make_corner(words[3 + i], v, vt, vn, vertices)

    def make_corner(self, corner_description: str, v, vt, vn, vertices):
        v_vt_vn = corner_description.split('/')
        for element in v[int(v_vt_vn[0]) - 1]:
            vertices.append(element)
        for element in vt[int(v_vt_vn[1]) - 1]:
            vertices.append(element)
        for element in vn[int(v_vt_vn[2]) - 1]:
            vertices.append(element)

    def render(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))
