"""
포즈 디텍션 및 값 추출 파트 잘 되는지 테스트하는 코드
"""


import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Empty Camera Frame")
            continue

        """포즈 디텍션 수행 및 값 추출"""
        # Pose 모델 작동
        image.flags.writeable = False
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        # Pose 특징점 그리기
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        output_image = image.copy()
        mp_drawing.draw_landmarks(
            output_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        image_height, image_width, _ = image.shape
        # 눈 좌우와 코의 x좌표값 구하기
        leftEyeInner = int(results.pose_landmarks.landmark[1].x * image_width)
        rightEyeInner = int(results.pose_landmarks.landmark[4].x * image_width)
        nose = int(results.pose_landmarks.landmark[0].x * image_width)
        # 왼쪽, 오른쪽 눈과 코 사이의 거리를 구하기
        leftDist = abs(leftEyeInner - nose)
        rightDist = abs(rightEyeInner - nose)
        centerDist = abs(rightDist - leftDist)
        # 각도를 구하기 위한 거리값!
        angleDist = rightDist - leftDist

        cv2.putText(
            output_image, text=str(angleDist), org=(10, 30),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(255,0,0), thickness=3)

        cv2.imshow('PoseModuleTest', output_image)
        if cv2.waitKey(1) == 27:
            break

cap.release()