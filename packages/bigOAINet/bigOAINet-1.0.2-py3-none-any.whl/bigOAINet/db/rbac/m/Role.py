from peewee import IntegerField, CharField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class Role(EntityX):
    
    # 名称、编码、编码路径、描述、排序
    name = CharField(max_length=200)
    code = CharField(max_length=200)
    codePath = CharField(max_length=200)
    desc = CharField(max_length=200, null=True)
    sort = IntegerField(default=0)
    
    roleCategory = ForeignKeyField(bigo.RoleCategory, backref='roleList', column_name='roleCategoryId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '角色'
        