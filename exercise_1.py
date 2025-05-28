class Shape:
    def __init__(self):
        pass

    def compute_area(self):
        raise NotImplementedError("Subclases deben implementar compute_area()")

    def compute_perimeter(self):
        raise NotImplementedError("Subclases deben implementar compute_perimeter()")

class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width

    def compute_area(self):
        return self.length * self.width

    def compute_perimeter(self):
        return 2 * (self.length + self.width)

class Square(Shape):
    def __init__(self, side):
        super().__init__()
        self.side = side

    def compute_area(self):
        return self.side * self.side

    def compute_perimeter(self):
        return 4 * self.side

# Ejemplo de uso
figura1 = Rectangle(4, 5)
figura2 = Square(3)

print("Área del rectángulo:", figura1.compute_area())
print("Perímetro del rectángulo:", figura1.compute_perimeter())

print("Área del cuadrado:", figura2.compute_area())
print("Perímetro del cuadrado:", figura2.compute_perimeter())
