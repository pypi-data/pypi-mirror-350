from peewee import Model, CharField, BooleanField, DateTimeField, ForeignKeyField, AutoField, IntegerField
from datetime import datetime
from mxupy import EntityX
import bigOAINet as bigo


class Login(EntityX):
    class Meta:
        database = bigo.db
        name = '登录'
    loginId = AutoField()
    
    # ip、在线否、登录时间、退出时间、平台
    ip = CharField(max_length=200, null=True)
    isOnline = BooleanField()
    loginTime = DateTimeField(default=datetime.now)
    logoutTime = DateTimeField(null=True)
    platform = CharField(max_length=200)
    
    # 令牌用于前端调用函数时校验其有效性
    access_token = CharField(max_length=200)
    
    # user = ForeignKeyField(User, backref='loginList', column_name='userId', on_delete='CASCADE')

    @property
    def platformText(self):
        platforms = { 'pc': '电脑', 'mobile': '手机', 'qq': 'QQ', 'wechat': '微信' }
        return platforms.get(self.platform, '电脑')
    