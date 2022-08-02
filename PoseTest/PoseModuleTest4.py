import cv2
import mediapipe as mp
import PoseModule2 as poseModule2

# pose 돌리는데 필요한 모듈들을 변수에 담아줌
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 웹캠을 연결함
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# pose 돌리는 데 필요한 설정
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

final_direct = poseModule2.switchPoseDirection(timer_second=2, center_threshold=7)

print(final_direct)     # a를 여러번 눌렀을 땐, 마지막으로 눌렀을 때 나오는 값이 final_direct에 저장됨
