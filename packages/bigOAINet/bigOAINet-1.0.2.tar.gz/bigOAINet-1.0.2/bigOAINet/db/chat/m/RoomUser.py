from datetime import datetime
from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, TextField, IntegerField
from mxupy import EntityX
import bigOAINet as bigo


class RoomUser(EntityX):
    """ 房间用户
    """
    
    roomUserId = AutoField()
    room = ForeignKeyField(bigo.Room, backref='roomUsers', column_name='roomId', on_delete='CASCADE')
    user = ForeignKeyField(bigo.User, backref='roomUsers', column_name='userId', on_delete='CASCADE')
    
    class Meta:
        database = bigo.db
        name = '房间用户'
        