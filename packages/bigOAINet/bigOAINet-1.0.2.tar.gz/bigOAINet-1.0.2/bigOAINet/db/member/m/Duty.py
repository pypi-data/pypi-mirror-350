from peewee import IntegerField, CharField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class Duty(EntityX):
    class Meta:
        database = bigo.db
        name = '职务'
        
    dutyId = AutoField()
    
    # 名称、英文名称、描述、缩略图、排序
    name = CharField(max_length=200)
    enName = CharField(max_length=200, null=True)
    desc = CharField(null=True)
    thumb = CharField(max_length=200, null=True)
    sort = IntegerField()
