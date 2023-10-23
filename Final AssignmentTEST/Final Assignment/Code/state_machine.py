from transitions import Machine
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
from circle_class import * 
from triangle_class import *
from square_class import * 
import pygwidgets
import DoBotArm as dbt
import time
import DobotDllType as dType


class SystemOperations(object):

    # Defining states of the state machine as per design
    states = ['start operations', 'check loading area', 'initialize UI', 'object relocation', 'move conveyor', 'end operations']

    def __init__(self):
        # Defining data shared between transitions as class attributes
        self.shapes_list = []
        self.shape_selected = None
        self.pos1 = (139.7, -208.8, -38.5) # triangular prism
        self.pos2 = (200.6, -236.2, -38) # circular prism
        self.pos3 = (236.4, -195.8, -38.5) # rectangular prism
        self.pos4 = (205.2, -49.8, 10) # drop-off
        
        self.position_dictionary = {
                    'triangle': self.pos1,
                    'square' :  self.pos3,
                    'circle' :  self.pos2,
                    'drop-off': self.pos4
                }    
        # instantiating an object that represents the physical Dobot
        self.homeX, self.homeY, self.homeZ = 250, 0, 50
        self.ctrlDobot = dbt.DoBotArm("COM11", self.homeX, self.homeY, self.homeZ, home= False) 
        
        # Initialize the state machine
        self.machine = Machine(model=self, states=SystemOperations.states, initial='start operations')

        # Adding transitions as per design
        self.machine.add_transition(trigger='start_system', source='start operations', dest='check loading area', after= 'create_shapes_list')

        self.machine.add_transition('shapes_list_created', 'check loading area', 'end operations', conditions=['check_shapes_list'], after= ['disconnect_dobot'])
        self.machine.add_transition('shapes_list_created', 'check loading area', 'initialize UI', after= 'create_UI')
        
        self.machine.add_transition('user_selected_shape', 'initialize UI', 'object relocation', after= 'relocate_selected_object')

        
        self.machine.add_transition('object_relocated', 'object relocation', 'move conveyor', after= 'move_conveyor_belt')

        self.machine.add_transition('conveyor_belt_moved', 'move conveyor', 'check loading area', after= 'create_shapes_list')
    
    # this is where the loading area is imaged; then the image is processed to 
    # identify the three desired shapes: red triangle; green circle; yellow square;
    # identified shapes are put in self.shapes_list
    def create_shapes_list(self):
        self.shapes_list = []

        loading_area_video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        frame = loading_area_video.read()[1]
        loading_area_video.release()
       
        # First try to detect the red triangle
        # filtering image for red
        #first convert img to LAB colorspace
        imgLAB = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        # setting red color (value found through image investigation)
        BGR = [61,67,250]
        thresh = 50

        #convert 1D color information array to 3D, then convert it to LAB and take the first element
        lab = cv2.cvtColor( np.uint8([[BGR]] ), cv2.COLOR_BGR2LAB)[0][0]
        
        minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
        maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

        maskLAB = cv2.inRange(imgLAB, minLAB, maxLAB)
        resultLAB = cv2.bitwise_and(imgLAB, imgLAB, mask = maskLAB)
        
        # now checking for objects in filtered image
        resultLAB_gray = cv2.cvtColor((cv2.cvtColor(resultLAB, cv2.COLOR_LAB2BGR)), cv2.COLOR_BGR2GRAY)
        # Inverse binary thresholding of image for better blob detection
        thresh_img = cv2.threshold(resultLAB_gray,80,200, cv2.THRESH_BINARY_INV)[1]; 
       
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(thresh_img)
        if not keypoints:
            print ('red triangle not detected')
        else:
            print ('red triangle detected')
            self.shapes_list.append('red triangle')

        # second, try to detect green circle
        # setting green color (value found through image investigation)
        BGR = [85,190,146]
        thresh = 22
        lab = cv2.cvtColor( np.uint8([[BGR]] ), cv2.COLOR_BGR2LAB)[0][0]
        
        minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
        maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

        maskLAB = cv2.inRange(imgLAB, minLAB, maxLAB)
        resultLAB = cv2.bitwise_and(imgLAB, imgLAB, mask = maskLAB)

        # now checking for objects in filtered image
        resultLAB_gray = cv2.cvtColor((cv2.cvtColor(resultLAB, cv2.COLOR_LAB2BGR)), cv2.COLOR_BGR2GRAY)
        thresh_img = cv2.threshold(resultLAB_gray,80,230, cv2.THRESH_BINARY_INV)[1]; 
       
        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(thresh_img)
        if not keypoints:
            print ('green circle not detected')
        else:
            print ('green circle detected')
            self.shapes_list.append('green circle')

        # third, try to detect yellow square
        # setting yellow color (value found through image investigation)
        BGR = [44,241,249]
        thresh = 50
        lab = cv2.cvtColor( np.uint8([[BGR]] ), cv2.COLOR_BGR2LAB)[0][0]
        
        minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
        maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

        maskLAB = cv2.inRange(imgLAB, minLAB, maxLAB)
        resultLAB = cv2.bitwise_and(imgLAB, imgLAB, mask = maskLAB)

        # now try to see if any shapes match a square profile
        resultLAB_gray = cv2.cvtColor((cv2.cvtColor(resultLAB, cv2.COLOR_LAB2BGR)), cv2.COLOR_BGR2GRAY)
        thresh_img = cv2.threshold(resultLAB_gray,80,200, cv2.THRESH_BINARY_INV)[1]; 

        detector = cv2.SimpleBlobDetector_create()
        keypoints = detector.detect(thresh_img)

        if not keypoints:
            print ('yellow square not detected')
        else:
            print ('yellow square detected')
            self.shapes_list.append('yellow square')

        self.trigger('shapes_list_created')
    
    def create_UI(self):
        # Set up the constants
        WHITE = (255, 255, 255)
        WINDOW_WIDTH = 640
        WINDOW_HEIGHT = 480
        FRAMES_PER_SECOND = 30

        # Set up the window
        pygame.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
        clock = pygame.time.Clock()

        draw_list = []    
        for shape in self.shapes_list:
            if shape == 'red triangle':
                TShape = Triangle(window, shape_type='triangle', width=150, height=150, x=280, y=80)
                draw_list.append(TShape)
            elif shape == 'green circle':
                CShape = Circle(window, shape_type='circle', radius=50, x=380, y=280)
                draw_list.append(CShape)
            elif shape == 'yellow square':
                SShape = Square(window,  shape_type='square', width=80, x=180, y=280)
                draw_list.append(SShape)
        
        #oStatusLine = pygwidgets.DisplayText(window, (4,4),'Please choose an object to place on the conveyor belt', fontSize=28)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    # Reverse order to check last drawn shape first
                    for oShape in draw_list:
                        if oShape.clickedInside(event.pos):
                            self.shape_selected = oShape.getType()
                            newText = 'Now placing ' + self.shape_selected + ' on the conveyor'
                            #oStatusLine.setValue(newText)
                            print (f'Shape selected for relocation: {self.shape_selected}')
                            running = False
                            break

            # Tell each shape to draw itself
            window.fill(WHITE)
            for oShape in draw_list:
                oShape.draw()
            #oStatusLine.draw()

            pygame.display.update()
            clock.tick(FRAMES_PER_SECOND)
        
        pygame.time.wait(1500)
        pygame.quit()
        #del oStatusLine
        self.trigger('user_selected_shape')

            

    @property
    def check_shapes_list(self):
        if not self.shapes_list:
            return True
        else:
            return False

    def relocate_selected_object(self):
        if self.shape_selected == 'triangle':
            x, y, z = self.position_dictionary['triangle']
            self.ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
            self.ctrlDobot.toggleSuction()
            time.sleep(0.3)
            
            
            x, y, z = self.position_dictionary['drop-off']
            self.ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
            self.ctrlDobot.toggleSuction()
            self.ctrlDobot.moveArmRelXYZ(0, 0, 20)
            self.trigger('object_relocated')

        elif self.shape_selected == 'circle':
            x, y, z = self.position_dictionary['circle']
            self.ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)       
            self.ctrlDobot.toggleSuction()
            time.sleep(0.3)

            x, y, z = self.position_dictionary['drop-off']
            self.ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
            self.ctrlDobot.toggleSuction()
            self.ctrlDobot.moveArmRelXYZ(0, 0, 20)
            self.trigger('object_relocated')

        elif self.shape_selected == 'square':
            x, y, z = self.position_dictionary['square']
            self.ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
            self.ctrlDobot.toggleSuction()
            time.sleep(0.3)
        
            x, y, z = self.position_dictionary['drop-off']
            self.ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
            self.ctrlDobot.toggleSuction()
            self.ctrlDobot.moveArmRelXYZ(0, 0, 20)
            self.trigger('object_relocated')


    def move_conveyor_belt(self):
        print ('Moving conveyor belt')
        self.ctrlDobot.SetConveyor(enabled= True, speed= -10000)
        time.sleep(1)
        self.ctrlDobot.SetConveyor(enabled= False)
        self.trigger('conveyor_belt_moved')

    def disconnect_dobot(self):
        print ('Dobot Disconnected')