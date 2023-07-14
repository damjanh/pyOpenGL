import numpy as np
from cube_mesh import CubeMesh
from material import Material


class Cube:
    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

        self.mesh = CubeMesh()
        self.texture = Material('gfx/wood.jpeg')

    def update(self):
        self.eulers[2] += 0.2
        if self.eulers[2] > 360:
            self.eulers[2] -= 350

    def render(self):
        self.texture.use()
        self.mesh.render()

    def destroy(self):
        self.texture.destroy()
        self.mesh.destroy()


