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

class MyCatechismControl(mu.EntityXControl):

    class Meta:
        model_class = MyCatechism


    def del_catechism_judge_associated(self,catechismId,userId,accesstoken):
        def _do():
            # 查询是否存在 catechismId 这条数据
            im1 = self.get_one(where={'catechismId': catechismId,'userId': userId})
            if im1.success is False:
                return im1
                
            catechism = im1.data

            # 收集所有的文件路径
            filePathList = []
            
            if mu.isNN(catechism.videoFile):
                filePathList.append(catechism.videoFile)

            filePath = mu.file_dir('user',userId) + '\\'

            filepath, shotname, extension = mu.fileParts(catechism.videoFile)
            dataPath = mu.file_dir('user',userId)
            filePathList.append(shotname + '.m3u8')
            for root, dirs, files in os.walk(filePath):
                for file in files:
                    if file.endswith(".ts") and file.startswith(shotname):
                        filePathList.append(file)

            attachmentList = list(catechism.attachmentList)

            for attachment in attachmentList:
                filePathList.append(attachment.attachmentUrl)

            # 删除自己
            im3 = self.delete_by_id(catechismId)
            if im3.success is False:
                return im3
            
            # 去重后删除全部关联文件
            filePathListSet = list(set(filePathList))
            mu.removeFileList(filePathListSet,filePath)

        return self.run(_do)
    
    def update_catechism2(self,model,userId,accesstoken):
        def _do():
            im = IM()

            catechism = MyCatechism.select().where(MyCatechism.catechismId == model.catechismId,MyCatechism.userId == userId).first()
            if mu.isN(catechism):
                im.success = False
                im.msg = '问答不存在'
                return im

            catechism.question=model.question
            catechism.answer=model.answer
            catechism.renderStatus=model.renderStatus
            # 删除老的生成视频
            if mu.isNN(catechism.videoFile) and catechism.videoFile != model.videoFile:
                mu.removeFile(mu.file_dir('user',userId) + '\\'  + catechism.videoFile)
            catechism.videoFile=model.videoFile
            catechism.save()

            im.msg = '恭喜！修改问答成功。'
            im.data = model_to_dict(catechism, False)

        return self.run(_do)