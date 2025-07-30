from datetime import datetime
from peewee import Model, IntegerField, CharField, AutoField, DateTimeField, ForeignKeyField
from mxupy import EntityX
import bigOAINet as bigo


class FriendGroup(EntityX):
    class Meta:
        database = bigo.db
        name = '朋友分组'
    friendGroupId = AutoField()  # 好友分组的唯一标识符，自动增长

    # 名称、好友数量、创建时间
    name = CharField(max_length=200, null=False)
    friends = IntegerField(default=0)
    addTime = DateTimeField(default=datetime.now)

    # 用户
    # user = ForeignKeyField(User, backref='friendGroupList', column_name='userId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.name} - {self.user}"
