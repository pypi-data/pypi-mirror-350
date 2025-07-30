from peewee import IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class RoleExclusive(EntityX):
    """ 角色互斥

    Args:
        BaseModel (obj): 模型基类
    """
    roleExclusiveId = AutoField()
    
    role1 = ForeignKeyField(bigo.Role, backref='roleExclusiveList1', column_name='roleId1', on_delete='CASCADE')
    role2 = ForeignKeyField(bigo.Role, backref='roleExclusiveList2', column_name='roleId2', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '角色互斥'
        