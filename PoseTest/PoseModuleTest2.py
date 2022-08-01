
import cv2
import mediapipe as mp
import PoseModule as poseModule
import time
from gtts import gTTS
import playsound
import os
# from scipy.io import wavfile



center_direct_list = []
left_direct_list = []
right_direct_list = []
directionResult, center, left, right = poseModule.poseDetectDirect(center_direct_list, left_direct_list, right_direct_list,5, 1)

# if result == "timeout":
print("----------", center, left, right)

if len(center) >= len(left) and len(center) >= len(right):
    final_direct = "Center"
elif len(left) > len(center) and len(left) > len(right):
    final_direct = "Left"
elif len(right) > len(center) and len(right) > len(left):
    final_direct = "Right"
else:
    final_direct = "Center"     # 디폴트값 센터로 함
print(f"final direction = {final_direct}")

voice = gTTS("조명이 설정되었습니다", lang = 'ko')
voice.save("voice.mp3")
time.sleep(1)
playsound.playsound("voice.mp3")
os.remove("voice.mp3")








