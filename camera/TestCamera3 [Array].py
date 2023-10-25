import cv2
import numpy as np
import time

class ShapeDetector:
    def __init__(self):
        pass

    def detect_shape(self, contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        num_sides = len(approx)

        shape = None
        if num_sides == 3:
            shape = "Triangle"
        elif num_sides == 4:
            shape = "Square"
        else:
            shape = "Circle"

        return shape

    def detect_color(self, image, cX, cY):
        (b, g, r) = image[cY, cX]
        if r > 150 and g < 100 and b < 100:
            return "Red"
        else:
            return "Not Red"

# Access the webcam
cap = cv2.VideoCapture(1)

# Create an instance of the shape detector
shape_detector = ShapeDetector()

# Flag to indicate image capture
capture_flag = False

# Time when the red shape was detected
start_time = None

# List to store detected shapes
detected_shapes = []

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert BGR to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges in the image
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through each contour
    for contour in contours:
        # Ignore small contours
        if cv2.contourArea(contour) < 100:
            continue

        # Detect the color
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        color = shape_detector.detect_color(frame, cX, cY)

        # Only detect and draw red shapes
        if color == "Red":
            # Detect the shape
            detected_shape = shape_detector.detect_shape(contour)

            # Draw the contour and the name of the shape on the frame
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            cv2.putText(frame, f"{detected_shape}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            if start_time is None:
                start_time = time.time()

            # Set the capture flag to True when a red shape is detected and 5 seconds have passed
            if time.time() - start_time >= 5:
                detected_shapes.append(detected_shape)  # Add the detected shape to the list
                capture_flag = True

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Capture and save the image if the capture flag is True
    if capture_flag:
        cv2.imwrite('captured_image.png', frame)
        print("Image captured successfully!")
        print("Detected Shapes:", detected_shapes)
        break  # Stop the program after capturing the image

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
cap.release()
cv2.destroyAllWindows()
