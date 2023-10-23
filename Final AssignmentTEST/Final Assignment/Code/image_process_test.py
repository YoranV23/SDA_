import cv2
import numpy as np

shapes_list =[]

video = cv2.VideoCapture(1, cv2.CAP_DSHOW)
img = video.read()[1]

# First try to detect the red triangle
# filtering image for red
# first convert img to LAB colorspace
imgLAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

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
thresh_img = cv2.threshold(resultLAB_gray,80,200, cv2.THRESH_BINARY_INV)[1]; 
cv2.imshow('result lab gray', resultLAB_gray) 
cv2.imshow('thresholded image', thresh_img)
cv2.waitKey()
cv2.destroyAllWindows

detector = cv2.SimpleBlobDetector_create()
 
keypoints = detector.detect(thresh_img)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(thresh_img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()

if not keypoints:
    print ('red triangle not detected')
else:
    print ('red triangle detected')
    shapes_list.append('red triangle')

print (f'Shapes list: {shapes_list}')


# second try to detect green circle
# setting green color (value found through image investigation)
#BGR = [85,190,146]
BGR = [61,67,250]
thresh = 50
#thresh = 22
lab = cv2.cvtColor( np.uint8([[BGR]] ), cv2.COLOR_BGR2LAB)[0][0]
 
minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

maskLAB = cv2.inRange(imgLAB, minLAB, maxLAB)
resultLAB = cv2.bitwise_and(imgLAB, imgLAB, mask = maskLAB)

# now try to see if any shapes match a circular profile
resultLAB_gray = cv2.cvtColor((cv2.cvtColor(resultLAB, cv2.COLOR_LAB2BGR)), cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(resultLAB_gray,80,230, cv2.THRESH_BINARY_INV)[1]; 
cv2.imshow('result lab gray', resultLAB_gray) 
cv2.imshow('thresholded image', thresh_img)
cv2.waitKey()
cv2.destroyAllWindows

detector = cv2.SimpleBlobDetector_create()
 
# Detect blobs.
keypoints = detector.detect(thresh_img)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(thresh_img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()

if not keypoints:
    print ('red circle not detected')
else:
    print ('red circle detected')
    shapes_list.append('red circle')

print (f'Shapes list: {shapes_list}')

# third try to detect yellow square
# setting yellow color (value found through image investigation)
BGR = [61,67,250]
thresh = 50
lab = cv2.cvtColor( np.uint8([[BGR]] ), cv2.COLOR_BGR2LAB)[0][0]
 
minLAB = np.array([lab[0] - thresh, lab[1] - thresh, lab[2] - thresh])
maxLAB = np.array([lab[0] + thresh, lab[1] + thresh, lab[2] + thresh])

maskLAB = cv2.inRange(imgLAB, minLAB, maxLAB)
resultLAB = cv2.bitwise_and(imgLAB, imgLAB, mask = maskLAB)

# now try to see if any shapes match a square profile
resultLAB_gray = cv2.cvtColor((cv2.cvtColor(resultLAB, cv2.COLOR_LAB2BGR)), cv2.COLOR_BGR2GRAY)
thresh_img = cv2.threshold(resultLAB_gray,80,200, cv2.THRESH_BINARY_INV)[1] 
cv2.imshow('result lab gray', resultLAB_gray) 
cv2.imshow('thresholded image', thresh_img)
cv2.waitKey()
cv2.destroyAllWindows

detector = cv2.SimpleBlobDetector_create()
 
# Detect blobs.
keypoints = detector.detect(thresh_img)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(thresh_img, keypoints, np.array([]), (255,0,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()

if not keypoints:
    print ('red square not detected')
else:
    print ('red square detected')
    shapes_list.append('red square')

print (f'Shapes list: {shapes_list}')