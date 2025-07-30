# -*- coding: utf-8 -*-
import http.client
import json
import time
import requests
headers = {
    'cookie':'X-Kunlun-SessionId=L%3A3b34958803f34f43a52c.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2YWwiOnsidGVuYW50X2lkIjozOTAsInVzZXJfaWQiOjE3MjIxNjYwNzMxOTk2NDUsInRlbmFudF9kb21haW5fbmFtZSI6ImFwYWFzIiwic2Vzc2lvbl92ZXJzaW9uIjoidjIwMjAtMDUtMTkiLCJ3c190b2tlbiI6Ilc6OTk3Y2MwNTA3OTRlNGFmYWFkYzEiLCJsb2dpbl90b2tlbiI6IjE3MDE3ZmFlMWJlNjVlMzdzSzBhMzA0ZjY0N2MyZmFjY2QwSjRFYmNmNGVjNzAzZDgwOWYxNDVnNDY0MzY1ZjEyNWI0YmZlZDhhTmMiLCJzb3VyY2VfY2hhbm5lbCI6ImZlaXNodSIsInRlbmFudF9rZXkiOiI3MzY1ODhjOTI2MGYxNzVkIiwiZXh0ZXJuYWxfZG9tYWluX25hbWUiOiJieXRlZGFuY2UiLCJvcmlnaW5hbF90ZW5hbnRfaWQiOjAsIm9yaWdpbmFsX3VzZXJfaWQiOjAsImlkcF9jaGFubmVsIjoiIn0sImV4cCI6MTc1ODk0MTY3MH0.l9yn5zbWFhOEJml5iA69TpFwZ7qgLMzj7L0cj4Ryozc; passport_web_did=7487801556726579201; passport_trace_id=7487801556748156956; QXV0aHpDb250ZXh0=2f506053fdd544e7aa0df84c66a287f9; locale=zh-CN; landing_url=https://accounts.feishu.cn/accounts/page/login?app_id=107&no_trap=1&redirect_uri=https%3A%2F%2Fapaas.feishu.cn%2Fai%2Fspring_f17d05d924__c%2Fmanagement%2Fchat-log; _gcl_au=1.1.1249684330.1743389657; s_v_web_id=verify_m8wh6ssk_JRUTLUkb_AJsu_4Xjm_ANzV_gLPDip941iqw; __tea__ug__uid=7487801495396992562; _ga=GA1.2.1834362348.1743389657; _gid=GA1.2.758422620.1743389658; session=XN0YXJ0-4e7g6c2c-da65-4492-a6f6-6413002bd949-WVuZA; session_list=XN0YXJ0-4e7g6c2c-da65-4492-a6f6-6413002bd949-WVuZA; login_recently=1; _ga_VPYRHN104D=GS1.1.1743389657.1.1.1743389669.48.0.0; msToken=4W_kQaUJyB5jBl5FX8vjfY6SYAFcNAp7NiDqM3-QyBN0XIF24a5SyaOeTpfzIZAuNfH-cGjXK1u3tNXV3ETo8Z2ZTQFLGSTFF2KmMr35XQsODVrddz8FdHAfyJg4F7ayxiDsicO5ObKgK0Y_95Bq1d12vKKbJ99vm9IZWEpcRFLG; kunlun-session-v2=L%3A3b34958803f34f43a52c.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2YWwiOnsidGVuYW50X2lkIjozOTAsInVzZXJfaWQiOjE3MjIxNjYwNzMxOTk2NDUsInRlbmFudF9kb21haW5fbmFtZSI6ImFwYWFzIiwic2Vzc2lvbl92ZXJzaW9uIjoidjIwMjAtMDUtMTkiLCJ3c190b2tlbiI6Ilc6OTk3Y2MwNTA3OTRlNGFmYWFkYzEiLCJsb2dpbl90b2tlbiI6IjE3MDE3ZmFlMWJlNjVlMzdzSzBhMzA0ZjY0N2MyZmFjY2QwSjRFYmNmNGVjNzAzZDgwOWYxNDVnNDY0MzY1ZjEyNWI0YmZlZDhhTmMiLCJzb3VyY2VfY2hhbm5lbCI6ImZlaXNodSIsInRlbmFudF9rZXkiOiI3MzY1ODhjOTI2MGYxNzVkIiwiZXh0ZXJuYWxfZG9tYWluX25hbWUiOiJieXRlZGFuY2UiLCJvcmlnaW5hbF90ZW5hbnRfaWQiOjAsIm9yaWdpbmFsX3VzZXJfaWQiOjAsImlkcF9jaGFubmVsIjoiIn0sImV4cCI6MTc1ODk0MTY3MH0.l9yn5zbWFhOEJml5iA69TpFwZ7qgLMzj7L0cj4Ryozc; kunlun-session-token=2b32fc3c28f44fb89bab94ad072a05c9f2f844c49705c95d76bae40479a189b7; _tea_utm_cache_1229=undefined; sl_session=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM0MzI4NzEsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtZXRhIjoiQVdIazBuRzhRUUFDQUFBQUFBQUFBQUZuNmdQWUFVNEFBV2ZxQTlnQlRnQUJaK29ENWRES3dBSUNLZ0VBUVVGQlFVRkJRVUZCUVVKdU5tZFFiRE40ZDBGQlp6MDkiLCJzdW0iOiJlMmM4YTIwMTcyMDcxNmVjYTFiOWRlOTQ5Yjc3OGJkNDczOGIzOTAwNWJiNTJhYTkyOTM2YTRhZWIzMGI2ZTY0IiwibG9jIjoiemhfY24iLCJhcGMiOiJSZWxlYXNlIiwiaWF0IjoxNzQzMzg5NjcxLCJzYWMiOnsiVXNlclN0YWZmU3RhdHVzIjoiMSIsIlVzZXJUeXBlIjoiNDIifSwibG9kIjpudWxsLCJjbmYiOnsiamt0IjoiYkx6aTdPRDBHS09mNllOQ0xGamtPZWtuQkNRSHM2ZFh5STdmcTVubE93VSJ9LCJucyI6ImxhcmsiLCJuc191aWQiOiI3MDUzOTk0MzAyMzAwNTUzMjE4IiwibnNfdGlkIjoiMSIsIm90IjozLCJjdCI6MTc0MzM4OTY3MCwicnQiOjE3NDMzODk2NzB9fQ.2pQlqU6fuqnw_iqtJe1sH1FfSSXBpFQ0RAoaRccxHEaHSBvqsdc9_7e4zjgcHOhTjISi3mGw3EC3EXftLj5Otw; passport_app_access_token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM0MzI4NzIsInVuaXQiOiJldV9uYyIsInJhdyI6eyJtX2FjY2Vzc19pbmZvIjp7IjEwNyI6eyJpYXQiOjE3NDMzODk2NzIsImFjY2VzcyI6dHJ1ZX19LCJzdW0iOiJlMmM4YTIwMTcyMDcxNmVjYTFiOWRlOTQ5Yjc3OGJkNDczOGIzOTAwNWJiNTJhYTkyOTM2YTRhZWIzMGI2ZTY0In19.jtfbxALtDnZYTJx4cb6ohPy2uDVCHTuh0x-Dg7Ui1F4vMO3aka7rvOeZTIwGJ7IlAn0b-OjBOWQEVQvHthhEwQ; swp_csrf_token=a239a297-e0f7-4820-aa3a-6349c8a04977; t_beda37=10a0c227407070710f979ef9d5b530118d080fd0ec27f2c3ce04c251a5a20d70',
    'x-kunlun-token': '17017fae1be65e37sK0a304f647c2faccd0J4Ebcf4ec703d809f145g464365f125b4bfed8aNc',
    'Content-Type': 'application/json'
}
itamheaders = {
  'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InYyIiwidHlwIjoiSldUIn0.eyJleHAiOjE3NDI1NDYyMTcsImp0aSI6ImJKMk9hV0dkanU5QStMMXciLCJpYXQiOjE3NDEyNTAyMTcsImlzcyI6InRhbm5hIiwic3ViIjoiMzgzMDMxOUBieXRlZGFuY2UucGVvcGxlIiwidGVuYW50X2lkIjoiYnl0ZWRhbmNlLnBlb3BsZSIsInRlbmFudF9uYW1lIjoiIiwicHJvamVjdF9rZXkiOiJjcm1TZmdIVmU1dXhIMHJyIiwidW5pdCI6ImV1X25jIiwiYXV0aF9ieSI6Mn0.eHghtX4NOnD1uD65bzqv7n1J3mtnPPXJoVKIWDwl4PMZPkqc3FisH4RMXxDqeOyDCgRHYhmam7VEenl8T0UIKpzI8ad8yMiZytvAkNhclLjCdmokLB7DdwnbO1qeDLxdqjL-S3da0KHHkOT8j-rWR94XJ0N7T_snoko4Ovsp13w',
  'Content-Type': 'application/json'

}

