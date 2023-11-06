import cv2 as cv
import os
from gradio_client import Client
import speech_recognition as sr
# currently 
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


# # Open a connection to the camera (usually camera index 0)
cap = cv.VideoCapture(0)

while True:
#     # Capture frame-by-frame
    ret, frame = cap.read()

#     # Display the frame
    cv.imshow('Camera Feed', frame)

#     # Break the loop if the 'q' key is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Initialize recognizer class (for recognizing the speech)

r = sr.Recognizer()

# Reading Microphone as source
# listening the speech and store in audio_text variable

with sr.Microphone() as source:
    print("Talk")
    audio_text = r.listen(source,5 ,5)
    print("Time over, thanks")
# recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    
    try:
        # using google speech recognition
        print("Text: "+r.recognize_google(audio_text))
    except:
         print("Sorry, I did not get that")
# Release the camera and close the OpenCV window
 cap.release()
cv.destroyAllWindows()
