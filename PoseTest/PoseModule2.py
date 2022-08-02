import cv2
import mediapipe as mp
import PoseModule as poseModule
import time
import sys
from gtts import gTTS
# import playsound
import os
import winsound

# pose 돌리는데 필요한 모듈들을 변수에 담아줌
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 웹캠을 연결함
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# pose 돌리는 데 필요한 설정
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def switchPoseDirection(timer_second=2, center_threshold=7):

    # 위치 여부 판정값 리스트 초기화
    center_result = []
    left_result = []
    right_result = []

    # 파라미터 초기화
    end = timer_second
    center_threshold = center_threshold
    # 타이머 시간 초기화
    time_end = sys.maxsize

    # 카메라가 열려 있을 때
    while cap.isOpened():
        # 카메라 프레임을 가져와라
        success, image = cap.read()
        if not success:
            print("EMPTY CAMERA FRAME")
            continue

        # 포즈 디텍팅 인공지능
        pose_results, output_image = poseModule.detectPose(image, pose)
        # 키 입력 대기 코드
        key = cv2.waitKey(1) & 0xFF

        # 포즈가 인식 되었을 때
        if pose_results.pose_landmarks:
            # 방향 판정
            directionResult, center, left, right = poseModule.poseDirection(output_image, pose_results,
                                                                            center_result, left_result, right_result,
                                                                            threshold=center_threshold)

            """타이머 부분 : a를 눌렀을 때 -- 나중에 스위치로 바꾸기"""
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
                # print(f"{center_result}\n{left_result}\n{right_result}")

                if len(center_result) >= len(left_result) and len(center_result) >= len(right_result):
                    final_direct = "Center"
                elif len(left_result) > len(center_result) and len(left_result) > len(right_result):
                    final_direct = "Left"
                elif len(right_result) > len(center_result) and len(right_result) > len(left_result):
                    final_direct = "Right"
                else:
                    final_direct = "Center"  # 디폴트값 센터로 함
                print(f"final direction = {final_direct}")
                print("-"*80)


                """음성 안내 재생 부분"""
                # if final_direct == "Center":
                #     voice = gTTS("텔레비전이 설정되었습니다", lang='ko')
                # elif final_direct == "Left":
                #     voice = gTTS("조명이 설정되었습니다", lang='ko')
                # elif final_direct == "Right":
                #     voice = gTTS("에어컨이 설정되었습니다", lang='ko')
                # else:
                #     voice = gTTS("버튼을 다시 눌러주세요", lang='ko')

                # voice.save("VoiceResult.wav")
                # winsound.Playsound("VoiceResult.wav")
                # os.remove("VoiceResult.wav")

                time_end = sys.maxsize

            else:
                pass

        cv2.imshow('PoseModuleTest', output_image)
        if key == 27:
            break

    cap.release()

    return final_direct

# switchPoseDirection()