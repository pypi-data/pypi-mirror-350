import requests
import json
from mxupy import read_config
import bigOAINet as bigo

# dify 调用
class AgentCaller:
    '''
        智能体调用
    '''
    def __init__(self, agentId, userId, sessionId):

        self.url = read_config().get('dify_api_url', {})
        self.agentId = agentId
        self.agent = bigo.AgentControl.inst().get_one_by_id(agentId).data
        self.userId = userId
        self.sessionId = sessionId
        # self.conversationId = conversationId
        self.headers = {
            'Authorization': f'Bearer { self.agent.apiKey }',
            'Content-Type': 'application/json'
        }

    def call(self, msg):
        """ 调用智能体

        Args:
            msg (_type_): 消息
                input: 输入
                query: 问题
                files: 文件
                userId: 用户id
        Returns:
            requests.models.Response: 
        """

        # file 数据结构
        # {
        #     'type': 'image',
        #     'transfer_method': 'remote_url',
        #     'url': 'https://cloud.dify.ai/logo/logo-site.png'
        # }
        
        payload = json.dumps({
            'inputs': msg.get('input', {}),
            'query': msg.get('query', ''),
            'response_mode': 'streaming',
            'conversation_id': msg.get('conversationId', ''),
            'user': str(self.userId),
            'files': msg.get('files', [])
        })
        response = requests.request('POST', self.url + 'chat-messages', headers=self.headers, data=payload)

        return response

    def upload(self):
        # url = self.url + "/files/upload"

        # payload = {}
        # files = [('file', ('file', open('/path/to/file', 'rb'), 'application/octet-stream'))]
        # headers = {
        #     'Authorization': 'Bearer {self.agent.apiKey}'
        # }

        # response = requests.request("POST", url, headers=headers, data=payload, files=files)

        # # print(response.text)
        # return response
        pass
