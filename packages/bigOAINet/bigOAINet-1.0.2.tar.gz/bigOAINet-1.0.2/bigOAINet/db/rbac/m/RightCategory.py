from peewee import IntegerField, CharField, AutoField
from mxupy import TreeEntityX
import bigOAINet as bigo

class RightCategory(TreeEntityX):
    
    rightCategoryId = AutoField()
    
    # 名称、名称路径、编码、编码路径
    name = CharField(max_length=200)
    namePath = CharField(max_length=200, null=True)
    code = CharField(max_length=200)
    codePath = CharField(max_length=200, null=True)
    
    @property
    def roleRightList(self):
        return self._roleRightList
    @roleRightList.setter
    def roleRightList(self, value):
        self._roleRightList = value
    
    class Meta:
        model_name = '权限分类'
        database = bigo.db
    

# from ...db.Database import db
# RightCategory._meta.database = bigo.db
