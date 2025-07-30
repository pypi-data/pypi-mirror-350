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

class MyCardControl(mu.EntityXControl):

    class Meta:
        model_class = MyCard

    def update_card2(self,model,userId,accesstoken):
        def _do():
            im = IM()

            card = MyCard.select().where(MyCard.cardId == model.cardId,MyCard.userId == userId).first()
            if mu.isN(card):
                im.success = False
                im.msg = '名片不存在'
                return im

            card.name=model.name
            card.defaultCardModelId=model.defaultCardModelId
            card.save()

            im.msg = '恭喜！修改名片成功。'
            im.data = model_to_dict(card, False)

        return self.run(_do)