from peewee import IntegerField, CharField, TextField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class DepartmentType(EntityX):
    class Meta:
        database = bigo.db
        name = '部门类型'
        
    departmentTypeId = AutoField()
    
    # 名称、英文名称、排序、描述、缩略图
    name = CharField(max_length=200)
    enName = CharField(max_length=200)
    sort = IntegerField(default=0)
    desc = TextField(null=True)
    thumb = CharField(max_length=200, null=True)
