from math import degrees, acos, sin, radians, atan2, sqrt


class Point:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
    
    def compute_distance(self, other_point):
        """Calculate distance to another point"""
        return sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)


class Line:
    def __init__(self, start_point: Point, end_point: Point):
        self.start_point = start_point
        self.end_point = end_point
        self.length = self._calculate_length()
        self.slope_radians = atan2((end_point.y - start_point.y), (end_point.x - start_point.x))
        self.slope_degrees = degrees(self.slope_radians)

    def _calculate_length(self) -> float:
        dx = self.end_point.x - self.start_point.x
        dy = self.end_point.y - self.start_point.y
        return sqrt(dx**2 + dy**2)
    
    def compute_length(self) -> float:
        return self.length


class Shape:
    def __init__(self):
        self._regular_flag = False
        self._vertex_list = []
        self._edge_collection = []
        self._angle_values = []

    def set_is_regular(self, regular_status: bool):
        self._regular_flag = regular_status

    def get_is_regular(self) -> bool:
        return self._regular_flag

    def set_vertices(self, vertex_points: list):
        self._vertex_list = vertex_points
        self._build_edges()

    def get_vertices(self) -> list:
        return [(vertex.x, vertex.y) for vertex in self._vertex_list]
    
    def _build_edges(self):
        """Internal method to construct edges from vertices"""
        pass

    def compute_edges(self):
        """Calculate edges of the shape"""
        pass

    def get_edges(self):
        """Retrieve edge information"""
        pass

    def compute_inner_angles(self):
        """Calculate internal angles"""
        pass        

    def compute_perimeter(self):
        """Calculate shape perimeter"""
        pass

    def compute_area(self):
        """Calculate shape area"""
        pass


class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        self._top_side = None
        self._bottom_side = None
        self._left_side = None
        self._right_side = None
    
    def compute_edges(self):   
        # Vertex structure: [top_left, top_right, bottom_right, bottom_left]
        vertices = self._vertex_list
        self._top_side = Line(vertices[0], vertices[1])
        self._bottom_side = Line(vertices[3], vertices[2])
        self._left_side = Line(vertices[0], vertices[3])
        self._right_side = Line(vertices[1], vertices[2])

    def get_edges(self) -> list:
        self.compute_edges()
        edge_info = [
            {
                "edge_name": "upper_border",
                "start_coord": (self._top_side.start_point.x, self._top_side.start_point.y),
                "end_coord": (self._top_side.end_point.x, self._top_side.end_point.y),
                "edge_length": self._top_side.compute_length()
            },
            {
                "edge_name": "lower_border",
                "start_coord": (self._bottom_side.start_point.x, self._bottom_side.start_point.y),
                "end_coord": (self._bottom_side.end_point.x, self._bottom_side.end_point.y),
                "edge_length": self._bottom_side.compute_length()
            },
            {
                "edge_name": "left_border",
                "start_coord": (self._left_side.start_point.x, self._left_side.start_point.y),
                "end_coord": (self._left_side.end_point.x, self._left_side.end_point.y),
                "edge_length": self._left_side.compute_length()
            },
            {
                "edge_name": "right_border",
                "start_coord": (self._right_side.start_point.x, self._right_side.start_point.y),
                "end_coord": (self._right_side.end_point.x, self._right_side.end_point.y),
                "edge_length": self._right_side.compute_length()
            }
        ]
        return edge_info

    def compute_area(self) -> float:
        self.compute_edges()
        width = self._top_side.compute_length()
        height = self._right_side.compute_length()
        return width * height
       
    def compute_perimeter(self) -> float:
        self.compute_edges()
        horizontal_length = self._top_side.compute_length()
        vertical_length = self._right_side.compute_length()
        return 2 * (horizontal_length + vertical_length)
    
    def compute_inner_angles(self):
        return [90.0, 90.0, 90.0, 90.0]


class Square(Rectangle):
    def __init__(self):
        super().__init__()
        self._regular_flag = True


