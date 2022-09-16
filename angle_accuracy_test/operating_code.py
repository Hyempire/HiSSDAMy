import copy
import os
import cv2
import mediapipe as mp
import pprint
import random
import json
from utils import *
import PoseModule as poseModule

"""피험자 설정"""
# 피험자 이름 인풋
subject_name = input("피험자의 이름(HongGilding) : ")
print()

# 폴더 구조 생성
directory_name = './TestResults/' + subject_name
os.mkdir(directory_name)
captures_directory_name = './TestResults/' + subject_name + '/captures'
os.mkdir(captures_directory_name)
landmarks_directory_name = './TestResults/' + subject_name + '/landmarks'
os.mkdir(landmarks_directory_name)

# 엑셀 파일 생성
tries = ['try1', 'try2', 'try3', 'try4', 'try5']
angles = ['초기값', '0', '30', '60']
excel_dict = {}
excel_file_location = directory_name + '/' + subject_name + '_distances.xlsx'
for t in tries:
    excel_dict[t] = {}
    for a in angles:
        excel_dict[t][a] = 'default'
# dict_to_excel(excel_dict, excel_file_location)

# 확인을 위한 엑셀 파일용 딕셔너리 출력
for k in excel_dict:
    print(f"{k} -- {excel_dict[k]}")


"""영상 처리"""
print("\n\n")
print("실험을 시작합니다")

test_dict = copy.deepcopy(excel_dict)
angle_count = 0
try_count = 1
count = 0

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
        # 각도를 구하기 위한 거리값! 양수면 오른쪽, 음수면 왼쪽 쳐다보고 있는 거
        angleDist = rightDist - leftDist

        cv2.imshow('AngleAccuracyTest', output_image)
        if cv2.waitKey(1) == 27:
            break


        """각 try에서, 각도를 랜덤으로 배정하고, 이미 실행한 try-각도 element는 test_dict에서 삭제함"""
        keyboard_input = cv2.waitKey(300)
        try_key = 'try' + str(try_count)
        if keyboard_input == ord('a') and angleDist:
            if try_count < 6:
                if angle_count == 0:
                    key_angle = '초기값'
                    # val_result = test_dict[try_key].pop(key_angle)
                    # print(try_key, key_angle)       # 현재 진행중인 try, angle 확인
                    # pprint.pprint(test_dict)  # 진행한 try, angle 제거했는지 확인

                    """여기에, 각 try-angle 마다 실행할 코드 입력"""
                    print(f"{try_key}입니다. 초기값 받아오는 중입니다")

                    # text_input = input()


                        # 엑셀에  distance 값 넣기
                    excel_dict[try_key]['초기값'] = angleDist
                    # 확인을 위한 딕셔너리 출력
                    for k in excel_dict:
                        print(f"{k} -- {excel_dict[k]}")

                    # 이미지 저장
                    capture_file_path = captures_directory_name + '/capture_' + try_key + '_' + str(key_angle) + '.png'
                    cv2.imwrite(capture_file_path, image)

                    # json 파일 저장
                    json_file_path = landmarks_directory_name + '/landmarks_' + try_key + '_' + str(key_angle) + '.json'
                    landmark_dict = {}
                    for landmark_index, landmark_value in enumerate(results.pose_landmarks.landmark):
                        landmark_dict[landmark_index] = {
                            'X': landmark_value.x,
                            'Y': landmark_value.y,
                            'Z': landmark_value.z,
                        }
                    save_as_json(landmark_dict, json_file_path)

                    angle_count += 1

                    key_angle = random.choice(list(test_dict[try_key].keys())[1:])
                    val_result = test_dict[try_key].pop(key_angle)
                    print(f"{try_key}입니다. {key_angle}도 방향을 바라봐주세요.")

                elif angle_count < 3:
                    # print(try_key, key_angle)       # 현재 진행중인 try, angle 확인
                    # pprint.pprint(test_dict)  # 진행한 try, angle 제거했는지 확인

                    """여기에, 각 try-angle 마다 실행할 코드 입력"""
                    # text_input = input()


                    # 엑셀에  distance 값 넣기
                    excel_dict[try_key][key_angle] = angleDist
                    # 확인을 위한 딕셔너리 출력
                    for k in excel_dict:
                        print(f"{k} -- {excel_dict[k]}")

                    # 이미지 저장
                    capture_file_path = captures_directory_name + '/capture_' + try_key + '_' + str(key_angle) + '.png'
                    cv2.imwrite(capture_file_path, image)

                    # json 파일 저장
                    json_file_path = landmarks_directory_name + '/landmarks_' + try_key + '_' + str(key_angle) + '.json'
                    landmark_dict = {}
                    for landmark_index, landmark_value in enumerate(results.pose_landmarks.landmark):
                        landmark_dict[landmark_index] = {
                                                            'X': landmark_value.x,
                                                            'Y': landmark_value.y,
                                                            'Z': landmark_value.z,
                                                        }
                    save_as_json(landmark_dict, json_file_path)

                    angle_count += 1

                    key_angle = random.choice(list(test_dict[try_key].keys())[1:])
                    val_result = test_dict[try_key].pop(key_angle)
                    print(f"{try_key}입니다. {key_angle}도 방향을 바라봐주세요.")
                elif angle_count < 4:
                    """여기에, 각 try-angle 마다 실행할 코드 입력"""
                    # text_input = input()

                    # 엑셀에  distance 값 넣기
                    excel_dict[try_key][key_angle] = angleDist
                    # 확인을 위한 딕셔너리 출력
                    for k in excel_dict:
                        print(f"{k} -- {excel_dict[k]}")

                    # 이미지 저장
                    capture_file_path = captures_directory_name + '/capture_' + try_key + '_' + str(key_angle) + '.png'
                    cv2.imwrite(capture_file_path, image)

                    # json 파일 저장
                    json_file_path = landmarks_directory_name + '/landmarks_' + try_key + '_' + str(key_angle) + '.json'
                    landmark_dict = {}
                    for landmark_index, landmark_value in enumerate(results.pose_landmarks.landmark):
                        landmark_dict[landmark_index] = {
                            'X': landmark_value.x,
                            'Y': landmark_value.y,
                            'Z': landmark_value.z,
                        }
                    save_as_json(landmark_dict, json_file_path)

                    angle_count += 1

                else:
                    print(f"\n{try_count+1}번째 try로 넘어갑니다\n")
                    try_count += 1
                    angle_count = 0
                    continue
            else:
                print("\n실험을 종료합니다\n")
                break

cap.release()

dict_to_excel(excel_dict, excel_file_location)


