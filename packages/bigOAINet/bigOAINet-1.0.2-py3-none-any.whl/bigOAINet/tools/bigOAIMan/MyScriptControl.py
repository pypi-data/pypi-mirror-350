import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
from .m.models import *
from mxupy import IM


class MyScriptControl(mu.EntityXControl):

    class Meta:
        model_class = MyScript
    
    def del_script_judge_associated(self,scriptId,userId,accesstoken):
        def _do():
            im = IM()
            # 查询是否存在 scriptId 这条数据
            im1 = self.get_one(where={'scriptId': scriptId,'userId': userId})
            if im1.success is False:
                return im1
                
            # 查询项目是否引用了这个脚本
            project = MyProject.select().where(MyProject.userId == userId,MyProject.scriptId == scriptId).first()
            if project is not None:
                im.success = False
                im.msg = '已有项目选中了这个脚本,无法删除'
                return im

            # 删除自己
            im3 = self.delete_by_id(scriptId)
            if im3.success is False:
                return im3

        return self.run(_do)