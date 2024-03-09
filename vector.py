import math


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return self

    def __str__(self):
        return str((self.x, self.y))

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, other):
        return Vector2D(self.x * other, self.y * other)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def RotateInRads(self, angle):
        newAngle = self.GetAngleInRads() + angle
        magnitude = self.Magnitude()

        self.x = magnitude * math.cos(newAngle)
        self.y = magnitude * math.sin(newAngle)

    def RotateAroundInRads(self, coordinateSystem, angle):
        localVector = self - coordinateSystem
        localVector.RotateInRads(angle)
        newVector = coordinateSystem + localVector
        self.x = newVector.x
        self.y = newVector.y

    def GetAngleInRads(self):
        result = math.asin(self.Sin())
        if (self.Cos() < 0):
            result = math.pi - result
        return result

    def GetRelativeAngleInRads(self, coordinateSystem):
        localVector = self - coordinateSystem

        return localVector.GetAngleInRads()

    def SetAngleInRads(self, angle):
        magnitude = self.Magnitude()

        self.x = magnitude * math.cos(angle)
        self.y = magnitude * math.sin(angle)

    def SetRelativeAngleInRads(self, coordinateSystem, angle):
        localVector = self - coordinateSystem
        localVector.SetAngleInRads(angle)

        newVector = coordinateSystem + localVector

        self.x = newVector.x
        self.y = newVector.y

    def Magnitude(self):
        return math.hypot(self.x, self.y)

    def Sin(self):
        if self.Magnitude() == 0:
            return 0

        return self.y / self.Magnitude()

    def Cos(self):
        if self.Magnitude() == 0:
            return 0

        return self.x / self.Magnitude()
