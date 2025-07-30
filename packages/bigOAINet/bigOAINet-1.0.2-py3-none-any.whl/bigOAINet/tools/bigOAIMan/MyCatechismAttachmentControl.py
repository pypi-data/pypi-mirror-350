import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
from .m.models import *
import os

class MyCatechismAttachmentControl(mu.EntityXControl):

    class Meta:
        model_class = MyCatechismAttachment

    def del_catechismAttachment_and_file(self,catechismId,catechismAttachmentId,userId,accesstoken):
        def _do():
            # 查询是否存在 catechismId 这条数据
            im1 = self.get_one(where={'catechismAttachmentId': catechismAttachmentId,'catechismId': catechismId})
            if im1.success is False:
                return im1
                
            catechismAttachment = im1.data

            # 删除自己
            im3 = self.delete_by_id(catechismAttachmentId)
            if im3.success is False:
                return im3
            
            if mu.isNN(catechismAttachment.attachmentUrl):
                mu.removeFile(mu.file_dir('user',userId) + '\\' + catechismAttachment.attachmentUrl)

        return self.run(_do)