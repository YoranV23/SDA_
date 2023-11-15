import cv2
import numpy as np
import time
import DoBotArm as Dbt  # Import the DoBotArm module

#List of Coordinates Dobot has to follow (x, y, z, suction_on)
coordinate_queue = [(-1, -143, 14, True), (140, -170, 90, False), (175, 13, -28, True), (0, -140, 60, False)]

#Detection of shapes 
class ShapeDetector:
    def __init__(self):
        pass
    #Detect shapes using contours
    def detect_shape(self, contour):
        peri = cv2.arcLength(contour, True)
        # Increase camera sensivity.
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        num_sides = len(approx)
        #Amount of contours to check what shape is detected.
        shape = None
        if num_sides == 3:
            shape = "Triangle"
        elif num_sides == 4:
            shape = "Square"
        else:
            shape = "Circle"
        return shape
    #Detect if the color red is detected within limits 
    def detect_color(self, image, cX, cY):
        (b, g, r) = image[cY, cX]   
        if r > 200 and g < 100 and b < 100:
            return "Red"
        else:
            return "Not Red"

def detect_shapes_and_capture():
    # Use camera index 1 for Dobot Camera
    cap = cv2.VideoCapture(1)  
    shape_detector = ShapeDetector()
    capture_flag = False
    start_time = None
    #Save detected shapes in an Array to print.
    detected_shapes = []

    while True:
        ret, frame = cap.read()
        #Change frame to grayscale for better object detection. 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Finding the center of the detected shape 
        for contour in contours:
            if cv2.contourArea(contour) < 100:
                continue
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            color = shape_detector.detect_color(frame, cX, cY)
            #If color Red is detected draw a frame around the shape and put the text in the center
            if color == "Red":
                detected_shape = shape_detector.detect_shape(contour)
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                cv2.putText(frame, f"{detected_shape}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
               
                #Timer to keep the camera activated for 5 seconds to prevent any changes.
                if start_time is None:
                    start_time = time.time()

                if time.time() - start_time >= 5:
                    detected_shapes.append(detected_shape)
                    capture_flag = True

        cv2.imshow('frame', frame)
        #Write the captured image and print if this is successfully completed, also print the detected shapes, and close camera
        if capture_flag:
            cv2.imwrite('captured_image.png', frame)
            print("Image captured successfully!")
            print("Detected Shapes:", detected_shapes)
            break
        #Turn off camera if 'q' is pressed.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return detected_shapes

def main():
    # Create an instance of the DoBotArm class
    dobot = Dbt.DoBotArm(port='COM9', homeX=0, homeY=-140, homeZ=60, home=True, homingWait=True)

    # Home Dobot
    dobot.rehome(0, -140, 60)
    print("Rehoming")
    # Cycle to change last position in the coordinate_queue.
    for cycle in range(3):
        print(f"Cycle {cycle + 1}")

        for i, (x, y, z, suction) in enumerate(coordinate_queue):
            if cycle == 1 and i == 2:
                # Change the coordinates for the second cycle
                x, y, z = 203, -33, -28
            elif cycle == 2 and i == 2:
                # Change the coordinates for the third cycle
                x, y, z = 143, -33, -28
            elif cycle == 2 and i == 3:
                # Return to home position
                x, y, z = 0, -140, 60

            # Move the Dobot to the specified coordinates
            dobot.moveArmXYZ(x, y, z)

            # Turn suction on and off
            if suction:
                dobot.toggleSuction()

            # If the Dobot has reached its final coordinate each step, move up 20 in z-axis before going home (better object placement)
            if (x, y, z) in [(175, 13, -28), (203, -33, -28), (143, -33, -28)]:
                dobot.moveArmRelXYZ(0, 0, 20)

        # Start conveyor belt 1 second after the cycle begins (for the first and second cycles)
        if cycle < 2:
            time.sleep(1)
            dobot.SetConveyor(enabled=True, speed=15000)

        # Stop conveyor belt after 1 second
        if cycle < 2:
            time.sleep(1)
            dobot.SetConveyor(enabled=False)

        # Return to the home position
        dobot.moveArmXYZ(0, -140, 60)
        time.sleep(2)

    # Detect shapes using the camera
    detected_shapes = detect_shapes_and_capture()
    print("Shapes Detected by the Camera:", detected_shapes)

if __name__ == "__main__":
    main()
                                                                                                                                                                                                   
