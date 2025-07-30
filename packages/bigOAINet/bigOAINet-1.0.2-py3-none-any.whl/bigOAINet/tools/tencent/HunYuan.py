import os
import json

# 安装腾讯云
# pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python

class HunYuan:
    """
        空间: bigOAINET.tencent.HunYuan
        名称：腾讯混元大模型
        参考网址：https://cloud.tencent.com/document/product/1729/105701
        开通界面：https://console.cloud.tencent.com/cam/capi
        语音收费：https://cloud.tencent.com/document/product/1449/56977
        提供普通问答、流式问答、两者的异步问答、http事件请求等功能
        辅助功能：提供历史记录超出最大请求额度则按比例裁剪的功能

    """
    def __init__(self, history_tokens=0, history_percent=0.6, min_history_length=5, record_error_log=False, write_error_to_file=False, client_id=''):
        """ 初始化

        Args:
            history_tokens (int): 历史记录最大token数。小于等于0时, 则不传历史消息。
            history_percent (float): 当超过历史记录最大token数时, 则保留最新的历史百分比(为了消息的完整性, 这里指的是消息条数)。
            min_history_length (int): 历史保留最小条数
            record_error_log (bool): 是否记录错误日志
            write_error_to_file (bool): 是否把错误日志记录到文档
            clientId (str): 对话id, 一个用户一次与ai的完整对话可以看成 client, 
                根据 clientId 可自动保存其历史消息, 用于本次的对话, 辅助ai更好的理解用户对话的含义
        Returns:
            无
        """
        # setx Tencent_HunYuan_Secret_Id 你的 secret_id 设置后需要重启
        # self.secret_id = os.getenv('Tencent_HunYuan_Secret_Id')
        # self.secret_key = os.getenv('Tencent_HunYuan_Secret_Key')
        
        self.secret_id = 'AKIDntTPSf2JBFiT72Gqdh19XA8G58OrYXwh'
        self.secret_key = 'Flx7BTdgd5Sjw4991sgR4bzHUfjrtsnv'
        
        self.endpoint = "hunyuan.tencentcloudapi.com"
        
        self.histories = []
        self.history_tokens = history_tokens
        self.history_percent = history_percent
        self.min_history_length = min_history_length
        
        self.record_error_log = record_error_log
        self.write_error_to_file = write_error_to_file
        self.error_logs = []
        
        self.client_id = client_id
        
    def call(self, messages, model='hunyuan-lite', topP=None, temperature=None, enableEnhancement=True, 
                   tools=None, toolChoice='auto', customTool=None, 
                   searchInfo=False, citation=False, enableSpeedSearch=False, enableMultimedia=False):  
        """ 调用

        Args:
            messages (list[obj]): 聊天上下文信息。
                1. 长度最多为 40，按对话时间从旧到新在数组中排列。
                2. Message.Role 可选值：system、user、assistant、 tool。
                    其中，system 角色可选，如存在则必须位于列表的最开始。
                    user（tool） 和 assistant 需交替出现（一问一答），
                    以 user 提问开始，user（tool）提问结束，且 Content 不能为空。
                    Role 的顺序示例：[system（可选） user assistant user assistant user …]。
                3. Messages 中 Content 总长度不能超过模型输入长度上限（可参考 产品概述 文档），超过则会截断最前面的内容，只保留尾部内容。
            model (str): 
                可选模型有：hunyuan-lite、hunyuan-standard、hunyuan-standard-256K、hunyuan-pro、 hunyuan-code、 
                hunyuan-role、 hunyuan-functioncall、 hunyuan-vision、 hunyuan-turbo。
            topP (float): 
                1. 影响输出文本的多样性。模型已有默认参数，不传值时使用各模型推荐值，不推荐用户修改。
                2. 取值区间为 [0.0, 1.0]。取值越大，生成文本的多样性越强。
            temperature (float): 
                1. 影响模型输出多样性，模型已有默认参数，不传值时使用各模型推荐值，不推荐用户修改。
                2. 取值区间为 [0.0, 2.0]。较高的数值会使输出更加多样化和不可预测，而较低的数值会使其更加集中和确定。
            enableEnhancement (bool): 功能增强（如搜索）开关。
                1. hunyuan-lite 无功能增强（如搜索）能力，该参数对 hunyuan-lite 版本不生效。
                2. 未传值时默认打开开关。
                3. 关闭时将直接由主模型生成回复内容，可以降低响应时延（对于流式输出时的首字时延尤为明显）。但在少数场景里，回复效果可能会下降。
                4. 安全审核能力不属于功能增强范围，不受此字段影响。
                
            tools ( ): 可调用的工具列表，仅对 hunyuan-pro、hunyuan-turbo、hunyuan-functioncall 模型生效。
            toolChoice (str): 工具使用选项，可选值包括 none、auto、custom。
                1. 仅对 hunyuan-pro、hunyuan-turbo、hunyuan-functioncall 模型生效。
                2. none：不调用工具；auto：模型自行选择生成回复或调用工具；custom：强制模型调用指定的工具。
                3. 未设置时，默认值为auto
            customTool (bool): 强制模型调用指定的工具，当参数ToolChoice为custom时，此参数为必填
            
            searchInfo (bool): 在值为 true 且命中搜索时，接口会返回 SearchInfo
            citation (bool): 搜索引文角标开关。
                1. 配合EnableEnhancement和SearchInfo参数使用。打开后，回答中命中搜索的结果会在片段后增加角标标志，对应SearchInfo列表中的链接。
                2. false：开关关闭，true：开关打开。
                3. 未传值时默认开关关闭（false）。
            enableSpeedSearch (bool): 是否开启极速版搜索，默认false，不开启；在开启且命中搜索时，会启用极速版搜索，流式输出首字返回更快。
            enableMultimedia (bool): 图文并茂开关。详细介绍请阅读 图文并茂 中的说明。
                1. 该参数仅在功能增强（如搜索）开关开启（EnableEnhancement=true）时生效。
                2. hunyuan-lite 无图文并茂能力，该参数对 hunyuan-lite 版本不生效。
                3. 未传值时默认关闭。
                4. 开启并搜索到对应的多媒体信息时，会输出对应的多媒体地址，可以定制个性化的图文消息。

        Returns:
            _type_: _description_
        """
        
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
        from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
        
        try:
            cred = credential.Credential(self.secret_id, self.secret_key)
            
            httpProfile = HttpProfile()
            httpProfile.endpoint = self.endpoint
            
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            
            client = hunyuan_client.HunyuanClient(cred, '', clientProfile)

            # 实例化一个请求对象, 每个接口都会对应一个 request 对象
            req = models.ChatCompletionsRequest()
            params = {
                'Model': model,
                'Messages': messages,
                'EnableEnhancement': enableEnhancement,
                'ToolChoice': toolChoice,
                
                'SsearchInfo': searchInfo,
                'Citation': citation,
                'EnableSpeedSearch': enableSpeedSearch,
                'EnableMultimedia': enableMultimedia,
            }
            if topP != None:
                params.TopP = topP
            if temperature != None:
                params.Temperature = temperature
            if tools != None:
                params.Tools = tools
            if customTool != None:
                params.CustomTool = customTool
            
            req.from_json_string(json.dumps(params))

            # 返回的resp是一个ChatCompletionsResponse的实例，与请求对象对应
            resp = client.ChatCompletions(req)

            if (resp.ErrorMsg):
                return json.dumps({
                    'msg': f"{resp.ErrorMsg.Code}, {resp.ErrorMsg.Msg}",
                    'success': False,
                })
            else:
                # 去除英文双引号，且不超过50个字
                return json.dumps({
                    'msg': f"{resp.Choices[0].Message.Content}".replace('"', '')[:50],
                    'success': True,
                })

        except TencentCloudSDKException as err:
            return json.dumps({
                'msg': f"{err}",
                'success': False,
            })

