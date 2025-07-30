from datetime import datetime
from peewee import AutoField, IntegerField, CharField, DateTimeField, ForeignKeyField
from mxupy import EntityX

import bigOAINet as bigo

class Log(EntityX):
    class Meta:
        database = bigo.db
        name = '日志'
        
    logId = AutoField()
    
    linkId = IntegerField()
    linkType = CharField(max_length=200)
    linkId2 = IntegerField(null=True)
    linkType2 = CharField(max_length=200)
    
    type = CharField(default='info')
    ip = CharField(max_length=200)
    title = CharField(max_length=200)
    content = CharField()
    
    data = CharField(max_length=200)
    referrer = CharField(max_length=200)
    addTime = DateTimeField(default=datetime.now)
    
    user = ForeignKeyField(bigo.User, backref='logList', column_name='userId', on_delete='CASCADE')
    category = ForeignKeyField(bigo.Category, backref='logList', column_name='categoryId', on_delete='CASCADE')


    # @property
    # def title_text(self):
    #     # 这里需要实现获取 title 对应值的逻辑
    #     # 假设有一个函数 get_log_title_value 来获取 title 的值
    #     return get_log_title_value(self.title) if self.title else ''

    # @property
    # def name_path(self):
    #     # 这里需要实现获取 category 对应 name_path 的逻辑
    #     # 假设有一个函数 get_category_name_path 来获取 name_path 的值
    #     return get_category_name_path(self.category_id) if self.category_id else None

    @property
    def log_text(self):
        # 这里需要实现格式化 item_text 的逻辑
        return f'[{self.add_time}] - {self.level_text} - {self.title} \n{self.content}\n\n'

    @property
    def type_text(self):
        # 这里需要实现根据 level 获取 level_text 的逻辑
        tts = {'info': '信息', 'warn': '警告', 'error': '错误'}
        return tts.get(self.level, 'info')
