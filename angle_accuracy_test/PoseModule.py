import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# 포즈 디텍션 수행
def detectPose(image, pose):
    """
    포즈 디텍션을 수행하는 함수
    :param image: 영상 프레임
    :param pose: mp.solutions.pose.Pose()를 담고 있는 변수
    :return:
        results : 이미지 위에 특징점을 출력한 아웃풋 이미지
        output_image : 랜드마크 출력하는 이미지. 출력하고 싶지 않으면 무시해도 됨
    """

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

    return results, output_image


# 방향 아웃풋
def poseDirection(image, results, center_direct_list, left_direct_list, right_direct_list, threshold=15):
    """
    방향 결과를 알려주는 함수
    :param image: 영상 프레임
    :param results: DetectPose의 ruturn값인 results
    :param threshold: 좌우와 가운데를 구별할 문턱값. 클수록 Center의 범위가 넓어짐
    :return:
        directResult : 방향 결과 string
    """

    image_height, image_width, _ = image.shape

    # 눈 좌우와 코의 x좌표값 구하기
    leftEyeInner = int(results.pose_landmarks.landmark[1].x * image_width)
    rightEyeInner = int(results.pose_landmarks.landmark[4].x * image_width)
    nose = int(results.pose_landmarks.landmark[0].x * image_width)

    # 왼쪽, 오른쪽 눈과 코 사이의 거리를 구하기
    leftDist = abs(leftEyeInner - nose)
    rightDist = abs(rightEyeInner - nose)
    centerDist = abs(rightDist - leftDist)

    if centerDist <= threshold:
        directResult = "Center"
        center_direct_list.append("Center")
        cv2.putText(
            image, text=f"Center", org=(10, 30),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=255, thickness=3)
    elif leftDist > rightDist:
        directResult = "Left"
        left_direct_list.append("Left")
        cv2.putText(
            image, text=f"Left", org=(10, 30),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=255, thickness=3)
    else:
        directResult = "Right"
        right_direct_list.append("Right")
        cv2.putText(
            image, text=f"Right", org=(10, 30),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=255, thickness=3)

    return directResult, center_direct_list, left_direct_list, right_direct_list


# def poseDetectDirect(center_direct_list, left_direct_list, right_direct_list, sec=3, imshow=1):
#     """
#     pose detection 수행하고 오른쪽 앞 왼쪽 판별해주는 함수
#     :param imshow: 영상 보여줄 것인지. 1이면 보여주고 0이면 안보여주고 왼,가,오 값만 던져줌
#     :return:
#         directionResult : Left, Center, Right 문자열값
#     """
#
#     # pose 돌리는데 필요한 모듈들을 변수에 담아줌
#     mp_drawing = mp.solutions.drawing_utils
#     mp_drawing_styles = mp.solutions.drawing_styles
#     mp_pose = mp.solutions.pose
#
#     # 웹캠을 연결함
#     cap = cv2.VideoCapture(0)
#
#     # pose 돌리는 데 필요한 설정
#     pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
#
#     # 타이머 지정
#     time_end = time.time() + sec
#
#     """실제 AI 카메라 동작하는 코드"""
#     # 웹캠이 열려있는 동안 수행할 거임
#     while cap.isOpened():
#
#         current_time = time.time()
#
#         success, image = cap.read()  # 웹캠이 성공적으로 읽혔는지, 그리고 웹캠 프레임(image)을 받아옴
#         # 웹캠 안 읽히면 오류 띄워주면서 다시 읽게 함
#         if not success:
#             print("Ignoring empty camera frame.")
#             continue
#
#         # pose AI를 수행하는 코드
#         pose_results, output_image = detectPose(image, pose)
#
#         # pose AI가 수행됐다면 수행할 코드
#         if pose_results.pose_landmarks:
#
#             # 어느 방향을 보고 있는지 알려주는 코드
#             directionResult, center, left, right = poseDirection(output_image, pose_results, center_direct_list, left_direct_list, right_direct_list, threshold=7)
#
#         else:
#             continue
#
#         # 영상 보여줄건지
#         if imshow == 1:
#             cv2.imshow('PoseModuleTest', output_image)
#             if cv2.waitKey(5) & 0xFF == 27:
#                 break
#         else:
#             print(directionResult)
#
#         # 시간이 다 되면 최종 리스트 값을 저장하고 함수를 빠져나옴
#         if current_time >= time_end:
#             final_center, final_left, final_right = center, left, right
#             break
#
#     cap.release()
#
#     return directionResult, final_center, final_left, final_right

# def timer():
#     time_end = time.time() + 2
#     while 1:
#         current_time = time.time()
#         print(current_time)
#         if current_time >= time_end:
#             result = "timeout"
#             break
#     return result