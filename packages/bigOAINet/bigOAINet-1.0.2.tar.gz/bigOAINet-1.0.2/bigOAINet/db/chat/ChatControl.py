from mxupy import EntityXControl
import bigOAINet as bigo

class ChatControl(EntityXControl):
    class Meta:
        model_class = bigo.Chat
    
    def add(self, sessionId, userId, content, type='text', conversationId=''):
        """ 
            添加聊天记录

            Args:
                sessionId (str): 会话的唯一标识符，用于标识当前聊天所属的会话。
                userId (str): 用户的唯一标识符，用于标识发送消息的用户。
                content (str): 聊天内容，即用户或系统在聊天中发送的具体文本或其他类型的内容。
                type (str, optional): 聊天内容的类型，默认为 'text'，表示文本内容。其他类型包括：
                    - 'html': HTML 格式的内容
                    - 'markdown': MarkDown 格式的内容
                    - 'table': 表格形式的内容
                    - 'code': 代码形式的内容
                    - 'form': 表单形式的内容
                    - 'chart': 报表形式的内容
                    - 'image': 图片内容
                    - 'audio': 语音内容
                    - 'video': 视频内容
                    - 'download': 下载内容
                    - 'file': 文件内容
                conversationId (str, optional): dify 会话的唯一标识符，用于标识当前聊天所属的会话。
            Returns:
                IM: 添加结果，通常是一个包含添加操作结果的对象，可能包含成功或失败的状态、错误信息（如果有）、以及添加的聊天记录的唯一标识符或其他相关数据。
        """
        sup = super()
        def _do():
            
            # 获取会话
            im = bigo.SessionControl.inst().get_one(select='roomId', where={'sessionId':sessionId})
            if im.error:
                return im
            if im.data is None:
                return im.set_error('会话不存在')
            session = im.data
            
            # 添加聊天记录
            roomId = im.data.roomId
            rim = sup.add(bigo.Chat(roomId=roomId, content=content, type=type, userId=userId, session=session))
            if rim.error:
                return rim
            chat = rim.data
            
            # 更新会话的 conversationId
            if conversationId != '':
                session.conversationId = conversationId
                im = bigo.SessionControl.inst().update(model=session, where={'sessionId':sessionId}, fields='conversationId')
                if im.error:
                    return im
            
            # 按道理是要更新会话的 lastChatId 的，但是这个字段在to_dict方法会被干掉，所以这里就用 lastChat 替代
            # 更新会话的 lastChatId
            session.lastChat = chat
            im = bigo.SessionControl.inst().update(model=session, where={'sessionId':sessionId}, fields=['lastChat'])
            if im.error:
                return im
            
            return im
        
        return self.run(_do)
    