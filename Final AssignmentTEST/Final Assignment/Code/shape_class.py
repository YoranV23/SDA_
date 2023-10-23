# Base class for all shapes

import pygame
import abc
from abc import ABC, abstractmethod
import random

# Set up the colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Shape(ABC):
    # Setting attributes common to all derived classes
    # Assigned default values to avoid TypeError; self.rect must be overridine 
    # when width and height values are not passed
    def __init__(self, window, shape_type, width=1, height=1, x=0, y=0):
        self.window = window
        self.width = width
        self.height = height
        self.color = random.choice([RED, GREEN, BLUE])
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.shapeType = shape_type

    # Defining blueprints and concrete methods for inheritance     
    @abstractmethod
    def clickedInside(self, mousePoint):
        raise NotImplementedError

    def getType(self):
        return self.shapeType
    
    @abstractmethod
    def getArea(self):
        raise NotImplementedError

    @abstractmethod
    def draw(self):
        raise NotImplementedError
