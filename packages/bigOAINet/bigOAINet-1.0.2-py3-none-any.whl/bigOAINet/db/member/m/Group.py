from peewee import Model, IntegerField, CharField, BooleanField, ForeignKeyField, AutoField, TextField
from mxupy import EntityX
import bigOAINet as bigo

class Group(EntityX):
    class Meta:
        database = bigo.db
        name = '分组'
    groupId = AutoField()
    
    # 名称、英文名称、缩略图、描述、激活否
    name = CharField(max_length=200)
    enName = CharField(max_length=200, null=True)
    thumb = CharField(max_length=200, null=True)
    desc = TextField(null=True)
    isActive = BooleanField(default=True)

    # 企业
    enterprise = ForeignKeyField(bigo.Enterprise, backref='groupList',
                                 column_name='enterpriseId', on_delete='CASCADE', null=True)
