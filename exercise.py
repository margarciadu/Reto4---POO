import math 
from math import degrees, acos

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.length = self.compute_length()
        self.slope = self.compute_slope()
        self.points = []
    
    def compute_length(self):
        return ((self.end.x - self.start.x)**2 + (self.end.y - self.start.y)**2)**0.5
    
    def compute_slope(self):
        dx = self.end.x - self.start.x
        if dx == 0:
            return float('inf') 
        return (self.end.y - self.start.y) / dx
    
    def compute_horizontal_cross(self):
        return self.start.y * self.end.y < 0
    
    def compute_vertical_cross(self):
        return self.start.x * self.end.x < 0
    
    def discretize_line(self, n: int):
        self.points = [
            Point(
                self.start.x + i * (self.end.x - self.start.x) / (n - 1),
                self.start.y + i * (self.end.y - self.start.y) / (n - 1)
            ) for i in range(n)
        ]
    
class Shape:
    def __init__(self, is_regular: bool, edge: list["Line"], vertice: list["Point"], inner_angles: list[float]):
        self.is_regular = is_regular
        self.edge = edge
        self.vertices = vertice
        self.inner_angels = inner_angles

    def compute_area(self) -> float:
        pass
    
    def compute_perimeter(self) -> float:
        perimeter = 0
        for line in self.edge:
            perimeter += line.compute_length()
        return perimeter
            
    
    def compute_inner_angels(self) -> float:
        total_angles = 0
        for angle in self.inner_angels:
            total_angles += angle
        return total_angles
    
class Rectangle(Shape):
    def __init__(self, vertices: list["Point"], edges: list["Line"]):
        angles = [90, 90, 90, 90]
        super().__init__(is_regular=False, edge=edges, vertice=vertices, inner_angles=angles)
        self.width = edges[0].compute_length()
        self.height = edges[1].compute_length()
        
        def compute_area(self) -> float:
            return self.width * self.height
        
        def compute_perimeter(self) -> float:
            return 2 * (self.width + self.height)
        
        def compute_inner_angels(self) -> float:
            return sum(self.inner_angels)
        
        def diagonal_length(self) -> float:
            return (self.width**2 + self.height**2)**0.5
        
class Square(Rectangle):
    def __init__(self, vertices: list["Point"], edges: list["Line"]):
        super().__init__(vertices, edges)
        self.side = edges[0].compute_length()
        
    def compute_area(self) -> float:
        return self.side ** 2
    
    def compute_perimeter(self) -> float:
        return 4 * self.side
    
    def compute_angles(self) -> float:
        return 360
    
    
class Triangle(Shape):
    def __init__(self, is_regular: bool, vertices: list["Point"], edges: list["Line"], inner_angles: list[float]):
        super().__init__(is_regular, edges, vertices, inner_angles)
        self.side1 = edges[0].compute_length()
        self.side2 = edges[1].compute_length()      
        self.side3 = edges[2].compute_length()
        self.angle1 = inner_angles[0]
        self.angle2 = inner_angles[1]
        self.angle3 = inner_angles[2]
        
    def compute_area(self) -> float:
        s = (self.side1 + self.side2 + self.side3) / 2
        return (s * (s - self.side1) * (s - self.side2) * (s - self.side3)) ** 0.5
    
    def compute_perimeter(self) -> float:
        return self.side1 + self.side2 + self.side3
    
    def compute_inner_angles(self) -> float:
        return self.angle1 + self.angle2 + self.angle3
    
    def is_acute(self) -> bool:
        return self.angle1 < 90 and self.angle2 < 90 and self.angle3 < 90
    
    def is_obtuse(self) -> bool:
        return self.angle1 > 90 or self.angle2 > 90 or self.angle3 > 90
    
    def is_right(self) -> bool:
        return self.angle1 == 90 or self.angle2 == 90 or self.angle3 == 90
    
    def triangle_type(self) -> str:
        if self.is_acute():
            return "Acute Triangle"
        elif self.is_obtuse():
            return "Obtuse Triangle"
        elif self.is_right():
            return "Right Triangle"
        else:
            return "Unknown Triangle Type"
        
