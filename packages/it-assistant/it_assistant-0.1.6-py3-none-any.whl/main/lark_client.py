import json

import lark_oapi as lark
from lark_oapi.api.sheets.v3 import *


# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用

class LarkdocsClient:
    def __init__(self):
        """
        初始化 Client 实例,tenant_access_token 会在 Client 初始化时自动获取
        https://github.com/larksuite/oapi-sdk-python
        """
        self.app_id = "cli_a48be9fd54a5900d"
        self.app_secret = "pfiNeWKbkfbRvUunX3TrKdCCnftlUbxl"
        # 创建 Lark 客户端
        self.lark_client = lark.Client.builder().app_id(self.app_id).app_secret(self.app_secret).build()

    def get_the_worksheet(self, spreadsheet_token):

        # 获取工作表
        # 创建client
        # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
        # 构造请求对象
        try:
            request: QuerySpreadsheetSheetRequest = QuerySpreadsheetSheetRequest.builder() \
                .spreadsheet_token(spreadsheet_token) \
                .build()

            # 发起请求
            # option = self.lark_client.RequestOption.builder().user_access_token(
            # "u-hQ.Vthwt5blbznh92YFKhflkkfsAl5R3hW20l5cy07ag").build()
            response: QuerySpreadsheetSheetResponse = self.lark_client.sheets.v3.spreadsheet_sheet.query(request)

            # 处理失败返回
            if not response.success():
                lark.logger.error(
                    f"client.sheets.v3.spreadsheet_sheet.query failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
                return
            return response.data
            # 处理业务结果
            lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        except Exception as e:
            lark.logger.error(f"[lark]get user id by email failed, err: {e}")
            return None, e

    def get_plaintextcontent(self, ranges, spreadsheet_token, sheet_id):
        # 创建client
        # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
        # 构造请求对象
        # 构造请求对象
        # json_str = "{\"ranges\":[\"459f7e!A1:A1\"]}"
        body = ranges
        request: lark.BaseRequest = lark.BaseRequest.builder() \
            .http_method(lark.HttpMethod.POST) \
            .uri(f"/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{str(sheet_id)}/values/batch_get_plain") \
            .token_types({lark.AccessTokenType.TENANT}) \
            .body(body) \
            .build()

        # 发起请求
        response: lark.BaseResponse = self.lark_client.request(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(str(response.raw.content, lark.UTF_8))
        return str(response.raw.content, lark.UTF_8)


    def createsheets(self, spreadsheet_token, title):
        # 创建工作表
        # json_str = "{\"index\":0,\"title\":\"abc\"}"
        # 构造请求对象
        body = title
        request: lark.BaseRequest = lark.BaseRequest.builder() \
            .http_method(lark.HttpMethod.POST) \
            .uri(f"/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets") \
            .token_types({lark.AccessTokenType.TENANT}) \
            .body(body) \
            .build()

        # 发起请求
        response: lark.BaseResponse = self.lark_client.request(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(str(response.raw.content, lark.UTF_8))
        return json.loads(response.raw.content)['data']['sheet']


    def writesheets(self, spreadsheet_token, sheet_id, data):
        # 创建client
        # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
        # 构造请求对象
        # 构造请求对象
        json_str = "{\"value_ranges\":[{\"range\":\"HEJb8z!C1:C1\",\"values\":[[[{\"text\":{\"text\":\"abc\"},\"type\":\"text\"}]]]}]}"
        body = json.loads(json_str)
        body = data
        request: lark.BaseRequest = lark.BaseRequest.builder() \
            .http_method(lark.HttpMethod.POST) \
            .uri(
            f"/open-apis/sheets/v3/spreadsheets/{spreadsheet_token}/sheets/{sheet_id}/values/batch_update?user_id_type=open_id") \
            .token_types({lark.AccessTokenType.TENANT}) \
            .body(body) \
            .build()

        # 发起请求
        response: lark.BaseResponse = self.lark_client.request(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(str(response.raw.content, lark.UTF_8))


if __name__ == '__main__':
    spreadsheet_token = ""
    sheets = LarkdocsClient().get_the_worksheet(spreadsheet_token)
    for i in sheets.sheets:

        column_count = i.grid_properties.column_count
        row_count = i.grid_properties.row_count
        sheet_id = i.sheet_id
        title = i.title

        #print(column_count, row_count, sheet_id, title)
        json_str = {"ranges": ["459f7e!A1:A1"]}
        json_str = {"ranges": [sheet_id + "!A1:A" + str(row_count)]}
        test = LarkdocsClient().get_plaintextcontent(json_str, spreadsheet_token, sheet_id)
        test = json.loads(test)
        userinput = test['data']['value_ranges'][0]['values']
        print(f"表头为{userinput[0]}")
        i = 0
        for i in range(1,row_count):
            if userinput[i][0]:
                print(userinput[i][0])
            else:
                break





