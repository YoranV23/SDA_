import DoBotArm as dbt
import time
import DobotDllType as dType
import cv2

pos1 = (139.7, -208.8, -38.5) # triangular prism
pos2 = (200.6, -236.2, -34.7) # circular prism
pos3 = (236.4, -195.8, -38.5) # rectangular prism
pos4 = (205.2, -49.8, 10) # drop-off

position_dictionary = {
            'triangle': pos1,
            'square' :  pos3,
            'circle' :  pos2,
            'drop-off': pos4
        }

homeX, homeY, homeZ = 250, 0, 50
ctrlDobot = dbt.DoBotArm("COM11", homeX, homeY, homeZ, home= False)

img = cv2.imread(r'C:\Users\Stijn\Desktop\Fontys University of Applied Sciences\Fontys Mechatronica 2023-2024\SDA3\Final AssignmentTEST\Final Assignment\Media\blanca')
img = cv2.resize(img, dsize= (400,300))
text = 'Perform Required Steps'
text_org = (10,150)
cv2.putText(img, text, text_org, fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0))

#1. Place triangular prism (any color) on the loading area
#2. Move dobot end effector to the approximate center of the prism, making contact
#3. Retrieve and store the dobot coordinates for the prism

x, y, z = position_dictionary['triangle']
ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
ctrlDobot.pickToggle(itemHeight= 10)

cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    ctrlDobot.pickToggle(itemHeight= 10)
    print(' triangular prism positioned')
else:
    ctrlDobot.dobotDisconnect()

x, y, z = position_dictionary['circle']
ctrlDobot.moveArmXYZ(x= x, y= y, z= z+10)
ctrlDobot.pickToggle(itemHeight= 10)

cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    ctrlDobot.pickToggle(itemHeight= 10)
    print(' triangular prism positioned')
else:
    ctrlDobot.dobotDisconnect()

x, y, z = position_dictionary['square']
ctrlDobot.moveArmXYZ(x= x, y= y, z= z+10)
ctrlDobot.pickToggle(itemHeight= 10)

cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    ctrlDobot.pickToggle(itemHeight= 10)
    print(' triangular prism positioned')
else:
    ctrlDobot.dobotDisconnect()


