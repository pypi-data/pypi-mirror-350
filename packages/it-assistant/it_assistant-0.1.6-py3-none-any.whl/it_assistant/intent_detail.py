# -*- coding: utf-8 -*-
import copy
import http.client
import json
import time
import requests

from it_assistant.config import Clientin

import config
Clientinfox = {}
client = config.Clientassign(Clientinfox)

headers = {
            'cookie': client.cookie,
            'x-kunlun-token': client.x_kunlun_token,
            'Content-Type': "application/json"}
itamheaders = {
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6InYyIiwidHlwIjoiSldUIn0.eyJleHAiOjE3NDI1NDYyMTcsImp0aSI6ImJKMk9hV0dkanU5QStMMXciLCJpYXQiOjE3NDEyNTAyMTcsImlzcyI6InRhbm5hIiwic3ViIjoiMzgzMDMxOUBieXRlZGFuY2UucGVvcGxlIiwidGVuYW50X2lkIjoiYnl0ZWRhbmNlLnBlb3BsZSIsInRlbmFudF9uYW1lIjoiIiwicHJvamVjdF9rZXkiOiJjcm1TZmdIVmU1dXhIMHJyIiwidW5pdCI6ImV1X25jIiwiYXV0aF9ieSI6Mn0.eHghtX4NOnD1uD65bzqv7n1J3mtnPPXJoVKIWDwl4PMZPkqc3FisH4RMXxDqeOyDCgRHYhmam7VEenl8T0UIKpzI8ad8yMiZytvAkNhclLjCdmokLB7DdwnbO1qeDLxdqjL-S3da0KHHkOT8j-rWR94XJ0N7T_snoko4Ovsp13w',
    'Content-Type': 'application/json'

}


class webapiClient():
    def __init__(self):
        """
       初始化 Client 实例,tenant_access_token 会在 Client 初始化时自动获取
        """
        self.headers = headers
        self.itamheaders = headers
        self.conn = http.client.HTTPSConnection("apaas.feishu.cn")

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
                if i['channelType'] in ["LARK_OPEN_API", "LARK_BOT", "ANONYMOUS_CUI_SDK", "AILY_CUI_SDK"]:
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
        ii0 = []
        ii = {
            '对话日志/intentID': "7485264011232886786",
            '用户输入/userInput': "我要申请一个鼠标",
            '数据是否有效/isdatavalid': "是",
            '语言/language': "zh",
            '是否 IT 问题/isITproblem': "是",
            '业务场景/businessscenario': "NULL",
            '分发技能/skill': "NULL",
            '型号关键字词/asset_name': "NULL",  # 显示器
            '型号类型/device_type': "NULL",  # 设备 配件 软件
            '匹配型号/AssetNamelist': "NULL",
        }
        try:
            # 检查 res_list 是否为空
            if not res_list:
                print("输入的 res_list 为空")
                return []

            payload = ''
            for i in res_list:
                # intentID = i['对话日志/intentID']
                print("urlintentID_1:" + str(i))
                ii['对话日志/intentID'] = i
                intentID = str(i)
                urlintentID = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/intent/{intentID}?pageSize=20&statusFilter=%5B%5D&fieldFilter=_node_id&fieldFilter=status&fieldFilter=usages&fieldFilter=_node_name&fieldFilter=_node_type&fieldFilter=title_for_maker&fieldFilter=associate_id'
                response = requests.request("GET", urlintentID, headers=self.headers, data=payload)
                # sleep 3s
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
                    if j['titleForMaker'] in ["槽位抽取", "LLM 2", "LLM"]:
                        nodeid = j['nodeID']
                        urlnodeid = f'https://apaas.feishu.cn/ai/api/v1/conversational_runtime/namespaces/spring_f17d05d924__c/association/{intentID}/node/{nodeid}?intentID={intentID}'
                        response_nodeid = requests.request("GET", urlnodeid, headers=self.headers, data=payload)
                        time.sleep(1)
                        # 检查响应状态码
                        response_nodeid.raise_for_status()
                        try:
                            data_nodeid = response_nodeid.json()
                        except json.JSONDecodeError:
                            print(f"无法解析来自 {urlnodeid} 的响应为 JSON 格式")
                            continue

                        # 检查响应数据结构
                        if 'data' not in data_nodeid or 'step' not in data_nodeid['data'] or 'output' not in \
                                data_nodeid['data']['step']:
                            print(f"来自 {urlnodeid} 的响应缺少必要的字段 'data'、'step' 或 'output'")
                            continue

                        if not data_nodeid['data']['step']['output']:
                            ii['型号关键字词/asset_name'] = 'NULL'
                            ii['型号类型/device_type'] = 'NULL'
                        else:
                            nodeid_output = json.loads(data_nodeid['data']['step']['output'])
                            if nodeid_output is not None and nodeid_output.get('response') is not None:
                                # 判断是否为 json 格式
                                if not isinstance(nodeid_output['response'], dict):
                                    try:
                                        nodeid_output['response'] = json.loads(nodeid_output['response'])
                                    except json.JSONDecodeError:
                                        print(f"无法解析 {urlnodeid} 响应中的 'response' 字段为 JSON 格式")
                                        continue
                                ii['型号关键字词/asset_name'] = nodeid_output['response'].get('asset_name', 'NULL')
                                ii['型号类型/device_type'] = nodeid_output['response'].get('device_type', 'NULL')
                            else:
                                ii['型号关键字词/asset_name'] = 'NULL'
                                ii['型号类型/device_type'] = 'NULL'

                        ii0.append(copy.deepcopy(ii))
            # 对res_list中的用户输入/userInput去重

            return ii0
        except requests.RequestException as req_err:
            print(f"请求错误: {req_err}")
            return []
        except Exception as general_err:
            print(f"发生未知错误: {general_err}")
            return []

    def get_bestmatchitemforreturn(self, keyword):
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
        # 获取分数值
        ### 读取设备&配件的信息并拼接到text里面
        ### 遍历res_list中的device_name
        ###判断是否在asset.json里面
        ###调用算法接口获取设备&配件的分数值
        pass


