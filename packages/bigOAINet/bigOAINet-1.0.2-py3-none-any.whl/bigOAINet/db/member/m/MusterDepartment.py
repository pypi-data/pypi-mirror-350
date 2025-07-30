from peewee import Model, IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class MusterDepartment(EntityX):
    class Meta:
        database = bigo.db
        name = '主部门'
        
    musterDepartmentId = AutoField()

    # 部门、主部门
    department = ForeignKeyField(bigo.Department, backref='musterDepartmentList', column_name='departmentId', on_delete='CASCADE')
    muster = ForeignKeyField(bigo.Muster, backref='musterDepartmentList', column_name='musterId', on_delete='CASCADE')
