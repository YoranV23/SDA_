import pygame
import sys
from pygame.locals import *
from circle_class import * 
from triangle_class import *
from square_class import * 
import pygwidgets

# Set up the constants
        
WHITE = (255, 255, 255)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
shapes_list = ['red triangle','green circle']
shape_selected = None

# Set up the window
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
clock = pygame.time.Clock()

draw_list = []    
for shape in shapes_list:
    if shape == 'red triangle':
        TShape = Triangle(window, shape_type='triangle', width=150, height=150, x=280, y=80)
        draw_list.append(TShape)
    elif shape == 'green circle':
        CShape = Circle(window, shape_type='circle', radius=50, x=380, y=280)
        draw_list.append(CShape)
    elif shape == 'yellow square':
        SShape = Square(window,  shape_type='square', width=80, x=180, y=280)
        draw_list.append(SShape)

oStatusLine = pygwidgets.DisplayText(window, (4,4),'Please choose an object to place on the conveyor belt')

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            # Reverse order to check last drawn shape first
            for oShape in draw_list:
                if oShape.clickedInside(event.pos):
                    shape_selected = oShape.getType()
                    newText = 'Now placing ' + shape_selected + ' on the conveyor'
                    oStatusLine.setValue(newText)
                    print (f'Shape selected for relocation: {shape_selected}')
                    pygame.time.wait(1500)
                    pygame.quit()
                    sys.exit()

    # Tell each shape to draw itself
    window.fill(WHITE)
    for oShape in draw_list:
        oShape.draw()
    oStatusLine.draw()

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)

    