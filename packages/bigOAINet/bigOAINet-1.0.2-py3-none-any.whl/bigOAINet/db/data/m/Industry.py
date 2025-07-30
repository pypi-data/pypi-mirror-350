from peewee import Model, IntegerField, CharField, BooleanField, AutoField, TextField,ForeignKeyField
from mxupy import TreeEntityX
import bigOAINet as bigo

class Industry(TreeEntityX):
    class Meta:
        database = bigo.db
        name = '行业'
        
    industryId = AutoField()
    
    # 父亲
    parent = ForeignKeyField('self', column_name='parentId',backref='children', on_delete='CASCADE', default=None, null=True)
    
    # 名称、缩略图、描述
    name = CharField(max_length=200)
    thumb = CharField(max_length=200)
    desc = TextField()
