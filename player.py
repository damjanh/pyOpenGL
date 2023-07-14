import numpy as np


class Player:
    def __init__(self, pos):
        self.pos = np.array(pos, dtype=np.float32)
        self.theta = 0
        self.phi = 0
        self.forwards = None
        self.right = None
        self.up = None
        self.update_vectors()

    def update_vectors(self):
        self.forwards = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi))
            ]
        )
        global_up = np.array([0, 0, 1], dtype=np.float32)

        self.right = np.cross(self.forwards, global_up)
        self.up = np.cross(self.right, self.forwards)



