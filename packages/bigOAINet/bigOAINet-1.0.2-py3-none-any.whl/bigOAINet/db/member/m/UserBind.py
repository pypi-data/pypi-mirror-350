from datetime import datetime
from peewee import Model, IntegerField, CharField, AutoField, DateTimeField, ForeignKeyField
from mxupy import EntityX
import bigOAINet as bigo


class UserBind(EntityX):
    class Meta:
        database = bigo.db
        name = '用户绑定'
    userBindId = AutoField()  # 唯一标识符，自动增长

    # 唯一码、平台、绑定时间
    UUID = CharField(max_length=200, null=False)
    platform = CharField(max_length=200, null=False)
    bindTime = DateTimeField(default=datetime.now)
    
    # 子应用类型，如微信小程序(minip)、小游戏(minig)
    type = CharField(max_length=200, null=True)
    # 子类型，如UnionId、OpenId
    subType = CharField(max_length=200, null=True)
    
    # 用户
    # user = ForeignKeyField(User, backref='userBindList', column_name='userId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.user} - {self.platformText}"

    @property
    def platformText(self):
        platforms = { 'pc': '电脑', 'mobile': '手机', 'qq': 'QQ', 'wechat': '微信' }
        return platforms.get(self.platform, '电脑')