from peewee import Model, IntegerField, CharField, AutoField, ForeignKeyField
from mxupy import EntityX
import bigOAINet as bigo


class UserNoBind(EntityX):
    class Meta:
        database = bigo.db
        name = '用户不绑定'
    userNoBindId = AutoField()

    # 用户id，关联用户表的外键
    userId = IntegerField()
    
    # 平台，如微信、QQ、电话等
    platform = CharField(max_length=200, null=False)
    
    # 平台文本，根据平台值返回对应的设备文本
    @property
    def platformText(self):
        # 根据平台返回对应的设备文本
        platforms = { 'pc': '电脑', 'mobile': '手机', 'qq': 'QQ', 'wechat': '微信' }
        return platforms.get(self.platform, '电脑')

    # 用户
    # user = ForeignKeyField(User, backref='userBindList', column_name='userId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.user} - {self.platformText}"
