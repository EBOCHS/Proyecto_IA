import imp
from itertools import count
from tkinter import Frame
import cv2;
import numpy as np;
#import imutils
import os

Datos = 'p';
if not os.path.exists(Datos):
    print('Carpeta creada', Datos);
    os.makedirs(Datos);

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW);
x1,y1 = 190,80
x2,y2 =450,398
count =0

while True:
    ret , Frame= cap.read()
    if ret == False: break
    cv2.rectangle(Frame,(x1,x2),(x2,y2),(255,0,0),2)
    cv2.imshow('Frame',Frame )
    k = cv2.waitKey(1)
    if k==2:
        break;

cap.release();
cv2.destroyAllWindows();