class IsoscelesTriangle(Triangle):
    def __init__(self, vertices: list["Point"], edges: list["Line"], inner_angles: list[float]):
        super().__init__(is_regular=False, vertices=vertices, edges=edges, inner_angles=inner_angles)
        
    
    def equal_sides(self) -> bool:
        return self.side1 == self.side2 or self.side2 == self.side3 or self.side1 == self.side3
    
    def compute_area(self):
        if self.side1 == self.side2:
            equal_side = self.side1
            base = self.side3
        elif self.side2 == self.side3:
            equal_side = self.side2
            base = self.side1
        else:
            equal_side = self.side1
            base = self.side2
            
        return (base / 4) * (4 * equal_side**2 - base**2)**0.5
    
class EquilateralTriangle(Triangle):
    def __init__(self, vertices: list["Point"], edges: list["Line"]):
        inner_angles = [60, 60, 60]
        super().__init__(is_regular=True, vertices=vertices, edges=edges, inner_angles=inner_angles)
        self.side = edges[0].compute_length()
        
    def height(self) -> float:
        self.height = (self.side * (3**0.5)) / 2
        return self.height
    
    def compute_area(self) -> float:
        return (self.height() * self.side) / 2
    
class ScaleneTriangle(Triangle):
    def __init__(self, vertices: list["Point"], edges: list["Line"], inner_angles: list[float]):
        super().__init__(is_regular=False, vertices=vertices, edges=edges, inner_angles=inner_angles)
        
    def compute_area(self) -> float:
        s = (self.side1 + self.side2 + self.side3) / 2
        return (s * (s - self.side1) * (s - self.side2) * (s - self.side3)) ** 0.5
    
class TriRectangle(Triangle):
    def __init__(self, vertices: list["Point"], edges: list["Line"], inner_angles: list[float]):
        super().__init__(is_regular=False, vertices=vertices, edges=edges, inner_angles=inner_angles)
        
    def compute_area(self) -> float:
        if self.angle1 == 90:
            return (self.side2 * self.side3) / 2
        elif self.angle2 == 90:
            return (self.side1 * self.side3) / 2
        else:
            return (self.side1 * self.side2) / 2
    
            
    
        
#Test cases

if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    line = Line(p1, p2)
    print(f"Length of line: {line.compute_length()}")
    print(f"Slope of line: {line.compute_slope()}")
    
    rect_vertices = [Point(0, 0), Point(0, 4), Point(3, 4), Point(3, 0)]
    rect_edges = [Line(rect_vertices[0], rect_vertices[1]), 
                  Line(rect_vertices[1], rect_vertices[2]),
                  Line(rect_vertices[2], rect_vertices[3]),
                  Line(rect_vertices[3], rect_vertices[0])]
    
    rectangle = Rectangle(rect_vertices, rect_edges)
    print(f"Rectangle area: {rectangle.compute_area()}")
    print(f"Rectangle perimeter: {rectangle.compute_perimeter()}")
    
    square_vertices = [Point(0, 0), Point(0, 3), Point(3, 3), Point(3, 0)]
    square_edges = [Line(square_vertices[0], square_vertices[1]), 
                    Line(square_vertices[1], square_vertices[2]),
                    Line(square_vertices[2], square_vertices[3]),
                    Line(square_vertices[3], square_vertices[0])]
    
    square = Square(square_vertices, square_edges)
    print(f"Square area: {square.compute_area()}")
    print(f"Square perimeter: {square.compute_perimeter()}")
    
    triangle_vertices = [Point(0, 0), Point(4, 0), Point(2, 3)]
    triangle_edges = [Line(triangle_vertices[0], triangle_vertices[1]), 
                      Line(triangle_vertices[1], triangle_vertices[2]),
                      Line(triangle_vertices[2], triangle_vertices[0])]
    
    triangle_angles = [60, 60, 60]
    
    equilateral_triangle = EquilateralTriangle(triangle_vertices, triangle_edges)
    print(f"Equilateral Triangle area: {equilateral_triangle.compute_area()}")
    
    isosceles_triangle = IsoscelesTriangle(triangle_vertices, triangle_edges, triangle_angles)
    print(f"Isosceles Triangle area: {isosceles_triangle.compute_area()}")
    
    scalene_triangle = ScaleneTriangle(triangle_vertices, triangle_edges, triangle_angles)
    print(f"Scalene Triangle area: {scalene_triangle.compute_area()}")
        
    
        
        
    

   
         
                
        