from shape_class import *

class Triangle(Shape):
    # setting derived class attributes using constructor method __init__
    def __init__(self, window, shape_type, width, height, x, y):
        # inheriting definition of above attributes from parent 'S_Rectangle'
        super().__init__(window, shape_type, width, height, x, y)

        self.triangleSlope = -1 * (self.height / self.width)
        self.color = (255,0,0) # red triangle
        
    # Implementing abstract methods 
    def clickedInside(self, mousePoint):
        inRect = self.rect.collidepoint(mousePoint)
        if not inRect:
            return False

        # Do some math to see if the point is inside the triangle
        xOffset = mousePoint[0] - self.x
        yOffset = mousePoint[1] - self.y
        if xOffset == 0:
            return True

        # Calculate the slope (rise over run)
        pointSlopeFromYIntercept = (yOffset - self.height) / xOffset
        if pointSlopeFromYIntercept < self.triangleSlope:
            return True
        else:
            return False
    
    def getArea(self):
        theArea = .5 * self.width * self.height
        return theArea

    def draw(self):
         pygame.draw.polygon(self.window, self.color,
            ((self.x, self.y + self.height),
             (self.x, self.y),
             (self.x + self.width, self.y)))