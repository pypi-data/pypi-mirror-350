# -*- coding: utf-8 -*-
import copy
import csv
import time

import requests
import json
from typing import List, Dict

import config
Clientinfox = {}
client = config.Clientassign(Clientinfox)


def get_SegSearchCandidates(Query: str, Candidates: List[Dict]) -> str or None:
    """
    获取分段搜索候选结果。

    :param Query: 搜索查询字符串
    :param Candidates: 候选结果列表，每个元素是一个字典，包含 "Score", "Text", "Attrs" 等键
    :return: 按分数排序后的前 5 个候选结果的 JSON 字符串，如果请求失败则返回 None
    """
    api_url = "https://genie.bytedance.com/pre/entsol/genie/skills/it-service/common/SegSearchCandidates"
    payload = {
        "Query": Query,
        "TopN": 0,
        "Candidates": Candidates
    }

    headers = {
        'Authorization': 'Basic bWFzLTZrMGJxLWgwMmhxbDM4MjQtMzJrcXQ6YTljNDIwMWJlOTc4OTg4MDRhZmZiNTQyMzA2ZTMxMzU=',
        'Content-Type': 'application/json'
    }

    try:
        # 发起 POST 请求
        response = requests.post(api_url, headers=headers, json=payload)
        # 检查响应状态码
        response.raise_for_status()
        result = response.json()
        if result and 'Candidates' in result:
            top_5_scores = sorted(result['Candidates'], key=lambda x: x.get('Score', 0), reverse=True)[:5]
            return json.dumps(top_5_scores, ensure_ascii=False)
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")
    except (KeyError, ValueError) as e:
        print(f"处理响应数据时发生错误: {e}")

    return None


def get_query_vector(MinScore, QueryValue, size, vec_type,AssetModelBizTypes):
    url = "https://open-itam-mig-pre.bytedance.net/v1/query_vector"

    payload = json.dumps({
        "From": 0,
        "Size": size,
        "MinScore": MinScore,
        "AssetModelFieldsWithAnd": [
            {
                "FieldName": vec_type,  # vec_type: vec_neme/vec_description
                "FieldType": "knn",
                "QueryValue": QueryValue
            }
        ],
        "AssetModelFieldsWithOR": None,
        "SPUIDs": None,
        "AssetModelBizTypes": AssetModelBizTypes
    })
    headers = {
        'Authorization': client.authorization,
        'x-use-ppe': '1',
        'x-tt-env': client.x_tt_env,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    info = {
        'input': {'用户输入/userInput': 'Autodesk 3Ds MAX'},
        'output': {'用户输入/output': 'Autodesk 3Ds MAX'},
        'rt': True,
        'label': []

    }
    info_list = []
    a = 0
    # 读取文件it_assistant/data/software_spu.csv
    with open('data/software_spu.csv', 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name_zh'] != "--":
                a = a + 1

                row_ = row['name_zh'].lower()
                row_ = row_.replace(' ', '')
                info['input'] = {'用户输入/userInput': row['name_zh']}
                info['output'] = {'用户输入/output': row_}
                res = json.loads(get_query_vector(0.6, [row_], 4, "vec_name"))
                for i in res['body']['Results']:
                    info['label'].append({'socre': i['Score'], 'label': i['Item']['name_zh']})
                print(a)
            info_list.append(copy.deepcopy(info))
            # 将info_list写入本地文件
           # 异常报错或退出时将info_list写入本地文件

    with open('test_data/software_spu_res_xiaoxie.csv', 'w', encoding='utf-8') as file:
        json.dump(info_list, file, ensure_ascii=False)
