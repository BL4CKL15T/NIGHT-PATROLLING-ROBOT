import RPi.GPIO as gpio
import numpy as np
import cv2
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
import speech_recognition as sr
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(38,gpio.IN)
gpio.setup(40,gpio.OUT)
recognizer = sr.Recognizer()
keyword=['help','save']
global count
count=0
def SendMail(ImgFileName):
    print('sending mail')
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'alert'
    msg['From'] = 'krishnendugs10@gmail.com'
    msg['To'] = 'alhadquassim@gmail.com'

    text = MIMEText("Result")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('krishnendugs10@gmail.com', 'mtceunevvwpbnoeb')
    s.sendmail('krishnendugs10@gmail.com', 'alhadquassim@gmail.com', msg.as_string())
    s.quit()
    time.sleep(5)

def cam():
    global count
    global flag
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    while True:
        flag=0
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
        cv2.imshow('video',img)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
        elif count>200: # press 'ESC' to quit
            break
        count+=1
    cap.release()
    cv2.destroyAllWindows()
    return img
    
while 1:
    try:
        with sr.Microphone() as source:
            print("Start Talking")
            audio_text = recognizer.listen(source)
            print("Time over, thank you")
            text=recognizer.recognize_google(audio_text)
            print("Text: "+text)
            for k in keyword:
                if k in text :
                    image=cam()
            
            cv2.imwrite('image.jpg',image)
            
    except:
        print('error')
        continue
    SendMail('image.jpg')

