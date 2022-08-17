import cv2, os
import telepot
from time import sleep
from PIL import Image 
import RPi.GPIO as GPIO
import time
import logging

#dataset 100

RELAY = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY, GPIO.OUT) #set up GPIO output channel
GPIO.output(RELAY,GPIO.LOW)

        
bot = telepot.Bot ("YOUR TELEGRAM TOKEN")

    
chat_id = "YOUR CHAT ID"


def main_app(name):
        
        face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(f"./data/classifiers/{name}_classifier.xml")
        cap = cv2.VideoCapture(0)
        
        def make_360p():
            cap.set(3,640)
            cap.set(4,480) 
        
        make_360p()
        
  
        pred = 0
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:


                roi_gray = gray[y:y+h,x:x+w]

                id,confidence = recognizer.predict(roi_gray)
                confidence = 100 - int(confidence)
                print(confidence)
                pred = 0
                if confidence > 60:
                            pred += +1
                            text = name.capitalize()
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            
                            width = x + w
                            height = y + h
                            color = (0, 255, 0)
                            stroke = 2
                            
                            frame = cv2.rectangle(frame, (x, y), (width, height), color, stroke)
                            frame = cv2.putText(frame, text, (x, y), font, 2, (255, 0, 0), stroke, cv2.LINE_AA)
                        
                            GPIO.output(RELAY,GPIO.HIGH)
                            print("Door unlock! Please enter within 5 seconds!")
                            sleep(5)
                            GPIO.output(RELAY,GPIO.LOW)
                            print("Door locked! Do not enter!")
                            
                            logging.basicConfig(filename='knownlogs.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
                            logging.info(f'{name} logged in')
                            
                                                          

                else:   
                            pred += -1
                            text = "Unknown Face"
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            
                            width = x + w
                            height = y + h
                            color = (0, 0, 255)
                            stroke = 2
                            
                            frame = cv2.rectangle(frame, (x, y), (width, height), color, stroke)
                            frame = cv2.putText(frame, text, (x, y), font, 2, color, stroke, cv2.LINE_AA)
                            
                            GPIO.output(RELAY,GPIO.LOW) #lock
                            print('Unknown!! Door locked! Do not enter!')
                            cv2.imwrite('capture.jpg',frame)
                            bot.sendPhoto(chat_id,open('capture.jpg','rb'))
                            print("Image sent!")
                            
                            logging.basicConfig(filename='unknownlogs.log', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
                            logging.info('Intruder try to enter your place!!')
               
        
            cv2.imshow("Facial Recognition Started! Press q to stop!", frame)
            
            
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break


        cap.release()
        cv2.destroyAllWindows()
        