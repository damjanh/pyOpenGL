import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from cube import Cube
import sys


WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 800


class App:
    def __init__(self):
        pg.init()
        pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        # Initialise OpenGl
        glClearColor(0.1, 0.2, 0.2, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = self.create_shader('shaders/vertex.txt', 'shaders/fragment.txt')
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, 'imageTexture'), 0)
        self.cube = Cube(
            position=[0, 0, -3],
            eulers=[0, 0, 0]
        )

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=WINDOW_WIDTH/WINDOW_HEIGHT,
            near=0.1, far=10, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, 'projection'),
            1, GL_FALSE, projection_transform
        )

        self.model_matrix_location = glGetUniformLocation(self.shader, 'model')

        self.run()

    def create_shader(self, vertex_filepath, fragment_filepath):
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        return shader

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

            self.update()
            self.render()

            pg.display.flip()
            self.clock.tick(60)

    def update(self):
        self.cube.update(self.model_matrix_location)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.shader)

        self.cube.render()

    def quit(self):
        self.cube.destroy()
        glDeleteProgram(self.shader)
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    app = App()
