from peewee import IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class RoleInherit(EntityX):
    roleInheritId = AutoField()

    # 角色1、角色2
    role1 = ForeignKeyField(bigo.Role, backref='roleInheritList1', column_name='roleId1', on_delete='CASCADE')
    role2 = ForeignKeyField(bigo.Role, backref='roleInheritList2', column_name='roleId2', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '角色继承'