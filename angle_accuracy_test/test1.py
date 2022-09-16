"""
dict_to_excel() 함수 테스트
"""

from utils import *

my_dict = {
    "0":{"try1": 11, "try2": 11, "try3": 11, "try4": 11, "try5": 11},
    "30":{"try1": 11, "try2": 11, "try3": 11, "try4": 11, "try5": 11},
    "60":{"try1": 11, "try2": 11, "try3": 11, "try4": 11, "try5": 11}
}

dict_to_excel(my_dict, "my_excel.xlsx")
