from peewee import Model, IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class GroupUser(EntityX):
    class Meta:
        database = bigo.db
        name = '用户分组'
    groupUserId = AutoField()

    # 分组、用户
    group = ForeignKeyField(bigo.Group, backref='groupUserList',
                            column_name='groupId', on_delete='CASCADE')
    # user = ForeignKeyField(User, backref='groupUserList', column_name='userId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.group} - {self.user}"