class webapiClient:
    def __init__(self):
        """
       初始化 Client 实例,tenant_access_token 会在 Client 初始化时自动获取
        """
        self.headers = headers
        self.itamheaders = headers
        self.conn = http.client.HTTPSConnection("apaas.feishu.cn")

    def get_intent_detail_list1(self, startAt,pageSize):
        """
        outdata:
            对话ID 技能分发 用户输入
           res_ = {
          'intentID': 7485259579248705537,
          'userInput': "我要申请一个鼠标",
          'skillLabels': ["GUI 设备/配件申请"],
           'apply_day':"",
          'apply_num':"",
          'asset_name':"",
          'device_type':""
           }
        """
        endAt = int(time.time())
        payload = json.dumps({
            "startAt": startAt,
            "endAt": endAt,
            "matchIntentID": "",
            "matchStatus": [],
            "pageSize": pageSize+10
        })
        self.conn.request("POST",
                          "/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/stats/intent_detail_list",
                          payload, self.headers)
        res = self.conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))
        res_list = []

        for i in data['data']['intentDetailList']:
            if i['channelType'] in ["LARK_OPEN_API","LARK_BOT","ANONYMOUS_CUI_SDK"]:
                res_list.append(
                    {'对话日志/intentID': i['intentID'],
                     '用户输入/userInput': i['userInput'],
                     '数据是否有效/isdatavalid': "是",
                     '语言/language': "zh",
                     '是否 IT 问题/isITproblem': "是",
                     '业务场景/businessscenario': "NULL",
                     '分发技能/skill': i['skillLabels'],
                     '型号关键字词/asset_name': "NULL",
                     '型号类型/device_type': "NULL",
                     '匹配型号/AssetNamelist': "NULL",
                     })


        return res_list

    def get_intent_detail_list(self, startAt, pageSize):
        """
        outdata:
            对话ID 技能分发 用户输入
           res_ = {
          'intentID': 7485259579248705537,
          'userInput': "我要申请一个鼠标",
          'skillLabels': ["GUI 设备/配件申请"],
           'apply_day':"",
          'apply_num':"",
          'asset_name':"",
          'device_type':""
           }
        """
        # 输入参数类型和范围检查
        if not isinstance(startAt, int) or startAt < 0:
            raise ValueError("startAt 必须是一个非负整数")
        if not isinstance(pageSize, int) or pageSize < 0:
            raise ValueError("pageSize 必须是一个非负整数")

        endAt = int(time.time())
        payload = json.dumps({
            "startAt": startAt,
            "endAt": endAt,
            "matchIntentID": "",
            "matchStatus": [],
            "pageSize": pageSize + 10
        })
        try:
            self.conn.request("POST",
                              "/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/stats/intent_detail_list",
                              payload, self.headers)
            res = self.conn.getresponse()

            # 检查响应状态码
            if res.status != 200:
                raise http.client.HTTPException(f"请求失败，状态码: {res.status}, 原因: {res.reason}")

            data = res.read()
            try:
                data = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                raise ValueError("无法将响应数据解析为 JSON 格式")

            # 检查响应数据结构
            if 'data' not in data or 'intentDetailList' not in data['data']:
                raise ValueError("响应数据缺少必要的字段 'data' 或 'intentDetailList'")

            res_list = []
            for i in data['data']['intentDetailList']:
                if i['channelType'] in ["LARK_OPEN_API", "LARK_BOT", "ANONYMOUS_CUI_SDK"]:
                    res_list.append({
                        '对话日志/intentID': i['intentID'],
                        '用户输入/userInput': i['userInput'],
                        '数据是否有效/isdatavalid': "是",
                        '语言/language': "zh",
                        '是否 IT 问题/isITproblem': "是",
                        '业务场景/businessscenario': "NULL",
                        '分发技能/skill': i['skillLabels'],
                        '型号关键字词/asset_name': "NULL",
                        '型号类型/device_type': "NULL",
                        '匹配型号/AssetNamelist': "NULL",
                    })
            return res_list
        except http.client.HTTPException as http_err:
            print(f"HTTP 请求错误: {http_err}")
            return []
        except ValueError as value_err:
            print(f"值错误: {value_err}")
            return []
        except Exception as general_err:
            print(f"发生未知错误: {general_err}")
            return []




    def get_intent_detail_llm0(self, res_list):
        """
        提取关键词
        'apply_day': "",'apply_num': "",'asset_name': "",'device_type': ""'对话日志/intentID': 7485264011232886786,
            '用户输入/userInput': "我要申请一个鼠标",
            '数据是否有效/isdatavalid': "是",
            '语言/language': "zh",
            '是否 IT 问题/isITproblem': "是",
            '业务场景/businessscenario': "NULL",
            '分发技能/skill': "NULL",
            '型号关键字词/asset_name': "NULL", #显示器
            '型号类型/device_type': "NULL",    # 设备 配件 软件
            '匹配型号/AssetNamelist': "NULL",
        """
        payload = ''
        for i in res_list:
            intentID = i['对话日志/intentID']
            urlintentID = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/intent/{intentID}?pageSize=20&statusFilter=%5B%5D&fieldFilter=_node_id&fieldFilter=status&fieldFilter=usages&fieldFilter=_node_name&fieldFilter=_node_type&fieldFilter=title_for_maker&fieldFilter=associate_id'
            response = requests.request("GET", urlintentID, headers=self.headers, data=payload)
            response = json.loads(response.text)
            for j in response['data']['steps']:
                if j['titleForMaker'] in ["槽位抽取","LLM 2"]:
                    nodeid = j['nodeID']
                    urlnodeid = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/association/{intentID}/node/{nodeid}?intentID={intentID}'
                    response = requests.request("GET", urlnodeid, headers=self.headers, data=payload)
                    data_nodeid = json.loads(response.text)
                    nodeid_output = json.loads(data_nodeid['data']['step']['output'])
                    if nodeid_output is not None and nodeid_output['response'] is not None:
                        # 判断是否为json格式
                        if not isinstance(nodeid_output['response'], dict):
                            nodeid_output['response'] = json.loads(nodeid_output['response'])
                        #i['apply_day'] = nodeid_output['response'].get('apply_day', 'NULL')
                        #i['apply_num'] = nodeid_output['response'].get('apply_num', 'NULL')

                        i['型号关键字词/asset_name'] = nodeid_output['response'].get('asset_name', 'NULL')
                        i['型号类型/device_type'] = nodeid_output['response'].get('device_type', 'NULL')
        return res_list


    def get_intent_detail_llm(self, res_list):
        """
        提取关键词：
        槽位提取：'apply_day': "",'apply_num': "",'asset_name': "",'device_type': ""
        表头字段：
        '对话日志/intentID': 7485264011232886786,
        '用户输入/userInput': "我要申请一个鼠标",
        '数据是否有效/isdatavalid': "是",
        '语言/language': "zh",
        '是否 IT 问题/isITproblem': "是",
        '业务场景/businessscenario': "NULL",
        '分发技能/skill': "NULL",
        '型号关键字词/asset_name': "NULL", #显示器
        '型号类型/device_type': "NULL",    # 设备 配件 软件
        '匹配型号/AssetNamelist': "NULL",
        """
        try:
            # 检查 res_list 是否为空
            if not res_list:
                print("输入的 res_list 为空")
                return []

            payload = ''
            for i in res_list:
                intentID = i['对话日志/intentID']
                urlintentID = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/intent/{intentID}?pageSize=20&statusFilter=%5B%5D&fieldFilter=_node_id&fieldFilter=status&fieldFilter=usages&fieldFilter=_node_name&fieldFilter=_node_type&fieldFilter=title_for_maker&fieldFilter=associate_id'
                response = requests.request("GET", urlintentID, headers=self.headers, data=payload)

                # 检查响应状态码
                response.raise_for_status()

                try:
                    response = response.json()
                except json.JSONDecodeError:
                    print(f"无法解析来自 {urlintentID} 的响应为 JSON 格式")
                    continue

                # 检查响应数据结构
                if 'data' not in response or 'steps' not in response['data']:
                    print(f"来自 {urlintentID} 的响应缺少必要的字段 'data' 或 'steps'")
                    continue

                for j in response['data']['steps']:
                    if j['titleForMaker'] in ["槽位抽取", "LLM 2"]:
                        nodeid = j['nodeID']
                        urlnodeid = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/association/{intentID}/node/{nodeid}?intentID={intentID}'
                        response_nodeid = requests.request("GET", urlnodeid, headers=self.headers, data=payload)

                        # 检查响应状态码
                        response_nodeid.raise_for_status()

                        try:
                            data_nodeid = response_nodeid.json()
                        except json.JSONDecodeError:
                            print(f"无法解析来自 {urlnodeid} 的响应为 JSON 格式")
                            continue

                        # 检查响应数据结构
                        if 'data' not in data_nodeid or 'step' not in data_nodeid['data'] or 'output' not in data_nodeid['data']['step']:
                            print(f"来自 {urlnodeid} 的响应缺少必要的字段 'data'、'step' 或 'output'")
                            continue

                        nodeid_output = json.loads(data_nodeid['data']['step']['output'])
                        if nodeid_output is not None and nodeid_output.get('response') is not None:
                            # 判断是否为 json 格式
                            if not isinstance(nodeid_output['response'], dict):
                                try:
                                    nodeid_output['response'] = json.loads(nodeid_output['response'])
                                except json.JSONDecodeError:
                                    print(f"无法解析 {urlnodeid} 响应中的 'response' 字段为 JSON 格式")
                                    continue
                            i['型号关键字词/asset_name'] = nodeid_output['response'].get('asset_name', 'NULL')
                            i['型号类型/device_type'] = nodeid_output['response'].get('device_type', 'NULL')

            return res_list
        except requests.RequestException as req_err:
            print(f"请求错误: {req_err}")
            return []
        except Exception as general_err:
            print(f"发生未知错误: {general_err}")
            return []



    def get_bestmatchitemforreturn(self,keyword):
        """
        mock数据，获取最佳匹配的sku/spu
        mock数据：公用配件列表、设备列表、软件列表
        todo：mock数据表格为飞书文档或者其他？
        """
        _urlGetBestMatchItemForReturn = "https://asset-mig-pre.bytedance.net/aily/api/itservice/ai/GetBestMatchItemForReturn"

        payload = json.dumps({
            "SearchKey": keyword,
            "AiUseType": 1,
            "ListReturnableAccessoryRequest": {
                "IsAll": True,
                "Page": {
                    "PageNum": 1,
                    "PageSize": 30
                },
                "OwnerUserID": "",
                "AccessoryApplyTypeList": []
            },
            "GetAssetListRequest": {
                "Status": 6,
                "Search": "",
                "IsAll": True,
                "SubStatusList": [
                    12,
                    18,
                    19
                ],
                "Page": {
                    "PageNum": 1,
                    "PageSize": 30
                },
                "OrganizationalUnitID": 1
            }
        })
        response = requests.request("GET", _urlGetBestMatchItemForReturn, headers=self.headers, data=payload)
        response = json.loads(response.text)

    def get_segsearchcandidates(self, res_list):
        #获取分数值
        ### 读取设备&配件的信息并拼接到text里面
        ### 遍历res_list中的device_name
        ###判断是否在asset.json里面
        ###调用算法接口获取设备&配件的分数值
        pass



if __name__ == '__main__':
    data = webapiClient().get_intent_detail_list(1742832000,10)
    data_qqq = webapiClient().get_intent_detail_llm(data)
    print("成都")
