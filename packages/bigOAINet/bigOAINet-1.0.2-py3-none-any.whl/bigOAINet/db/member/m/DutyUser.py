from peewee import IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class DutyUser(EntityX):
    class Meta:
        database = bigo.db
        name = '职务用户'
    dutyUserId = AutoField()
    
    # 职务排序
    dutySort = IntegerField(default=0)
    
    # 用户、职务、部门
    # user = ForeignKeyField(User, column_name='userId', backref='dutyUserList', on_delete='CASCADE')
    duty = ForeignKeyField(bigo.Duty, column_name='dutyId', backref='dutyUserList', on_delete='CASCADE')
    department = ForeignKeyField(bigo.Department, column_name='departmentId', backref='dutyUserList', on_delete='CASCADE')
