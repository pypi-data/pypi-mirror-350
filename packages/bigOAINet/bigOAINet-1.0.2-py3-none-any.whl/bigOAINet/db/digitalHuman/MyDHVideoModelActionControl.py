import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
import bigOAINet as bigo
from mxupy import IM

import os,json

class MyDHVideoModelActionControl(mu.EntityXControl):
    class Meta:
        model_class = bigo.MyDHVideoModelAction
        
    def __init__(self, *args, **kwargs):
        self.sub_dir = 'digitalHuman/videoModelAction/'
        super().__init__(*args, **kwargs)

    
    def add1(self, model, userId, accessToken):
        """
            添加

        Args:
            model (MyDHVideoModel): 视频模型
            userId (int): 用户id
            accessToken (str): 访问令牌
        Returns:
            IM：结果
        """
        def _do():
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            im = self.add(model)
            if im.error:
                return im
                       
            return im

        return self.run(_do)

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

            # 删除
            im = self.delete_by_id(id, recursive=True)
            if im.error:
                return im

        return self.run(_do)

