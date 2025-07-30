import json
from peewee import *
import mxupy as mu
from playhouse.shortcuts import model_to_dict
from .m.models import *
from mxupy import IM
import os

class MyVoiceModelControl(mu.EntityXControl):

    class Meta:
        model_class = MyVoiceModel

    def del_voiceModel_judge_associated(self,voiceModelId,userId,accesstoken):
        def _do():
            im = IM()
            # 查询是否存在 voiceModelId 这条数据
            im1 = self.get_one(where={'voiceModelId': voiceModelId,'userId': userId})
            if im1.success is False:
                return im1
                
            # 查询项目是否引用了这个语音模型
            project = MyProject.select().where(MyProject.userId == userId,MyProject.voiceModelId == voiceModelId).first()
            if project is not None:
                im.success = False
                im.msg = '已有项目选中了这个语音模型,无法删除，如以修改请先保存项目'
                return im

            # 查询名片是否引用了这个语音模型
            card = MyCard.select().where(MyCard.userId == userId,MyCard.voiceModelId == voiceModelId).first()
            if card is not None:
                im.success = False
                im.msg = '已有名片选中了这个语音模型,无法删除，如以修改请先保存名片'
                return im

            voiceModel = im1.data

            # 删除自己
            im3 = self.delete_by_id(voiceModelId)
            if im3.success is False:
                return im3
            
            filePathList = [
                voiceModel.trainFile,
            ]
            if mu.isNN(voiceModel.previewFile):
                filePathList.append(voiceModel.previewFile)
            # 去重后删除全部关联文件
            filePathListSet = list(set(filePathList))
            mu.removeFileList(filePathListSet,mu.file_dir('user',userId) + '\\' )

            return im

        return self.run(_do)