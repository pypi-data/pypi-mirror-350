from datetime import datetime
from peewee import Model, IntegerField, CharField, AutoField, DateTimeField, ForeignKeyField
from mxupy import EntityX
import bigOAINet as bigo


class Friend(EntityX):
    class Meta:
        database = bigo.db
        name = '朋友'
    friendId = AutoField()  # 好友关系的唯一标识符，自动增长

    # 好友关系描述
    relation = CharField(max_length=200, null=False)
    # 好友关系建立的时间，默认为当前时间
    addTime = DateTimeField(default=datetime.now)

    # 好友分组
    friendGroup = ForeignKeyField(bigo.FriendGroup, backref='friendList', column_name='friendGroupId', on_delete='CASCADE')
    # 发起好友请求的用户
    # fromUser = ForeignKeyField(User, backref='friendList', column_name='fromUserId', on_delete='CASCADE')
    # 接收好友请求的用户
    # toUser = ForeignKeyField(User, backref='friendList', column_name='toUserId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.fromUser} - {self.toUser} in group {self.friendGroup}"
