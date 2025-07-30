from peewee import IntegerField, ForeignKeyField, BooleanField, CharField, TextField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class DepartmentUser(EntityX):
    class Meta:
        database = bigo.db
        name = '部门用户'
        
    departmentUserId = AutoField()
    
    # 主部门、用户排序
    isMaster = BooleanField()
    userSort = IntegerField()
    
    # 部门、用户
    department = ForeignKeyField(bigo.Department, backref='departmentUserList', column_name='departmentId', on_delete='CASCADE')
    # user = ForeignKeyField(User, backref='departmentUserList', column_name='userId', on_delete='CASCADE')

    @property
    def duty_list(self):
        # 这里需要根据你的具体实现来获取职务列表
        # 以下代码是一个示例，你需要根据实际情况调整
        # query = (BeCoolMemberDutyUser
        #          .select()
        #          .join(BeCoolMemberDuty, on=(BeCoolMemberDutyUser.dutyId == BeCoolMemberDuty.dutyId))
        #          .where(BeCoolMemberDutyUser.userId == self.userId, BeCoolMemberDutyUser.departmentId == self.departmentId)
        #          .order_by(BeCoolMemberDuty.dutySort.desc()))
        # duties = query.execute()
        # return [model_to_dict(duty) for duty in duties]
        print(self)

