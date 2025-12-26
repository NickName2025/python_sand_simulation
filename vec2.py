class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if type(other) == int:
            return vec2(self.x + other, self.y + other)
        elif type(other) == vec2:
            return vec2(self.x + other.x, self.y + other.y)

    def __floordiv__(self, other):
        if type(other) == int:
            return vec2(self.x // other, self.y // other)
        
    def __mod__(self, other):
        if type(other) == int:
            return vec2(self.x % other, self.y % other)

    def list(self):
        return (self.x, self.y)