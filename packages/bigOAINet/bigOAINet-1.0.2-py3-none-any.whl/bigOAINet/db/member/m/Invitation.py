from datetime import datetime
from peewee import Model, IntegerField, CharField, AutoField, DateTimeField, ForeignKeyField
from mxupy import EntityX
import bigOAINet as bigo


class Invitation(EntityX):
    class Meta:
        database = bigo.db
        name = '邀请'
    invitationId = AutoField()

    # 邀请关系，例如朋友、家人等
    relation = CharField(max_length=200, null=False)
    # 邀请状态，例如已发送、已接受等
    status = CharField(max_length=200, null=False)
    # 添加时间，默认为当前时间
    addTime = DateTimeField(default=datetime.now)
    # 邀请备注
    note = CharField(max_length=200, null=True)
    
    # 发送邀请的用户
    # fromUser = ForeignKeyField(User, backref='invitationList', column_name='fromUserId', on_delete='CASCADE')
    # 接收邀请的用户
    # toUser = ForeignKeyField(User, backref='invitationList', column_name='toUserId', on_delete='CASCADE')

    def __str__(self):
        return f"Invitation from {self.fromUser} to {self.toUser} - Relation: {self.relation}, Status: {self.status}"

