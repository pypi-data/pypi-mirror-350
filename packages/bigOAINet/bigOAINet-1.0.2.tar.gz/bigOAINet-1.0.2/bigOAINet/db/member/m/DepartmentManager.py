from peewee import Model, IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class DepartmentManager(EntityX):
    class Meta:
        database = bigo.db
        name = '部门管理者'
        
    departmentManagerId = AutoField()

    # 用户排行
    userSort = IntegerField(default=0)

    # 部门、管理员
    department = ForeignKeyField(bigo.Department, backref='departmentManagerList', column_name='departmentId', on_delete='CASCADE')
    manager = ForeignKeyField(bigo.User, backref='departmentManagerList', column_name='managerId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.department} - {self.manager}"
