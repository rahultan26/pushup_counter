

import cv2
import mediapipe as md
import argparse
#from google.colab.patches import cv2_imshow

md_drawing=md.solutions.drawing_utils
md_drawing_styles=md.solutions.drawing_styles
md_pose=md.solutions.pose

#!/usr/bin/python
# -*- coding: utf-8 -*-
fourcc=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output.mp4',fourcc,20.0,(640,480))
count=0
position=None
ap = argparse.ArgumentParser()

ap.add_argument("-v", "--video", required=True,
 	help="path to input video file")
args = vars(ap.parse_args())
cap=cv2.VideoCapture(args["video"])
#cap=cv2.VideoCapture('video_input.mp4')

with md_pose.Pose(min_detection_confidence=0.4,min_tracking_confidence=0.4) as pose:
    while cap.isOpened():
        (success, image) = cap.read()
        if not success:
            print('empty camera')
            break
        
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        result = pose.process(image)

        imlist = []

        if result.pose_landmarks:
            md_drawing.draw_landmarks(image, result.pose_landmarks,
                    md_pose.POSE_CONNECTIONS)
            for (id, im) in enumerate(result.pose_landmarks.landmark):
                (h, w, _) = image.shape
                (X, Y) = (int(im.x * w), int(im.y * h))
                imlist.append([id, X, Y])

      # print(imlist)

        if len(imlist) != 0:
            if (imlist[12][2] and imlist[11][2] >= imlist[14][2] 
                and imlist[13][2]):
                position = 'down'
            if (imlist[12][2] and imlist[11][2] <= imlist[14][2] 
                and imlist[13][2] and position == 'down'):
                position = 'up'
                count += 1
                print(count)
        #cv2.flip(image,1) 
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_RGB2BGR)
        out.write(image)
       
        cv2.imshow("MediaPipe pushup",image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()

