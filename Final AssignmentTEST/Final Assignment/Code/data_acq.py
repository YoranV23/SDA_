import cv2
import numpy as np
import DoBotArm as dbt
import datetime

# instantiating an object that represents the physical Dobot
homeX, homeY, homeZ = 250, 0, 50
ctrlDobot = dbt.DoBotArm("COM11", homeX, homeY, homeZ, home= False)

img = cv2.imread(r'C:\Users\Stijn\Desktop\Fontys University of Applied Sciences\Fontys Mechatronica 2023-2024\SDA3\Final AssignmentTEST\Final Assignment\Media\blanca.jpg')
img = cv2.resize(img, dsize= (400,300))
text = 'Perform Required Steps'
text_org = (10,150)
cv2.putText(img, text, text_org, fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0))

#1. Place triangular prism (any color) on the loading area
#2. Move dobot end effector to the approximate center of the prism, making contact
#3. Retrieve and store the dobot coordinates for the prism
cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    tri_prism_coord = ctrlDobot.getPosition()
    print('Position of triangular prism acquired')
else:
    ctrlDobot.dobotDisconnect()


#4. Place rectangular prism (any color) on the loading area (keep other prism(s) in place)
#5. Move dobot end effector to the approximate center of the prism, making contact
#6. Retrieve and store the dobot coordinates for the prism
cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    rect_prism_coord = ctrlDobot.getPosition()
    print('Position of rectangular prism acquired')
else:
    ctrlDobot.dobotDisconnect()
#7. Place circular prism (any color) on the loading area (keep other prism(s) in place)
#8. Move dobot end effector to the approximate center of the prism, making contact
#9. Retrieve and store the dobot coordinates for the prism
cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    circ_prism_coord = ctrlDobot.getPosition()
    print('Position of circular prism acquired')
else:
    ctrlDobot.dobotDisconnect()
#10. Move dobot to the desired drop-off position over the conveyor belt
#11. retrieve and store the dobot coordinates for object drop-off
cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    drop_off_coord = ctrlDobot.getPosition()
    print('Position of object drop-off acquired')
else:
    ctrlDobot.dobotDisconnect()

# Additional step: remove dobot from view of camera
cv2.imshow('Prompt Window', img)
key = cv2.waitKey()
cv2.destroyAllWindows()
if key == ord('d'):
    print('Dobot removed from view')
else:
    ctrlDobot.dobotDisconnect()
#12. Capture an image of the prisms in the set positions using the system's camera
#13. Capture a 15s video of the same using the same camera
video = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# getting properties of the video input object, to inform video output object creation
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)
fps = 60

# instantiating video output object
output = cv2.VideoWriter(r'C:\Users\Stijn\Desktop\Fontys University of Applied Sciences\Fontys Mechatronica 2023-2024\SDA3\Final AssignmentTEST\Final Assignment\Media\OutputVideo.avi',
                         cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, frame_size)


ret, frame = video.read()
cv2.imwrite(r'C:\Users\Stijn\Desktop\Fontys University of Applied Sciences\Fontys Mechatronica 2023-2024\SDA3\Final AssignmentTEST\Final Assignment\Media\loading_area.jpg', frame)

current_time = datetime.datetime.now()
end_time = current_time + datetime.timedelta(seconds= 15)

while datetime.datetime.now() <= end_time:
    ret, frame = video.read()
    cv2.imshow('Live Stream', frame)
    cv2.waitKey(20)
    output.write(frame)
cv2.destroyAllWindows()

print (f'Position coordinates of triangular prism: {tri_prism_coord}')
print (f'Position coordinates of circular prism: {circ_prism_coord}')
print (f'Position coordinates of rectangular prism: {rect_prism_coord}')
print (f'Drop-off coordinates: {drop_off_coord}')
video.release()
output.release()
ctrlDobot.dobotDisconnect()