"""capture_coordinates 딕셔너리와, capture_item 딕셔너리 값이 온전히 있을 때, 각 캡쳐 이미지와 비슷한 포즈를 취할 때 그에 맞는 사물을 지정해주는 코드
    - capture_coordinates : captureTest.py에서 가져온 값임. 추후 이 두 파일을 연결할 필요가 있음
    - capture_item : 웹사이트에서 가져와야 하는 값들
    poseTest/captureModuleTest1.py와 같은 파일
"""

import cv2
import mediapipe as mp
import PoseModule as poseModule
import time
import sys

# pose 돌리는데 필요한 모듈들을 변수에 담아줌
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# 웹캠을 연결함
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# pose 돌리는 데 필요한 설정
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 캡쳐를 위한 변수
capture_count = 0
# 좌표 더미 데이터 ---------------------나중엔 captureModule.py에서 가져올 값들!!!!
capture_coordinates = {'capture1.png': {'left_eye_x': 246, 'right_eye_x': 222, 'nose_x': 223, 'leftDist': 23, 'rightDist': 1},
           'capture2.png': {'left_eye_x': 317, 'right_eye_x': 277, 'nose_x': 297, 'leftDist': 20, 'rightDist': 20},
           'capture3.png': {'left_eye_x': 375, 'right_eye_x': 353, 'nose_x': 377, 'leftDist': 2, 'rightDist': 24}}
# 타이머 시간 설정 (초)
end = 2
current_time = 1
time_end = sys.maxsize

leftDist_list = []
rightDist_list = []
leftDist_sum = 0
rightDist_sum = 0


while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("EMPTY CAMERA FRAME")
        continue
    key = cv2.waitKey(1) & 0xFF
    image_height, image_width, _ = image.shape

    # 포즈 모듈 실행 함수 실행
    pose_results, output_image = poseModule.detectPose(image, pose)

    # 눈 좌우와 코의 x좌표값 구하기
    leftEyeInner = int(pose_results.pose_landmarks.landmark[1].x * image_width)
    rightEyeInner = int(pose_results.pose_landmarks.landmark[4].x * image_width)
    nose = int(pose_results.pose_landmarks.landmark[0].x * image_width)

    """더미데이터!!!!! @수림언니!! 여기다가 뭔가 딕셔너리 형태로 넣어주세용"""
    capture_item = {'capture1.png': '조명', 'capture2.png': 'TV', 'capture3.png': '에어컨'}

    """좌표값 비교"""
    # 왼쪽, 오른쪽 눈과 코 사이의 거리를 구하기
    leftDist = abs(leftEyeInner - nose)
    rightDist = abs(rightEyeInner - nose)
    centerDist = abs(rightDist - leftDist)

    # 시선 추적 버튼을 누르면 2초동안 판단하겠다
    current_time = time.time()
    if key == ord('b'):
        leftDist_list = []
        rightDist_list = []
        leftDist_sum = 0
        rightDist_sum = 0
        time_end = current_time + end

    leftDist_list.append(leftDist)
    rightDist_list.append(rightDist)

    if current_time >= time_end:
        for i in leftDist_list:
            leftDist_sum += i
        leftDist_avg = leftDist_sum / len(leftDist_list)
        for i in rightDist_list:
            rightDist_sum += i
        rightDist_avg = rightDist_sum / len(rightDist_list)

        if len(capture_item) == 3:
            for img_name, item_name in capture_item.items():
                leftDist_standard = capture_coordinates[img_name]['leftDist']
                rightDist_standard = capture_coordinates[img_name]['rightDist']
                # 참고로, 포즈가 중복되는 지점이 있으면, capture.png 이름이 앞서는게 우선순위가 됨
                if (leftDist_standard - 5 <= leftDist_avg <= leftDist_standard + 5) and (rightDist_standard - 5 <= rightDist_avg <= rightDist_standard + 5):
                    detected_item = item_name
                    break
                else:
                    detected_item = 'Not Found'
                    continue
        else:
            print("쓰담이 사물 설정을 완료해주세요")
            pass

        print(f"final direction = {detected_item}")
        print("-" * 80)

        time_end = sys.maxsize
    else:
        pass

    cv2.imshow('PoseModuleTest', output_image)
    if key == 27:
        break

cap.release()