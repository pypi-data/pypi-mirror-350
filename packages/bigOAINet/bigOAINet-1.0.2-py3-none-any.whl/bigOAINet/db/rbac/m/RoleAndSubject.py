from peewee import IntegerField, CharField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class RoleAndSubject(EntityX):
    roleAndSubjectId = AutoField()
    
    # 外链id，外链类型（一般为用户、用户分组、部门等）
    linkId = IntegerField()
    linkType = CharField(max_length=200)

    role = ForeignKeyField(bigo.Role, backref='roleAndSubjectList', column_name='roleId', on_delete='CASCADE')

    @property
    def user(self):
        if self.linkType == "User" and self.linkId > 0:
            return bigo.User.get_by_id(self.linkId)
        return None

    @property
    def group(self):
        if self.linkType == "Group" and self.linkId > 0:
            return bigo.Group.get_by_id(self.linkId)
        return None

    @property
    def department(self):
        if self.linkType == "Department" and self.linkId > 0:
            return bigo.Department.get_by_id(self.linkId)
        return None

    class Meta:
        database = bigo.db
        name = '角色对象'
        