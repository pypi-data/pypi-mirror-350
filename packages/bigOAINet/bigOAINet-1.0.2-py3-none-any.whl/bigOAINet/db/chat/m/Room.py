from datetime import datetime
from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    TextField,
    IntegerField,
)
from mxupy import EntityX
import bigOAINet as bigo


class Room(EntityX):
    """聊天室（对应一个智能体）"""

    roomId = AutoField()

    # 名称、编码（用作房间路径）、缩略图、描述、创建时间
    name = CharField()
    # code = CharField()
    thumb = CharField(null=True)
    desc = TextField(null=True)
    sort = IntegerField(default=0)
    createTime = DateTimeField(default=datetime.now)

    createUser = ForeignKeyField(
        bigo.User, backref="rooms", column_name="createUserId", on_delete="CASCADE"
    )

    class Meta:
        database = bigo.db
        name = "房间"
