import cv2
import numpy as np

class ShapeDetector:
    def __init__(self):
        self.detected_shapes = set()  # Use a set to store unique detected shapes

    def detect_shape(self, contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.03 * peri, True)  # Increase sensitivity by reducing the tolerance
        num_sides = len(approx)

        if num_sides == 3:
            shape = "Triangle"
        elif num_sides == 4:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:  # Adjust the aspect ratio range for squares
                shape = "Square"
            else:
                shape = "Unknown"
        else:
            circularity = 4 * np.pi * cv2.contourArea(contour) / (peri ** 2)
            if 0.8 <= circularity <= 1.2:
                shape = "Circle"
            else:
                shape = "Unknown"

        if shape != "Unknown":
            self.detected_shapes.add(shape)  # Add the detected shape to the set

        return shape

    def get_detected_shapes(self):
        return list(self.detected_shapes)  # Convert the set to a list

    def detect_color(self, image, cX, cY):
        (b, g, r) = image[cY, cX]
        if r > 150 and g < 100 and b < 100:
            return "Red"
        else:
            return "Not Red"

def capture_and_detect_shapes():
    shape_detector = ShapeDetector()

    # Open the camera
    cap = cv2.VideoCapture(1)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 120:
                continue
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            color = shape_detector.detect_color(frame, cX, cY)

            if color == "Red":
                detected_shape = shape_detector.detect_shape(contour)
                if detected_shape != "Unknown":
                    cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                    cv2.putText(frame, f"{detected_shape}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    print("Detected Shape:", detected_shape)

        # Display the frame with detected shapes
        cv2.imshow('Camera View', frame)

        # Check for user input to exit
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return shape_detector.get_detected_shapes()

if __name__ == "__main__":
    detected_shapes = capture_and_detect_shapes()
    print("Detected Shapes in the Camera View:", detected_shapes)
