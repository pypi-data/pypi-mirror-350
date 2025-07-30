from peewee import Model, IntegerField, CharField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class DepartmentAndSubject(EntityX):
    class Meta:
        database = bigo.db
        name = '部门与对象'
        
    departmentAndSubjectId = AutoField()

    # 链接、链接类型
    linkId = IntegerField()
    linkType = CharField(max_length=200)

    # 部门
    department = ForeignKeyField(bigo.Department, backref='departmentAndSubjectList', column_name='departmentId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.linkType} - {self.department}"
