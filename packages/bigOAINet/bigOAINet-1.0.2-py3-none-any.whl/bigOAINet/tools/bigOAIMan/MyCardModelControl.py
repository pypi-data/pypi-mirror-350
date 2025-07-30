import uuid as uid
from peewee import *
import base64
import json
import os
import mxupy as mu
from mxupy import IM
from playhouse.shortcuts import model_to_dict
from .m.models import *
import random

class MyCardModelControl(mu.EntityXControl):

    class Meta:
        model_class = MyCardModel

    def update_cardModel2(self,model,userId,accesstoken):
        def _do():
            im = IM()

            cardModel = MyCardModel.select().where(MyCardModel.cardModelId == model.cardModelId,MyCardModel.cardId == model.cardId,MyCardModel.userId == userId).first()
            if mu.isN(cardModel):
                im.success = False
                im.msg = '名片模型不存在'
                return im

            cardModel.modelId=model.modelId
            cardModel.voiceModelId=model.voiceModelId
            cardModel.voiceSpeed=model.voiceSpeed
            cardModel.name=model.name
            cardModel.save()

            im.msg = '恭喜！修改名片模型成功。'
            im.data = model_to_dict(cardModel, False)

        return self.run(_do)