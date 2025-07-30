import uuid as uid
from peewee import *
import base64
import json
import os
import mxupy as mu
from mxupy import IM
from playhouse.shortcuts import model_to_dict
import bigOAINet as bigo

class MyDHCardControl(mu.EntityXControl):

    class Meta:
        model_class = bigo.MyDHCard

    def update1(self, model, userId, accessToken):
        """ 
        更新用户名片信息

        Args:
            model (object): 名片
            userId (str): 用户id
            accessToken (str): 访问令牌
        Returns:
            IM: 结果
        """
        def _do():
            
            im = IM()
            
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            im = self.get_one(where=[{ 'myDHCardId': model.myDHCardId, 'userId': userId }])
            if im.error:
                return im
            if im.data is None:
                return im.set_error('名片不存在')
            
            im = self.update_by_id(model.myDHCardId, model)
            if im.error:
                return im
            
            return im
            
            # im = self.update(model, where={'myDHCardId': model.myDHCardId, 'userId': userId })
            
            # # ？？？
            # im = bigo.MyDHCardModelControl.inst().update(where={'myDHCardModelId': model.defaultCardModelId })
            

            # card = bigo.MyDHCard.select().where(bigo.MyDHCard.cardId == model.cardId,bigo.MyDHCard.userId == userId).first()
            # if mu.isN(card):
            #     im.success = False
            #     im.msg = '名片不存在'
            #     return im

            # card.name=model.name
            # card.defaultCardModelId=model.defaultCardModelId
            # card.save()

            # im.msg = '恭喜！修改名片成功。'
            # im.data = model_to_dict(card, False)

        return self.run(_do)