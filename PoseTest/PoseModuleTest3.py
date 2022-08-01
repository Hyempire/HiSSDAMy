import cv2
import mediapipe as mp
import PoseModule as poseModule
import time
from gtts import gTTS
import playsound
import os
import msvcrt

# pose 돌리는데 필요한 모듈들을 변수에 담아줌
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 웹캠을 연결함
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# pose 돌리는 데 필요한 설정
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

center_result = []
left_result = []
right_result = []

end = 2

current_time = 1
time_end = 99999999999999

while cap.isOpened():

    success, image = cap.read()
    if not success:
        print("EMPTY CAMERA FRAME")
        continue

    pose_results, output_image = poseModule.detectPose(image, pose)
    key = cv2.waitKey(1) & 0xFF

    if pose_results.pose_landmarks:
        directionResult, center, left, right = poseModule.poseDirection(output_image, pose_results,
                                                                        center_result, left_result, right_result,
                                                                        threshold=7)
        current_time = time.time()

        if key == ord('a'):
            center_result = []
            left_result = []
            right_result = []
            time_end = current_time + end
        else:
            pass

        if current_time >= time_end:
            center_result = center
            left_result = left
            right_result = right
            print(f"{center_result}\n{left_result}\n{right_result}")
            time_end = 999999999999999
            # voice = gTTS("조명이 설정되었습니다", lang='ko')
            # voice.save("voice.mp3")
            # playsound.playsound("voice.mp3")
            # os.remove("voice.mp3")
            # current_time = 0
        else:
            pass




    cv2.imshow('PoseModuleTest', output_image)
    if key == 27:
        break

cap.release()


