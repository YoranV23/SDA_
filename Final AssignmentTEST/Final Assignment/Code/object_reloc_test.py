import DoBotArm as dbt
import time
import DobotDllType as dType
import cv2

pos1 = (139.7, -208.8, -38.5) # triangular prism
pos2 = (200.6, -236.2, -38) # circular prism
pos3 = (236.4, -195.8, -38.5) # rectangular prism
pos4 = (205.2, -49.8, 10) # drop-off

position_dictionary = {
            'triangle': pos1,
            'square' :  pos3,
            'circle' :  pos2,
            'drop-off': pos4
        }
shape_selected = 'square'

img = cv2.imread(r'SDA3_PersonalRepo\Final Assignment\Media\blanca.jpg')
img = cv2.resize(img, dsize= (400,300))
text = 'Everything as desired?'
text_org = (10,150)
cv2.putText(img, text, text_org, fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0))

# instantiating an object that represents the physical Dobot
homeX, homeY, homeZ = 250, 0, 50
ctrlDobot = dbt.DoBotArm("COM8", homeX, homeY, homeZ, home= False)

if shape_selected == 'triangle':
    x, y, z = position_dictionary['triangle']
    ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)

    cv2.imshow('Prompt Window', img)
    key = cv2.waitKey()
    cv2.destroyAllWindows()
    if key == ord('d'):
        pass
    else:
        ctrlDobot.dobotDisconnect()
    
    
    ctrlDobot.toggleSuction()
    time.sleep(0.5)
    
    
    x, y, z = position_dictionary['drop-off']
    ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
    ctrlDobot.toggleSuction()
    #time.sleep(0.5)
    ctrlDobot.moveArmRelXYZ(0, 0, 20)
    

    ctrlDobot.SetConveyor(enabled= True, speed= -10000)
    time.sleep(1)
    ctrlDobot.SetConveyor(enabled= False)
    print('triangle relocated')

if shape_selected == 'circle':
    x, y, z = position_dictionary['circle']
    ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)

    cv2.imshow('Prompt Window', img)
    key = cv2.waitKey()
    cv2.destroyAllWindows()
    if key == ord('d'):
        pass
    else:
        ctrlDobot.dobotDisconnect()
    
    
    ctrlDobot.toggleSuction()
    time.sleep(0.5)
    
    
    x, y, z = position_dictionary['drop-off']
    ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
    ctrlDobot.toggleSuction()
    #time.sleep(0.5)
    ctrlDobot.moveArmRelXYZ(0, 0, 20)
    

    ctrlDobot.SetConveyor(enabled= True, speed= -10000)
    time.sleep(1)
    ctrlDobot.SetConveyor(enabled= False)
    print('triangle relocated')
if shape_selected == 'square':
    x, y, z = position_dictionary['square']
    ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)

    cv2.imshow('Prompt Window', img)
    key = cv2.waitKey()
    cv2.destroyAllWindows()
    if key == ord('d'):
        pass
    else:
        ctrlDobot.dobotDisconnect()
    
    
    ctrlDobot.toggleSuction()
    time.sleep(0.5)
    
    
    x, y, z = position_dictionary['drop-off']
    ctrlDobot.moveArmXYZ(x= x, y= y, z= z, jump= True)
    ctrlDobot.toggleSuction()
    #time.sleep(0.5)
    ctrlDobot.moveArmRelXYZ(0, 0, 20)
    

    ctrlDobot.SetConveyor(enabled= True, speed= -10000)
    time.sleep(1)
    ctrlDobot.SetConveyor(enabled= False)
    print('triangle relocated')

