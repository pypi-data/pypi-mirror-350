import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
from .m.models import *
from mxupy import IM
import os

class MyVoiceControl(mu.EntityXControl):

    class Meta:
        model_class = MyVoice

    def del_voice_judge_associated(self,voiceId,userId,accesstoken):
        def _do():
            im = IM()
            # 查询是否存在 voiceId 这条数据
            im1 = self.get_one(where={'voiceId': voiceId,'userId': userId})
            if im1.success is False:
                return im1
                
            # 查询项目是否引用了这个语音
            project = MyProject.select().where(MyProject.userId == userId,MyProject.voiceId == voiceId).first()
            if project is not None:
                im.success = False
                im.msg = '已有项目选中了这段语音,无法删除'
                return im

            voice = im1.data

            # 删除自己
            im3 = self.delete_by_id(voiceId)
            if im3.success is False:
                return im3
                
            mu.removeFile(mu.file_dir('user',userId) + '\\'  + voice.immortalVoiceUrl)

        return self.run(_do)