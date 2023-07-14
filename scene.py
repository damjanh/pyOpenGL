from cube import Cube
from player import Player
import numpy as np
import pyrr
from OpenGL.GL import *


class Scene:
    def __init__(self):
        self.objects = [
            Cube(
                position=[6, 0, 0],
                eulers=[0, 0, 0]
            ),
            Cube(
                position=[12, 5, 1],
                eulers=[0, 0, 0]
            )
        ]

        self.player = Player(pos=[0, 0, 2])

    def move_player(self, d_pos):
        d_pos = np.array(d_pos, dtype=np.float32)
        self.player.pos += d_pos

    def spin_player(self, d_theta, d_phi):
        self.player.theta += d_theta
        if self.player.theta > 360:
            self.player.theta -= 360
        elif self.player.theta < 0:
            self.player.theta += 360

        self.player.phi = min(
            89, max(-89, self.player.phi + d_phi)
        )

        self.player.update_vectors()

    def update(self, rate):
        for obj in self.objects:
            obj.update(rate)

    def render(self, model_matrix_location, view_matrix_location):
        view_transform = pyrr.matrix44.create_look_at(
            eye=self.player.pos,
            target=self.player.pos + self.player.forwards,
            up=self.player.up,
            dtype=np.float32
        )
        glUniformMatrix4fv(view_matrix_location, 1, GL_FALSE, view_transform)
        for obj in self.objects:
            obj.render(model_matrix_location)

    def destroy(self):
        for obj in self.objects:
            obj.destroy()
