import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
import bigOAINet as bigo
from mxupy import IM

class MyDHVoiceControl(mu.EntityXControl):

    class Meta:
        model_class = bigo.MyDHVoice
        
    def __init__(self, *args, **kwargs):
        self.sub_dir = 'digitalHuman/voice/'
        super().__init__(*args, **kwargs)

    def delete1(self, id, userId, accessToken):
        """
            删除

        Args:
            self: 当前对象的引用。
            id (int): 要删除的资源的唯一标识符。
            userId (int): 请求删除操作的用户的唯一标识符。
            accessToken (str): 用于身份验证的访问令牌。

        Returns:
            IM：结果
        """
        def _do():
            im = IM()
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            cs = [{'myDHVoiceId': id}, {'userId': userId}]
            
            # 查询是否存在 voiceId 这条数据
            im = self.get_one(where=cs)
            if im.error:
                return im
            voice = im.data
            
            # 查询项目是否引用了这个语音模型
            im = bigo.MyDHVideoControl.inst().exists(where=cs)
            if im.error:
                return im
            if im.data:
                return IM(False, '删除失败。已有视频选中了此语音。')

            # 删除
            im = self.delete_by_id(id)
            if im.error:
                return im
            
            return im
            
            # # 删除文件
            # mu.removeFile(mu.file_dir('user',userId) + '\\'  + voice.url)

        return self.run(_do)