class Triangle(Shape):
    def __init__(self):
        super().__init__()
        self._side_a = None
        self._side_b = None
        self._side_c = None
        self._length_a = 0
        self._length_b = 0
        self._length_c = 0

    def compute_edges(self): 
        vertices = self._vertex_list
        self._side_a = Line(vertices[0], vertices[1])
        self._side_b = Line(vertices[1], vertices[2])
        self._side_c = Line(vertices[2], vertices[0])
        
        self._length_a = self._side_a.compute_length()
        self._length_b = self._side_b.compute_length()
        self._length_c = self._side_c.compute_length()

    def get_edges(self):
        self.compute_edges()
        triangle_edges = [
            {
                "edge_name": "side_alpha",
                "start_coord": (self._side_a.start_point.x, self._side_a.start_point.y),
                "end_coord": (self._side_a.end_point.x, self._side_a.end_point.y),
                "edge_length": self._length_a
            },
            {
                "edge_name": "side_beta",  
                "start_coord": (self._side_b.start_point.x, self._side_b.start_point.y),
                "end_coord": (self._side_b.end_point.x, self._side_b.end_point.y),
                "edge_length": self._length_b
            },
            {
                "edge_name": "side_gamma",
                "start_coord": (self._side_c.start_point.x, self._side_c.start_point.y),
                "end_coord": (self._side_c.end_point.x, self._side_c.end_point.y),
                "edge_length": self._length_c
            }
        ]
        return triangle_edges

    def compute_inner_angles(self):
        self.compute_edges()
        
        # Angle opposite to side_a
        cos_alpha = (self._length_c**2 + self._length_b**2 - self._length_a**2) / (2 * self._length_c * self._length_b)
        self.alpha_angle = degrees(acos(cos_alpha))
        
        # Angle opposite to side_b
        cos_beta = (self._length_c**2 + self._length_a**2 - self._length_b**2) / (2 * self._length_c * self._length_a)
        self.beta_angle = degrees(acos(cos_beta))
        
        # Angle opposite to side_c
        cos_gamma = (self._length_b**2 + self._length_a**2 - self._length_c**2) / (2 * self._length_b * self._length_a)
        self.gamma_angle = degrees(acos(cos_gamma))
       
        return [self.alpha_angle, self.beta_angle, self.gamma_angle]
        
    def compute_area(self) -> float:
        self.compute_edges()
        self.compute_inner_angles()
        # Using formula: Area = (1/2) * a * b * sin(C)
        area_value = 0.5 * self._length_a * self._length_b * sin(radians(self.gamma_angle))
        return area_value
       
    def compute_perimeter(self) -> float:
        self.compute_edges()
        total_perimeter = self._length_a + self._length_b + self._length_c
        return total_perimeter


class Equilateral(Triangle):
    def __init__(self):
        super().__init__()
        self._regular_flag = True


class Isosceles(Triangle):
    def __init__(self):
        super().__init__()


class Scalene(Triangle):
    def __init__(self):
        super().__init__()


class TriRectangle(Triangle):
    def __init__(self):
        super().__init__()


# Testing and demonstration
if __name__ == "__main__":
    
    # Rectangle demonstration
    print("=== Rectangle Testing ===")
    my_rectangle = Rectangle()
    my_rectangle.set_vertices([Point(1, 3), Point(5, 3), Point(5, 1), Point(1, 1)])
    print("Vertices:", my_rectangle.get_vertices())
    print("Edges:", my_rectangle.get_edges())
    print("Area:", my_rectangle.compute_area())
    print("Perimeter:", my_rectangle.compute_perimeter())
    print("Inner angles:", my_rectangle.compute_inner_angles())
    print()

    # Square demonstration
    print("=== Square Testing ===")
    my_square = Square()
    my_square.set_vertices([Point(2, 2), Point(5, 2), Point(5, 5), Point(2, 5)])
    print("Vertices:", my_square.get_vertices())
    print("Edges:", my_square.get_edges())
    print("Area:", my_square.compute_area())
    print("Perimeter:", my_square.compute_perimeter())
    print("Inner angles:", my_square.compute_inner_angles())
    print("Is regular:", my_square.get_is_regular())
    print()

    # Triangle demonstration
    print("=== Triangle Testing ===")
    my_triangle = Triangle()
    my_triangle.set_vertices([Point(1, 4), Point(5, 1), Point(1, 1)])
    print("Vertices:", my_triangle.get_vertices())
    print("Edges:", my_triangle.get_edges())
    print("Area:", round(my_triangle.compute_area(), 3))
    print("Perimeter:", round(my_triangle.compute_perimeter(), 3))
    print("Inner angles:", [round(angle, 2) for angle in my_triangle.compute_inner_angles()])
    print()

    # Equilateral Triangle demonstration
    print("=== Equilateral Triangle Testing ===")
    my_equilateral = Equilateral()
    my_equilateral.set_vertices([Point(1, 1), Point(3, 1), Point(2, 2.732)])
    print("Vertices:", my_equilateral.get_vertices())
    print("Edges:", my_equilateral.get_edges())
    print("Area:", round(my_equilateral.compute_area(), 3))
    print("Perimeter:", round(my_equilateral.compute_perimeter(), 3))
    print("Inner angles:", [round(angle, 1) for angle in my_equilateral.compute_inner_angles()])
    print("Is regular:", my_equilateral.get_is_regular())
    print()

    # Scalene Triangle demonstration
    print("=== Scalene Triangle Testing ===")
    my_scalene = Scalene()
    my_scalene.set_vertices([Point(0, 0), Point(6, 0), Point(2, 4)])
    print("Vertices:", my_scalene.get_vertices())
    print("Edges:", my_scalene.get_edges())
    print("Area:", round(my_scalene.compute_area(), 3))
    print("Perimeter:", round(my_scalene.compute_perimeter(), 3))
    print("Inner angles:", [round(angle, 1) for angle in my_scalene.compute_inner_angles()])
    print("Side lengths verification:")
    edges = my_scalene.get_edges()
    for edge in edges:
        print(f"  {edge['edge_name']}: {round(edge['edge_length'], 2)}")
    print("All sides different (Scalene confirmed):", 
          len(set(round(edge['edge_length'], 2) for edge in edges)) == 3)