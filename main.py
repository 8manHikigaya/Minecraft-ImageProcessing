import cv2
import mss
import numpy as np

# Define screen capture region
monitor = {"top": 400, "left": 100, "width": 900, "height": 400}

while True:
    with mss.mss() as sct:
        # Capture screen and resize
        img = np.array(sct.grab(monitor))
        img = cv2.resize(img, (800, 400))

        # Define blue color range in HSV
        BLUE_MIN = np.array([85, 50, 70], np.uint8)
        BLUE_MAX = np.array([90, 255, 255], np.uint8)

        # Convert to HSV and create a mask
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        frame_threshed = cv2.inRange(hsv_img, BLUE_MIN, BLUE_MAX)

        # Find non-zero points in the mask
        points = cv2.findNonZero(frame_threshed)

        # If points are detected, calculate their average position
        if points is not None:
            avg = np.mean(points, axis=0)[0]
            avgx, avgy = int(avg[1]), int(avg[0])  # Flip x and y because of OpenCV's coordinates
            print(f"Center: ({avgx}, {avgy})")

            # Add a red dot at the detected center
            cv2.circle(img, (avgy, avgx), 5, (0, 0, 255), -1)

        # Display the output
        cv2.imshow('output', img)

    # Exit on 'ESC' key
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break
