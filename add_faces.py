import cv2
import pickle
import numpy as np
import os

if not os.path.exists('data/'):
    os.makedirs('data/')


video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces_data = []

i=0
name = input("Enter your Aadhar Number:")

framesTotal = 51
captureAfterFrame = 2

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        

    cv2.imshow('frame', frame)
    k=cv2.waitKey(1)
    if k==ord('q') or len(faces_data) >= framesTotal:
        break