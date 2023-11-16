import base64
import cv2 as cv
import os
from gradio_client import Client
import speech_recognition as sr
import keyboard
import replicate
from gtts import gTTS

# initialize voice rec
r = sr.Recognizer() 
# initialize video capture
cap = cv.VideoCapture(0)

current_directory = os.getcwd()
os.environ["REPLICATE_API_TOKEN"] = "r8_dBJCnIX2PV0C1GNK0PlQEQZisK3q8Vp3KiqyO"
def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')
while True:
    print("press 'm' to take photo\npress 'p' to talk\npress 'b' to prompt 'q' to quit")
    if keyboard.read_key() == "m":
        print("m pressed")
        ret, frame = cap.read()
        cv.imwrite(os.path.join(current_directory , 'waka.jpg'), frame)
    if keyboard.read_key() == "p":
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source,5 ,5)
            print("Time over, thanks")
            try:
                # using google speech recognition
                text = r.recognize_google(audio_text)
                print("Text: "+text)
            except:
                print("Sorry, I did not get that")
            print("Text: "+text)

        with open(current_directory+"\waka.jpg", "rb") as imagefile:
            convert = base64.b64encode(imagefile.read())
            # print(convert.decode('utf-8'))
            image = convert.decode('utf-8')
    if keyboard.read_key() == "b":
        output = replicate.run(
            "daanelson/minigpt-4:b96a2f33cc8e4b0aa23eacfce731b9c41a7d9466d9ed4e167375587b54db9423",
            input={
            "image": image_to_data_url(current_directory+"\waka.jpg"),
            "top_p": 0.9,
            "prompt": "describe this image",
            "num_beams": 5,
            "max_length": 4000,
            "temperature": 1.32, #lower is less predictable results. default is 1
            "max_new_tokens": 3000,
            "repetition_penalty": 1 # higher is less repetition
        })
        myobj = gTTS(text=output, lang = 'en', slow=False) 
        myobj.save("welcome.mp3") 
        os.system("winsound " + current_directory+"\welcome.mp3") 
        print(output)
    elif keyboard.read_key() == "q":
        break