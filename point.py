import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def show(self):
        print(f"Point({self.x}, {self.y}, {self.z})")

    def move(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dist(self, other_point):
        dx = other_point.x - self.x
        dy = other_point.y - self.y
        dz = other_point.z - self.z
        return math.sqrt(dx**2 + dy**2 + dz**2)
