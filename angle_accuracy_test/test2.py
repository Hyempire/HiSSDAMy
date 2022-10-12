""""
results.pose_landmarks에 값들이 담겨있다! 근데 normalizedlist 형식이다! 는걸 알아낸 코드
+ 결과를 랜드마크 인덱스 - 랜드마크 값 의 딕셔너리로 변환하는 코드
+ json으로 만듦
"""


import cv2
import mediapipe as mp
import pprint
from utils import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

try_list = ['try1', 'try2', 'try3', 'try4', 'try5']

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Empty Camera Frame")
            continue

        key = cv2.waitKey(1)

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        if key == ord('a'):
            print(f"랜드마크 개수: {len(results.pose_landmarks.landmark)}")

            landmark_dict = {}
            for landmark_index, landmark_value in enumerate(results.pose_landmarks.landmark):
                landmark_dict[landmark_index] = {
                    'X': landmark_value.x,
                    'Y': landmark_value.y,
                    'Z': landmark_value.z,
                }
            #     landmark_dict[landmark_index] = [landmark_value]
            pprint.pprint(landmark_dict)

            save_as_json(landmark_dict, "./json_test.json")

        else:
            pass

        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        if key == 27:
            break

cap.release()




