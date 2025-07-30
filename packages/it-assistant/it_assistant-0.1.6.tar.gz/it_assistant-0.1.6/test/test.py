# -*- coding: utf-8 -*-
import csv
import json
import copy
from it_assistant.do_ai import do_ai_auto

# 假设 Testsuitelink 是一个有效的文档链接
from it_assistant.openapi import get_query_vector

Testsuitelink = "your_testsuitelink_here"

try:
    startAt, row_count = do_ai_auto(Testsuitelink)
    if startAt is not None and row_count is not None:
        print(f"成功执行，startAt: {startAt}, row_count: {row_count}")
    else:
        print("执行过程中出现错误")
except Exception as e:
    print(f"调用 do_ai_auto 函数时出现异常: {e}")

def _test():
    #读取本地文件 读取software.csv 获取description_zh字段
    description_zh_list = []
    file_path = 'data/software_spu.csv'
    with open(file_path, 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['description_zh'] != "--":
                res = json.loads(get_query_vector(0.6, [row['description_zh']], 10, "vec_description"))
                lista = {'score': '', 'label': ''}
                res_label = []
                for j in res['body']['Results']:
                    lista['label'] = j['Item']['name_en']
                    lista['score'] = j['Score']
                    res_label.append(copy.deepcopy(lista))
                    info0 = {
                        "input": {"用户输入/userInput": "我想申请" + row['name_en']},  # 每条用例的输入
                        "output": {"用户输入/output": "我想申请" + row['name_en']},  # 每条用例的输出
                        "rt": "True",  # 用例的人工人为的结果 True/Flase
                        "label": res_label,  # 用例的评测指标，如技能识别,实际的输出,如有
                        "exp": res_label,  # ，如技能识别,用例打标
                        "artificial": res_label  # ，人工标准的值，如有
                    }

                description_zh_list.append(copy.deepcopy(info0))
                print(len(description_zh_list))

        #将description_zh_list写入本地文件
    with open('../test_data/software_spu_resxxxxxx.json', 'w') as file:
        json.dump(description_zh_list, file, ensure_ascii=False)


    """

    #创建csv并写入值
    with open('data/software_spu_res1.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(['用户输入/userInput', '用户输入/output', 'rt', 'label0', 'score0','label1','score1','label2','score2','label3','score3','label4','score4','label5','score5','label6','score6','label7','score7','label8','score8','label9','score9'])
        # 写入数据
        for info in description_zh_list:
            input_text = info['input']['用户输入/userInput']
            output_text = info['output']['用户输入/output']
            rt = info['rt']
            row_data = [input_text, output_text, rt]
            labels = info['label']
            for i in range(10):
                if i < len(labels):
                    row_data.extend([labels[i]['label'], labels[i]['score']])
                else:
                    row_data.extend(['', ''])
            writer.writerow(row_data)
    """
