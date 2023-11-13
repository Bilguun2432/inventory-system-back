from typing import Protocol

class Shape(Protocol):
    def area(self) -> float:
        ...

    def perimeter(self) -> float:
        ...

class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius * self.radius

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius
    


shape: Shape


shape = Circle(radius = 10)

print(shape.area())