async def text_polishing(userId: int, nickname: str, text: str):

    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
    
    try:
        cred = credential.Credential(
            "AKIDZBpV4ZbaPJ82shdTI9wgJoCQWaefwRd6", "X0RkDg7SgsHiQC2mRvEMI2fCsTtCd5b2")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = hunyuan_client.HunyuanClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.ChatCompletionsRequest()
        params = {
            "Model": "hunyuan-lite",
            "TopP": 0.6,
            "Temperature": 1.8,
            "Messages": [{
                "Role": "system",
                "Content": f"你是一个主播，你的直播间来了一个网民，TA的昵称是： {nickname}"
            }, {
                "Role": "user",
                "Content": f"将如下文字润色并直接返回结果(不要去掉或改写网民的昵称，简明扼要，不超过40个字，不能一字不改)：{text}"
            }]
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个ChatCompletionsResponse的实例，与请求对象对应
        resp = client.ChatCompletions(req)

        if (resp.ErrorMsg):
            return json.dumps({
                'msg': f"{resp.ErrorMsg.Code}, {resp.ErrorMsg.Msg}",
                'success': False,
            })
        else:
            # 去除英文双引号，且不超过50个字
            return json.dumps({
                'msg': f"{resp.Choices[0].Message.Content}".replace('"', '')[:50],
                'success': True,
            })

    except TencentCloudSDKException as err:
        return json.dumps({
            'msg': f"{err}",
            'success': False,
        })
        
        
if __name__ == '__main__':
    hy = HunYuan()
    messages = [
        {
            "Role": "user",
            "Content": '几点了？',
        }
    ]
    hy.call(messages)