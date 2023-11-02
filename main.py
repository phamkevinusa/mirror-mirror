import cv2 as cv
import os
from gradio_client import Client

# Get the current working directory where your Python script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the image file name
image_filename = "test.jpg"

# Construct the full path to the image
image_path = os.path.join(current_directory, image_filename)



img = cv.imread(image_path)
cv.resize(img, (400,400),1,1)
cv.imshow("Display window", img)
k = cv.waitKey(0) # Wait for a keystroke in the window


# Open a connection to the camera (usually camera index 0)
cap = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the frame
    cv.imshow('Camera Feed', frame)

    # Break the loop if the 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv.destroyAllWindows()