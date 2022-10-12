import json
from pandas import DataFrame
import pandas as pd

def save_as_json(data, path):
    with open(path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def form_list_save_as_csv(data, path):
    tmp_data = {
        'name': [],
        'id': []
    }

    for index in data:
        name = index['name']
        id = index['id']

        tmp_data['name'].append(name)
        tmp_data['id'].append(id)
    
    data_df = DataFrame(tmp_data)
    data_df.to_csv(path, sep=',')

# None인지 구분해주는 기능 - fitbit 파일에서 동기화 시간이 없을 경우 대비해서 사용
def distinguish_none():
    pass

# 엑셀 관련
def excel_to_dict(excel):
    dataframe = pd.read_excel(excel, engine='openpyxl')
    dataframe = dataframe.T
    dataframe = dataframe.to_dict()
    return dataframe

def dict_to_excel(dict1, output_name):
    dataframe = pd.DataFrame(dict1)
    dataframe = dataframe.T
    dataframe.to_excel(output_name, index=True)