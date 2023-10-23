from shape_class import *

class Square(Shape):
    # setting derived class attributes using constructor method __init__
    def __init__(self, window, shape_type, width, x, y):
        # inheriting definition of above attributes from parent 'S_Rectangle'
        super().__init__(window, shape_type, width, width, x, y)

        self.color = (255,0,0) # blue square
        
    # Implementing abstract methods 
    def clickedInside(self, mousePoint):
        clicked = self.rect.collidepoint(mousePoint)
        return clicked
    
    def getArea(self):
        area =  self.width**2
        return area

    def draw(self):
         pygame.draw.rect(self.window, self.color, self.rect)