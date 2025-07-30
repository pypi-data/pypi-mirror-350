from peewee import IntegerField, CharField, PrimaryKeyField, TextField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class ValueEx(EntityX):
    class Meta:
        database = bigo.db
        name = '值'
        
    valueExId = AutoField()
    
    # 链接ID、链接类型
    linkId = IntegerField()
    linkType = CharField(max_length=200)
    
    v1 = CharField(max_length=200)
    v2 = CharField(max_length=200)
    v3 = CharField(max_length=200)
    v4 = CharField(max_length=200)
    v5 = CharField(max_length=200)
    v6 = CharField(max_length=200)
    v7 = CharField(max_length=200)
    v8 = CharField(max_length=200)
    v9 = CharField(max_length=200)
    v10 = CharField(max_length=200)
    v11 = CharField(max_length=200)
    v12 = TextField()
    
    v12 = CharField(max_length=200)
    v13 = CharField(max_length=200)
    v14 = CharField(max_length=200)
    v15 = CharField(max_length=200)
    v16 = CharField(max_length=200)
    v17 = CharField(max_length=200)
    v18 = CharField(max_length=200)
    v19 = CharField(max_length=200)
    v20 = CharField(max_length=200)
    v21 = CharField(max_length=200)
    v22 = CharField(max_length=200)
    v23 = CharField(max_length=200)
    v24 = TextField()

