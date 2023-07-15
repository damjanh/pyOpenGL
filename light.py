from billboard import Billboard


class Light:
    def __init__(self, position, color, strength):
        self.position = position
        self.color = color
        self.strength = strength
        self.billboard = Billboard(position, 0.5, 0.5)
