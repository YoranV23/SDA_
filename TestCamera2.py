import cv2
import numpy as np

def detect_shapes(frame):
    # Resize the frame to a smaller resolution
    frame = cv2.resize(frame, (640, 480))  # Adjust the size as needed

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detection to find edges in the image
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Filter out small contours based on area
        if cv2.contourArea(contour) < 100:  # Adjust the area threshold as needed
            continue

        # Approximate the contour with a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Get the number of vertices (sides) of the shape
        num_vertices = len(approx)
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # Use Hough Circle Transform to detect circles
        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
            param1=50, param2=30, minRadius=5, maxRadius=30)
        if circles is not None:
        # Convert the circle parameters to integers
            circles = np.uint16(np.around(circles))
            shape = "Circle"
            for circle in circles[0, 5:]:
                a, b, r = circle[0], circle[1], circle[2]

            # Draw the circumference of the circle
                cv2.circle(frame, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (center)
                cv2.circle(frame, (a, b), 2, (0, 0, 255), 3)

        # Get the shape's name based on the number of vertices
        shape = "Unknown"
        if num_vertices == 3:
            shape = "Triangle"
        elif num_vertices == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            shape = "Square" #if aspect_ratio >= 0.95 and aspect_ratio <= 1.05 else "Rectangle"
        elif num_vertices >= 5:
            shape = "Circle"
        # Draw the detected shape on the frame
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
        cv2.putText(frame, shape, (approx[0][0][0], approx[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

# Initialize the camera capture
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect shapes in the frame
    result_frame = detect_shapes(frame)

    # Display the frame with detected shapes
    cv2.imshow('Shape Detection', result_frame)

    # Press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
