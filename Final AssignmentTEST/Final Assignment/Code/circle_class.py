from shape_class import *
import math

class Circle(Shape):
    def __init__(self, window, shape_type, radius, x, y):
        # Inheriting above attributes from base class
        super().__init__(window=window, shape_type=shape_type, x=x, y=y)
        
        self.radius = radius
        self.circle_center = (self.x + self.radius, self.y + self.radius)
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.color = (0,255,0) # green cicle
        
    # Implementing abstract methods 
    def clickedInside(self, mousePoint):
        # mousePoint is a tuple containing the (x, y) position of the mouse cursor
        # first the difference between the x,y coordinates of the cursor and the
        # center of the circle object needs to be calculated
        x_diff = mousePoint[0] - (self.x + self.radius)
        y_diff = mousePoint[1] - (self.y + self.radius)

        # next the pythagorean theorem need be used to calculate the distance
        # between the cursor and the center of the circle
        dist = math.sqrt(x_diff**2 + y_diff**2)

        # finally, return T/F based on the distance from the center of the cicle
        # and the radius of the circle
        if dist < self.radius:
            return True
        else:
            return False
    
    def getArea(self):
        area = round((self.radius**2 * 3.1415),2)
        return area

    def draw(self):
        pygame.draw.circle(self.window, self.color, self.circle_center, self.radius)