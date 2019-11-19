#!/usr/bin/python3

#raspberry ID 2

#Horus contador multitracker
#tracker MedianFlow
#flip invertido

import crud_utils
import cv2
from datetime import datetime
import requests
import json

face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_frontalface_alt2.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_upperbody.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/cascadeH5.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/cascadG.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/models/upperbody_recognition_model.xml")
#face_cascade = cv2.CascadeClassifier("/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_profileface.xml")

videoPath = "/home/pi/teste.mp4"
#cap = cv2.VideoCapture(videoPath)
cap = cv2.VideoCapture(0)

bboxes = []
bbox=()
boxes = []

numFaces = 0
frame_altura =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
tempoIni = datetime.now()
face_anterior = 0

deleteBox=0

detectado = False

frame_largura = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_altura =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

def hansen_track(bbox, bboxes,frame,tracker):
    
    multiTracker = cv2.MultiTracker_create()
    
    for bbox in bboxes:
      
      multiTracker.add(tracker, frame, bbox)
    
    rect,boxes = multiTracker.update(frame)
    
    return boxes

soma=0
 
while True:
      
      ret, frame = cap.read()
      
      frame = cv2.flip(frame, 0)
      
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
      if(detectado == True):
          
          timeOut1=datetime.now()-tempoIni
          
          boxes = hansen_track(bbox, bboxes,frame,tracker)
         
          for i, newbox in enumerate(boxes):
            
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            
            
            #cv2.putText(frame, "{}".format(str(i)) , (int(newbox[0]), (int(newbox[1])-4)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 0, 0), 2)
          movement= abs(newbox[1] - bbox[1])
          
          if((timeOut.seconds >3 and movement < 60) or timeOut.seconds >7 ):
            deleteBox=1  
            
          if(int(newbox[1]) > 320):
            
            flag=1
      else:
        
        flag=0
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
    
        a=len(faces)
      
        for (x,y,w,h) in faces:
          
          coord=(x+10,y+80,w-20,h+90)    
          
          cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 1, 1)
      
      
      
      if(face_anterior < a):
          
          tempoIni = datetime.now()
          bbox=tuple(coord)
          bboxes.append(bbox)
          
          if(bbox[1]<300):
            
            face_anterior +=1
      else:
          
          timeOut=datetime.now()-tempoIni
          
          if(timeOut.seconds ==1 and face_anterior>0 ):
            
            tracker = cv2.TrackerMedianFlow_create()  
            
            detectado=True
          
      ###############################################################################################################################
      
      if(flag == 1):
          
          tracker.clear()
          del bboxes[:]
          
          soma=soma+face_anterior
          crud_utils.inserir_dado(2, 2, 'd3f2d810-1193-4cef-8a7a-971890a4157d', soma)
          cv2.putText(frame, "dados salvos!...", (5, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
          
          face_anterior=0
          detectado=False
      
      ###############################################################################################################################
      #timeout
      ###############################################################################################################################
      
      if(deleteBox == 1):    
          tracker.clear()
          del bboxes[:]
          face_anterior=0
          detectado=False
          deleteBox=0
      
      
      
      cv2.putText(frame, "Pessoas ja contadas: {}".format(str(soma)), (5, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
              
                    
      cv2.line(frame, (0,350), (frame_largura ,350), (255, 0, 55), 1)       
           
      cv2.putText(frame, "Pessoas detectadas: {}".format(str(face_anterior)), (5, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
      
      cv2.putText(frame, "ESC sai", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
      
      cv2.imshow("frame", frame)
      
    
      if cv2.waitKey(1) == 27 & 0xFF :
        
          break
    
cap.release()  
cv2.destroyAllWindows()
