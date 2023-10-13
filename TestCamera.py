import cv2
import numpy as np

def detect_shapes(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detection to find edges in the image
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Approximate the contour with a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Get the number of vertices (sides) of the shape
        num_vertices = len(approx)
        
        # Get the shape's name based on the number of vertices
        shape = "Unknown"
        if num_vertices == 3:
            shape = "Triangle"
        elif num_vertices == 4:
            x, y, w, h = cv2.boundingRect(approx)
            #aspect_ratio = float(w) / h
            shape = "Square" #if aspect_ratio >= 0.95 and aspect_ratio <= 1.05 else "Rectangle"
        elif num_vertices >= 10:
            shape = "Circle"
        
        # Draw the detected shape on the frame
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
        cv2.putText(frame, shape, (approx[0][0][0], approx[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

def detect_circles(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Use Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
        param1=50, param2=30, minRadius=5, maxRadius=50
    )

    if circles is not None:
        # Convert the circle parameters to integers
        circles = np.uint16(np.around(circles))

        for circle in circles[0, :]:
            a, b, r = circle[0], circle[1], circle[2]

            # Draw the circumference of the circle
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (center)
            cv2.circle(frame, (a, b), 2, (0, 0, 255), 3)

    return frame

# Initialize the camera capture
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Filter red, blue, green, and yellow colors
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color ranges for red, blue, green, and yellow
    red_lower = np.array([204, 204, 255])
    red_upper = np.array([0, 0, 255])
    
    blue_lower = np.array([100, 100, 100])
    blue_upper = np.array([140, 255, 255])
    
    green_lower = np.array([40, 100, 100])
    green_upper = np.array([80, 255, 255])
    
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    # Create masks for each color
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Apply masks to the frame
    red_result = cv2.bitwise_and(frame, frame, mask=red_mask)
    blue_result = cv2.bitwise_and(frame, frame, mask=blue_mask)
    green_result = cv2.bitwise_and(frame, frame, mask=green_mask)
    yellow_result = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    # Detect shapes and circles in the filtered frames
    red_result = detect_shapes(red_result)
    blue_result = detect_shapes(blue_result)
    green_result = detect_shapes(green_result)
    yellow_result = detect_shapes(yellow_result)

    # Combine the filtered frames
    result_frame = cv2.addWeighted(frame, 1, red_result, 1, 0)
    result_frame = cv2.addWeighted(result_frame, 1, blue_result, 1, 0)
    result_frame = cv2.addWeighted(result_frame, 1, green_result, 1, 0)
    result_frame = cv2.addWeighted(result_frame, 1, yellow_result, 1, 0)

    # Display the frame with detected shapes and colors
    cv2.imshow('Shape and Color Detection', result_frame)

    # Press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
