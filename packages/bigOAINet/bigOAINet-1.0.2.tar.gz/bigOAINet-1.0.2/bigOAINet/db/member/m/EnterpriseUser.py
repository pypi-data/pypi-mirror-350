from peewee import Model, IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class EnterpriseUser(EntityX):
    class Meta:
        database = bigo.db
        name = '企业用户'
    enterpriseUserId = AutoField()
    
    # 用户、企业
    # user = ForeignKeyField(User, backref='enterpriseUserList', column_name='userId', on_delete='CASCADE')
    enterprise = ForeignKeyField(bigo.Enterprise, backref='enterpriseUserList', column_name='enterpriseId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.enterprise} - {self.user}"
