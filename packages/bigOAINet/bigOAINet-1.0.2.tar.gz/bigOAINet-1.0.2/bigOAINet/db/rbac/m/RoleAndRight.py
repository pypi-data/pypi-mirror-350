from peewee import IntegerField, BooleanField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class RoleAndRight(EntityX):
    roleAndRightId = AutoField()
    
    # 正向引用否
    isPositive = BooleanField(default=True)

    # 权限、角色
    right = ForeignKeyField(bigo.Right, backref='roleAndRightList', column_name='rightId', on_delete='CASCADE')
    role = ForeignKeyField(bigo.Role, backref='roleAndRightList', column_name='roleId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '角色与权限'
        