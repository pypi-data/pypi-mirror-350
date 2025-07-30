from datetime import datetime
from peewee import AutoField, CharField, DateTimeField, ForeignKeyField, TextField, DeferredForeignKey, IntegerField
from mxupy import EntityX
import bigOAINet as bigo



class Chat(EntityX):
    """ 聊天记录
    """
    chatId = AutoField()
    
    type = CharField(default='text')
    content = TextField()
    data = TextField(null=True)
    addTime = DateTimeField(default=datetime.now)
    
    room = ForeignKeyField(bigo.Room, backref='chats', column_name='roomId', on_delete='CASCADE')
    # sessionId = IntegerField()
    session = ForeignKeyField(bigo.Session, backref='chats', column_name='sessionId', on_delete='CASCADE')
    user = ForeignKeyField(bigo.User, backref='chats', column_name='userId', on_delete='CASCADE')
    
    @property
    def typeText(self):
        txt = {
            'text': '文本', 'html': 'HTML', 'markdown': 'MarkDown', 
            'table': '表格', 'code': '代码', 'form': '表单', 'chart': '报表', 
            'image': '图片', 'audio': '语音', 'video': '视频', 'download': '下载'
        }
        return txt.get(self.type, '文本')
    
    
    class Meta:
        database = bigo.db
        name = '聊天记录'
        