import cv2.cv2 as cv
import numpy as np
import time
import PoseEstimationModule as pm

cap = cv.VideoCapture('AiTrainer/curls3.mp4')
# For camera
# cap = cv.VideoCapture(0)

detector = pm.PoseEstimator()
count = 0
dir = 0
pTime = 0
bar = 0
while True:
    success, img = cap.read()
    # img = cv.imread('AiTrainer/test2.jpg')

    img = cv.resize(img, (480, 720))
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    # Magic starts after this if statement
    if len(lmList)!= 0:
        # Left Arm
        angle = detector.findAngle(img, 11, 13, 15)
        # Right Arm
        # angle = detector.findAngle(img, 12, 14, 16)
        per = np.interp(angle, (210, 300), (0,100))
        bar = np.interp(angle, (210, 300), (650,100))
        print(angle, per)

    #     Check for the dumbbell curls
        color = (0, 100, 0)
        if per == 100:
            color= (0,255,0)
            if dir == 0: # Going up
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir==1:
                count+= 0.5
                dir = 0

        # print(count)
        # Printing the bar
        cv.rectangle(img, (400, 100), (450, 650), color, 2)
        cv.rectangle(img, (400, int(bar)), (450, 650), color, cv.FILLED)
        print(per)
        cv.putText(img, f'{int(per)}%', (390, 700), cv.FONT_HERSHEY_PLAIN, 2, color, 2)

        # Printing counts of the workout
        cv.rectangle(img, (20,20),(130,170),(0,0,0), cv.FILLED)
        cv.putText(img, f'{int(count)}', (30,150), cv.FONT_HERSHEY_PLAIN, 10,(0,255,0), 5)
    

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, f'FPS:{int(fps)}', (50, 700), cv.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv.imshow("Image", img)
    cv.waitKey(5)