if __name__ == '__main__':

    """
    data = [7498300843856445459,7498300827172667396,7498300811602296833,7498300842216161299,7498300799664340994,7498300843022991361,7498300875937595393,7498300870679248897,7498300855084810244,7498300861520494594,7498300893873750035,7498300861520707586,7498300855085400068,7498300888215207964,7498300921689260033,7498300853654634515,7498300905156657171,7498300912590094355,7498300912590225427,7498300881648435202,7498300896642334724,7498300918593994754,7498300952951111682,7498300915944423427,7498300952270372868,7498300988312141852,7498270448718184450,7498300984855494660,7498300891758723074,7498300954706231299,7498300965450973188,7498300969057173523,7498300948874149907,7498300997792055298,7498300984856543236,7498300952952406018,7498300978548244532,7498301012646920220,7498301028979818497,7498301028979965953,7498300997624692737,7498301016439570435,7498301023548833793,7498301051542503426,7498301035217993731,7498301019934670867,7498301041972969491,7498301017999245314,7498301045746483202,7498301077342011396,7498301052657909788,7498301021720215554,7498301032223424514,7498301021720363010,7498301045746991106,7498301068536496130,7498301087723159554,7498301090118533124,7498301072152231964,7498301075595870236,7498301087814991891,7498301080285888540,7498301102360346652,7498301099358355475,7498301132922896385,7498301087815565331,7498301134088962051,7498301100597805057,7498301077343469572,7498301074774491155,7498301160469282818,7498301169565106204,7498301134089453571,7498301126482427906,7498301120980680706,7498301183497633820,7498301139852984321,7498301136955015169,7498301122339438611,7498301136354787331,7498301169313890332,7498301197897711618,7498301136955392001,7498301197898170370,7498301180918906881,7498301131527110660,7498301134090420227,7498301181558407169,7498301138816729107,7498301150523064324,7498301190712967169,7498301224875229212,7498301165806649348,7498301233428119553,7498301226040770562,7498301231542681602,7498301187986227203,7498301216874758146,7498301216874889218,7498301241461358594,7498301186321235971,7498301241074499585,7498301234605981697,7498301187124609028,7498301202820841475,7498301202820923395,7498301190624231428,7498301234606686209,7498301234606833665,7498301260838387740,7498301212017999873,7498301206844669971,7498301280195493889,7498301193597026308,7498301283984228380,7498301271345201180,7498301330007588865,7498301321537241089,7498301235939688451,7498301313526186012,7498301330008211457,7498301322553065473,7498301334593568769,7498301313132265474,7498301317926404097,7498301322544889884,7498301656326062099,7498301362083627010,7498301358330331164,7498301335261396994,7498301280978173971,7498301322520969217,7498301350412075010,7498301366235922434,7498301385394847745,7498301350412435458,7498301359840509953,7498301294627438596,7498301317933645827,7498301410718318593,7498301339261960196,7498301370670710787,7498301395789463580,7498301355361239043,7498301317460377603,7498301317460574211,7498301397139357698,7498301303950327827,7498301330995576835,7498301377556824067,7498301415367655452,7498301410719399937,7498301408201261057,7498301398925492227,7498301415367966748,7498301415368114204,7498301444764876802,7498301413602918401,7498301452962758657,7498301444765188098,7498301444765319170,7498301452105465884,7498301436847554561,7498301457772150812,7498301470952243228,7498301411968729092,7498301481512845314,7498301474317975553,7498301457772642332,7498301462723526657,7498301444766400514,7498301462723854337,7498301479313817628,7498301454419116060,7498301486259863553,7498301474318680065,7498301454419394588,7498301479314276380,7498301463338319900,7498301501078011932,7498301463338483740,7498301496564940828,7498301518634614812,7498301496565104668,7498301482307551260,7498301506384166940,7498301501078700060,7498301518635302940,7498301473308835843,7498301461025718276,7498301496565956636,7498301506384887836,7498301506384986140,7498301501079519260,7498301455198224388,7498301523640631298,7498301529280364563,7498301557887926300,7498301553716625409,7498301540705878020,7498301522138529795,7498301578123509788,7498301578123673628,7498301540706287620,7498301573528207388,7498301572948787203,7498301530589478931,7498301524911734788,7498301578124247068,7498301540706762756,7498301615788179457,7498301590140207108,7498301614563049500,7498301600277872668,7498301524912521220,7498301591735287812,7498301598726012932,7498301595465039873,7498301591117332483,7498301600278708252,7498301601742880769,7498301634114371603,7498301635255599132,7498301539311894529,7498301638337118227,7498301656326062099,7498301634125660179]
    data_qqq = webapiClient().get_intent_detail_llm(data)
    #将data_qqq写入本地文件
    with open('../test_data/software_spu_resout.json', 'w') as file:
        json.dump(data_qqq, file, ensure_ascii=False)
    print("成都")
    """

    # 读取文件../test_data/software_spu_resout.json
    with open('../test_data/software_spu_resout.json', 'r') as file:
        data_qqq = json.load(file)
        for i in data_qqq:
            print(i['型号关键字词/asset_name'])
