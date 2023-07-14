import numpy as np
from mesh import Mesh
from material import Material
import pyrr
from OpenGL.GL import *


class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

        self.mesh = Mesh('models/cube.obj')
        self.texture = Material('gfx/wood.jpeg')

    def update(self, rate):
        self.eulers[1] += 0.2 * rate
        if self.eulers[1] > 360:
            self.eulers[1] -= 360

    def render(self, model_matrix_location):
        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_eulers(
                eulers=np.radians(self.eulers),
                dtype=np.float32
            )
        )
        model_transform = pyrr.matrix44.multiply(
            m1=model_transform,
            m2=pyrr.matrix44.create_from_translation(
                vec=self.position,
                dtype=np.float32
            )
        )
        glUniformMatrix4fv(model_matrix_location, 1, GL_FALSE, model_transform)
        self.texture.enable()
        self.mesh.render()

    def destroy(self):
        self.texture.destroy()
        self.mesh.destroy()
