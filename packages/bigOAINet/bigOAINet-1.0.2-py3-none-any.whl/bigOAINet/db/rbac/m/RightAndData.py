from peewee import IntegerField, CharField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class RightAndData(EntityX):
    rightAndDataId = AutoField()
    
    # k:key v:value
    k1 = CharField(max_length=200)
    k2 = CharField(max_length=200)
    k3 = CharField(max_length=200)
    k4 = CharField(max_length=200)
    k5 = CharField(max_length=200)
    k6 = CharField(max_length=200)
    
    v1 = CharField(max_length=200)
    v2 = CharField(max_length=200)
    v3 = CharField(max_length=200)
    v4 = CharField(max_length=200)
    v5 = CharField(max_length=200)
    v6 = CharField(max_length=200)

    right = ForeignKeyField(bigo.Right, backref='rightAndDataList', column_name='rightId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '权限数据'