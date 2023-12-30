import base64
import cv2 as cv
import os
from gradio_client import Client
import speech_recognition as sr
import keyboard
import replicate
from gtts import gTTS
from playsound import playsound
import tkinter as tk
import threading
import PIL
# initialize voice rec
r = sr.Recognizer() 
# initialize video capture
cap = cv.VideoCapture(0)

def print_to_window(text):
    text_to_print = text
    text_widget.delete("1.0","end")

    text_widget.insert(tk.END, text_to_print + "\n")


def display_video():
    while True:
        ret, frame = cap.read()

        # Display the frame
        cv.imshow('Camera Feed', frame)

        # Break the loop if the 'q' key is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def background_task():

    current_directory = os.getcwd()
    os.environ["REPLICATE_API_TOKEN"] = "YOUR_TOKEN"
    def image_to_data_url(filename):
        ext = filename.split('.')[-1]
        prefix = f'data:image/{ext};base64,'
        with open(filename, 'rb') as f:
            img = f.read()
        return prefix + base64.b64encode(img).decode('utf-8')
    while True:
        print_to_window("press 'm' to take photo\npress 'p' to talk\npress 'b' to prompt 'q' to quit")
        if keyboard.read_key() == "m":
            print_to_window("m pressed")
            ret, frame = cap.read()
            cv.imwrite(os.path.join(current_directory , 'waka.jpg'), frame)
        if keyboard.read_key() == "p":
            with sr.Microphone() as source:
                print_to_window("Talk")
                audio_text = r.listen(source,5 ,5)
                print_to_window("Time over, thanks")
                try:
                    # using google speech recognition
                    text = r.recognize_google(audio_text)
                    print_to_window("Text: "+text)
                except:
                    print_to_window("Sorry, I did not get that")

            with open(current_directory+"\waka.jpg", "rb") as imagefile:
                convert = base64.b64encode(imagefile.read())
                # print(convert.decode('utf-8'))
                image = convert.decode('utf-8')
        if keyboard.read_key() == "b":
            print_to_window("b pressed")

            output = replicate.run(
                "daanelson/minigpt-4:b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423",
                input={
                "image": image_to_data_url(current_directory+"\waka.jpg"),
                "top_p": 0.9,
                "prompt": "you are a person named 'mirror mirror' who's job is through conversation to boost the confidence of the subject in the image based on physical and emotional factors and give constructive and truthful advice. This is the subject's response: " + text,
                "num_beams": 5,
                "max_length": 4000,
                "temperature": .9, #lower is less predictable results. default is 1
                "max_new_tokens": 3000,
                "repetition_penalty": 1 # higher is less repetition
            })
            myobj = gTTS(text=output, lang = 'en', slow=False) 
            myobj.save('welcome.mp3') 
            playsound(current_directory+"\welcome.mp3") 
            os.remove(current_directory+"\welcome.mp3")
            print_to_window(output)
        elif keyboard.read_key() == "q":
            break
# Create the main window
window = tk.Tk()
window.title("Mirror Mirror")

# Create a Text widget to display the printed text
text_widget = tk.Text(window, height=10, width=40)
text_widget.pack(padx=10, pady=10)

# Start the background task in a separate thread
background_thread = threading.Thread(target=background_task)
background_thread.daemon = True  # Daemonize the thread so it automatically exits when the main program finishes
background_thread.start()
background_thread2 = threading.Thread(target=display_video)
background_thread2.daemon = True  # Daemonize the thread so it automatically exits when the main program finishes
background_thread2.start()
# Start the Tkinter event loop
window.mainloop()
cap.release()
cv.destroyAllWindows()

