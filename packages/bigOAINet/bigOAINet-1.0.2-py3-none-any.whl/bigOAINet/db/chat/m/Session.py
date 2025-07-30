from datetime import datetime
from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, DeferredForeignKey
from mxupy import EntityX
import bigOAINet as bigo


class Session(EntityX):
    """ 会话
    """
    sessionId = AutoField()

    # 主题、logo、创建时间
    title = CharField()
    logo = CharField()
    createTime = DateTimeField(default=datetime.now)

    # 对应dify的会话id，是一个guid
    conversationId = CharField(null=True)

    # 聊天室、创建者
    room = ForeignKeyField(bigo.Room, backref='sessions', column_name='roomId', on_delete='CASCADE')
    createUser = ForeignKeyField(bigo.User, backref='sessions', column_name='createUserId', on_delete='CASCADE')

    # 最后一条消息
    lastChat = DeferredForeignKey('Chat', backref='sessions', column_name='lastChatId', on_delete='CASCADE', null=True)

    class Meta:
        database = bigo.db
        name = '会话'
