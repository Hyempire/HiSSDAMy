
"""초기 설정! 복붙 추천"""
import cv2
import mediapipe as mp
import PoseModule as poseModule     # PoseModule에 detectPose()와 poseDirection() 함수가 있음

# pose 돌리는데 필요한 모듈들을 변수에 담아줌
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 웹캠을 연결함
cap = cv2.VideoCapture(0)

# pose 돌리는 데 필요한 설정
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

"""실제 AI 카메라 동작하는 코드"""
# 웹캠이 열려있는 동안 수행할 거임
while cap.isOpened():
    success, image = cap.read()     # 웹캠이 성공적으로 읽혔는지, 그리고 웹캠 프레임(image)을 받아옴
    # 웹캠 안 읽히면 오류 띄워주면서 다시 읽게 함
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # pose AI를 수행하는 코드
    pose_results, output_image = poseModule.detectPose(image, pose)

    # pose AI가 수행됐다면 수행할 코드
    if pose_results.pose_landmarks:
        # 어느 방향을 보고 있는지 알려주는 코드
        directionResult = poseModule.poseDirection(output_image, pose_results, threshold=15)

    else:
        continue

    cv2.imshow('PoseModuleTest', output_image)
    if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
