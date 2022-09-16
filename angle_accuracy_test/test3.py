"""
딕셔너리에서 랜덤으로 나오게 하는거 테스트
"""


import pprint
import random

my_dict = {
    "try1":{"0": 11, "30": 11, "90": 11},
    "try2":{"0": 11, "30": 11, "90": 11},
    "try3":{"0": 11, "30": 11, "90": 11},
    "try4":{"0": 11, "30": 11, "90": 11},
    "try5":{"0": 11, "30": 11, "90": 11}
}

# k, v = my_dict['try2'].popitem()
# print(k, v)
# pprint.pprint(my_dict)

# for k1 in my_dict:
#     for i in range(3):
#         key = random.choice(list(my_dict[k1].keys()))
#         print(key)
#         val = my_dict[k1].pop(key)
#         print(val)
#         pprint.pprint(my_dict)


# while 무한루프문에서 구현하기
angle_count = 0
try_count = 1
while 1:
    try_key = 'try' + str(try_count)
    if try_count < 6:
        if angle_count < 3:
            key = random.choice(list(my_dict[try_key].keys()))
            val = my_dict[try_key].pop(key)

            print(key, val)
            pprint.pprint(my_dict)
            print("\n\n")


            angle_count += 1
        else:
            try_count += 1
            angle_count = 0
    else:
        break
