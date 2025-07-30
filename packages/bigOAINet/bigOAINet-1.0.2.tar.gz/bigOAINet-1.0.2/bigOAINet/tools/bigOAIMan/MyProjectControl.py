import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
from .m.models import *
import os
import json
from mxupy import IM

class MyProjectControl(mu.EntityXControl):

    class Meta:
        model_class = MyProject

    def add_project2(self,model,userId,accesstoken):
        def _do():
            im = IM()

            # 创建新数字人模型
            newProject = MyProject.create(
                userId=userId,
                name=model.name,
                thumb=model.thumb,
                modelId=model.modelId,
                width=model.width,
                height=model.height,
                # scriptId=model.scriptId,
                scriptId=None if model.scriptId == -1 else model.scriptId,
                # voiceModelId=model.voiceModelId,
                voiceModelId=None if model.voiceModelId == -1 else model.voiceModelId,
                # voiceId=model.voiceId,
                voiceId=None if model.voiceId == -1 else model.voiceId,
                voiceSpeed=model.voiceSpeed,
                voiceUrl=model.voiceUrl,
                renderUrl=model.renderUrl,
                renderStatus=model.renderStatus,
                useVoice=model.useVoice,
            )

            im.msg = '恭喜！保存项目成功。'
            im.data = model_to_dict(newProject, False)

            return im

        return self.run(_do)

    def update_project2(self,model,userId,accesstoken):
        def _do():
            im = IM()

            project = MyProject.select().where(MyProject.projectId == model.projectId,MyProject.userId == userId).first()
            if mu.isN(project):
                im.success = False
                im.msg = '项目不存在'
                return im

            project.name=model.name
            project.thumb=model.thumb
            project.modelId=model.modelId
            project.width=model.width
            project.height=model.height
            project.scriptId=None if model.scriptId == -1 else model.scriptId
            project.voiceModelId=None if model.voiceModelId == -1 else model.voiceModelId
            project.voiceId=None if model.voiceId == -1 else model.voiceId
            project.voiceSpeed=model.voiceSpeed
            project.voiceUrl=model.voiceUrl
            project.renderUrl=model.renderUrl
            project.renderStatus=model.renderStatus
            project.useVoice=model.useVoice
            project.save()

            im.msg = '恭喜！修改项目成功。'
            im.data = model_to_dict(project, False)

            return im

        return self.run(_do)

    def del_project_judge_associated(self,projectId,userId,accesstoken):
        def _do():
            # 查询是否存在 projectId 这条数据
            im1 = self.get_one(where={'projectId': projectId,'userId': userId})
            if im1.success is False:
                return im1
                
            project = im1.data
            # 删除自己
            im3 = self.delete_by_id(projectId)
            if im3.success is False:
                return im3

            if mu.isNN(project.voiceUrl):
                mu.removeFile(mu.file_dir('user',userId) + '\\'  + project.voiceUrl)
            if mu.isNN(project.renderUrl):
                mu.removeFile(mu.file_dir('user',userId) + '\\'  + project.renderUrl)

        return self.run(_do)