import json

import lark_oapi as lark
from lark_oapi.api.auth.v3 import *
from lark_oapi.api.aily.v1 import *


# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.

class AilyLarkClient:
    def __init__(self):
        """
        初始化 Client 实例,tenant_access_token 会在 Client 初始化时自动获取
        """
        self.aily_app_id = "spring_f17d05d924__c"
        self.app_id = "cli_a6e3aea1a13c900c"
        self.app_secret = "J0fAPt3BL6bv4KUJV0dJMdTUdr0pv3xx"
        # 创建 Lark-tenant tenant客户端
        self.tlark_client = lark.Client.builder().app_id(self.app_id).app_secret(self.app_secret).build()

        # 创建 Lark-tenant user 客户端
        self.ulark_client = lark.Client.builder().enable_set_token(True).log_level(lark.LogLevel.DEBUG).build()

    def get_tenant_access_token(self):
        # 构造请求对象
        request: InternalTenantAccessTokenRequest = InternalTenantAccessTokenRequest.builder() \
            .request_body(InternalTenantAccessTokenRequestBody.builder()
                          .app_id(self.app_id)
                          .app_secret(self.app_secret)
                          .build()) \
            .build()

        # 发起请求
        response: InternalTenantAccessTokenResponse = self.tlark_client.auth.v3.tenant_access_token.internal(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.auth.v3.tenant_access_token.internal failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return
        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.raw, indent=4))
        tenant_access_token = json.loads(response.raw.content).get("tenant_access_token")
        if tenant_access_token:
            return tenant_access_token
        else:
            lark.logger.error(
                f"client.auth.v3.tenant_access_token.internal failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

    def create_ailysession(self, access_token):
        # 创建会话
        # 构造请求对象
        request: CreateAilySessionRequest = CreateAilySessionRequest.builder() \
            .request_body(CreateAilySessionRequestBody.builder()
                          .channel_context("{}")
                          .metadata("{}")
                          .build()) \
            .build()

        # 发起请求
        option = lark.RequestOption.builder().user_access_token(access_token).build()
        response: CreateAilySessionResponse = self.ulark_client.aily.v1.aily_session.create(request, option)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.aily.v1.aily_session.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return response.data.session.id

    def create_ailysessionaily_message(self, access_token, session_id, content):
        # 发送智能伙伴消息
        # 构造请求对象
        request: CreateAilySessionAilyMessageRequest = CreateAilySessionAilyMessageRequest.builder() \
            .aily_session_id(session_id) \
            .request_body(CreateAilySessionAilyMessageRequestBody.builder()
                          .content(content)
                          .content_type("MDX")
                          .idempotent_id("idempotent_id_1")
                          .build()) \
            .build()
        # 发起请求
        option = lark.RequestOption.builder().user_access_token(access_token).build()
        response: CreateAilySessionAilyMessageResponse = self.ulark_client.aily.v1.aily_session_aily_message.create(
            request,
            option)
        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.aily.v1.aily_session_aily_message.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return
        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return response.data.message.id

    def create_ailysession_run(self, access_token, aily_session_id):
        # 创建运行
        # 构造请求对象
        request: CreateAilySessionRunRequest = CreateAilySessionRunRequest.builder() \
            .aily_session_id(aily_session_id) \
            .request_body(CreateAilySessionRunRequestBody.builder()
                          .app_id(self.aily_app_id)
                          .build()) \
            .build()
        # 发起请求
        option = lark.RequestOption.builder().user_access_token(
            access_token).build()
        response: CreateAilySessionRunResponse = self.ulark_client.aily.v1.aily_session_run.create(request, option)
        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.aily.v1.aily_session_run.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))



if __name__ == '__main__':
    tenant_access_token = AilyLarkClient().get_tenant_access_token()
    seseion_id = AilyLarkClient().create_ailysession(tenant_access_token)
    print(seseion_id)
    message_id = AilyLarkClient().create_ailysessionaily_message(tenant_access_token, seseion_id, "你好")
    runs = AilyLarkClient().create_ailysession_run(tenant_access_token, seseion_id)

