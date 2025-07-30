# -*- coding: utf-8 -*-

from it_assistant.ailyapp_client import AilyLarkClient
from it_assistant.lark_client import LarkdocsClient
from it_assistant.intent_detail import *
import datetime


# Testsuitelink = "https://bytedance.larkoffice.com/sheets/ZVzfsw4rMhkMF6tjtxmc4BdSnMb"



def do_ai_auto(Testsuitelink):
    """
    自动化执行AI测试用例
    """
    startAt = 0
    try:
        # 获取租户访问令牌
        tenant_access_token = AilyLarkClient().get_tenant_access_token()
        if not tenant_access_token:
            raise ValueError("未能获取到有效的租户访问令牌")
        # 通过文档链接获取spreadsheet_token
        spreadsheet_token = Testsuitelink.split("/")[-1]
        if not spreadsheet_token:
            raise ValueError("未能从文档链接中提取到有效的spreadsheet_token")
        # 读取表格用户输入
        spreadsheet = LarkdocsClient().get_the_worksheet(spreadsheet_token)
        if not spreadsheet:
            raise ValueError("未能获取到有效的工作表数据")
        for i in spreadsheet.sheets:
            column_count = i.grid_properties.column_count
            row_count = i.grid_properties.row_count
            sheet_id = i.sheet_id
            title = i.title
            if title == "测试集":
                # 构建JSON字符串
                json_str = {"ranges": [sheet_id + "!A1:A" + str(row_count)]}
                # 获取纯文本内容
                test = LarkdocsClient().get_plaintextcontent(json_str, spreadsheet_token, sheet_id)
                test = json.loads(test)
                userinput = test['data']['value_ranges'][0]['values']
                print(f"表头为{userinput[0]}")
                for i in range(1, row_count):
                    if userinput[i][0]:
                        if startAt == 0:
                            startAt = int(time.time())
                        # 创建会话
                        seseion_id = AilyLarkClient().create_ailysession(tenant_access_token)
                        if not seseion_id:
                            raise ValueError("未能成功创建会话")
                        # 创建消息
                        message_id = AilyLarkClient().create_ailysessionaily_message(tenant_access_token, seseion_id,
                                                                                     userinput[i][0])
                        if not message_id:
                            raise ValueError("未能成功创建消息")
                        # 创建运行实例
                        runs = AilyLarkClient().create_ailysession_run(tenant_access_token, seseion_id)
                        #可不需等待运行实例创建完成
                        #if not runs:
                        #    raise ValueError("未能成功创建运行实例")
                        time.sleep(1)
                    else:
                        return startAt, i
                        break
                return startAt, row_count
                break
    except KeyError as ke:
        print(f"KeyError 发生: 数据中缺少必要的键，错误详情: {ke}")
        return None, None
    except json.JSONDecodeError as jde:
        print(f"JSON 解析错误: {jde}")
        return None, None
    except ValueError as ve:
        print(f"值错误: {ve}")
        return None, None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None, None


def get_conversationlogs1(startAt):
    """
    对话ID 技能分发 用户输入
    res_data = {
            'intentID': 7485259579248705537,
            'skillLabels': ["GUI 设备/配件申请"],
            'userInput': "我要申请一个鼠标",

         }
         """
    data = webapiClient().get_intent_detail_list(startAt)


def get_conversationlogs(startAt, pageSize=10):
    """
    对话ID 技能分发 用户输入
    res_data = {
            'intentID': 7485259579248705537,
            'skillLabels': ["GUI 设备/配件申请"],
            'userInput': "我要申请一个鼠标",

         }
    """
    try:
        # 之前提到形参 'pageSize' 未填，这里假设默认值为 10，你可按需修改
        data = webapiClient().get_intent_detail_list(startAt, pageSize=10)
        return data
    except KeyError as ke:
        print(f"KeyError 发生: 数据中缺少必要的键，错误详情: {ke}")
        return None
    except IndexError as ie:
        print(f"IndexError 发生: 索引超出范围，错误详情: {ie}")
        return None
    except Exception as e:
        print(f"发生未知错误: {e}")
        return None


def write_reslut(data, Testsuitelink, title):
    """
    写入表格
    """
    try:
        # 解析 spreadsheet_token
        spreadsheet_token = Testsuitelink.split("/")[-1]

        # 生成新工作表名称
        new_sheet_title = f"{title}{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        sheetinfo = {"index": 0, "title": new_sheet_title}

        # 创建新工作表
        spreadsheet0 = LarkdocsClient().createsheets(spreadsheet_token, sheetinfo)
        sheet_id = spreadsheet0['sheet_id']

        # 准备表头数据
        headers = list(data[0].keys())
        header_data = [
            {
                "range": f"{sheet_id}!{chr(ord('A') + col)}1:{chr(ord('A') + col)}1",
                "values": [[[{"text": {"text": header}, "type": "text"}]]]
            }
            for col, header in enumerate(headers)
        ]

        # 写入表头
        LarkdocsClient().writesheets(spreadsheet_token, sheet_id, {"value_ranges": header_data})

        # 写入数据
        for row, row_data in enumerate(data, start=1):
            row_values = [
                {
                    "range": f"{sheet_id}!{chr(ord('A') + col)}{row + 1}:{chr(ord('A') + col)}{row + 1}",
                    "values": [[[{"text": {"text": str(row_data[header])}, "type": "text"}]]]
                }
                for col, header in enumerate(headers)
            ]
            LarkdocsClient().writesheets(spreadsheet_token, sheet_id, {"value_ranges": row_values})

        return True
    except KeyError as ke:
        print(f"KeyError 发生: 数据中缺少必要的键，错误详情: {ke}")
        return False
    except IndexError as ie:
        print(f"IndexError 发生: 索引超出范围，错误详情: {ie}")
        return False
    except Exception as e:
        print(f"发生未知错误: {e}")
        return False


if __name__ == '__main__':
    Testsuitelink = "https://bytedance.larkoffice.com/sheets/ZVzfsw4rMhkMF6tjtxmc4BdSnMb"
    startAt, num = do_ai_auto(Testsuitelink)
    data = webapiClient().get_intent_detail_list(startAt, num)
    data_qqq = webapiClient().get_intent_detail_llm(data)
    aaaa = write_reslut(data_qqq, Testsuitelink, "测试")
