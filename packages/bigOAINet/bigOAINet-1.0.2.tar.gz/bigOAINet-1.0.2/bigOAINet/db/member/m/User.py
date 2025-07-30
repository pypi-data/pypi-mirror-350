from datetime import datetime
from peewee import (
    AutoField, IntegerField,
    CharField, TextField,
    BooleanField, DateTimeField,
    ForeignKeyField
)
from mxupy import EntityX

import bigOAINet as bigo

class User(EntityX):
    class Meta:
        database = bigo.db
        name = '用户'
        
    userId = AutoField()
    
    # 用户名、密码、昵称、真名
    username = CharField(null=False, unique=True)
    password = CharField(null=False)
    nickname = CharField(null=True)
    realname = CharField(null=True)
    
    # 激活、在线、删除、校验
    isActive = BooleanField(default=False)
    isOnline = BooleanField(default=False)
    isDelete = BooleanField(default=False)
    isValidate = BooleanField(default=False)
    
    # 电话、手机、办公电话、备用电话
    phone = CharField(null=True)
    mobile = CharField(null=True)
    officePhone = CharField(null=True)
    alternativePhone = CharField(null=True)
    
    # 签名、描述、手动签名、图像
    sign = CharField(null=True)
    desc = TextField(null=True)
    handSign = CharField(null=True)
    avatar = CharField(null=True)
    
    # 身份证号、qq、邮箱、邮编
    no = CharField(null=True)
    qq = CharField(null=True)
    email = CharField(null=True)
    zipCode = CharField(null=True)
    
    # 性别、生日、排序、地址
    sex = CharField(default='secret')
    birthday = DateTimeField(null=True)
    sort = IntegerField(default=0)
    address = CharField(null=True)
    
    # 最后一次登录ip、登录次数、最后一次登录时间、创建时间
    ip = CharField(null=True)
    logins = IntegerField(default=0)
    loginTime = DateTimeField(null=True)
    createTime = DateTimeField(default=datetime.now)
    
    # 角色集（多个用逗号分隔）、权限集、卡密、访问令牌
    roles = CharField(null=True)
    rights = CharField(null=True)
    cardSerial = CharField(null=True)
    accessToken = CharField(null=False)
    
    # 云服务器、应用类型、过期时间
    server = CharField(null=True)
    appType = CharField(null=True)
    expiryTime = DateTimeField(null=True)
    
    # departmentUser = ForeignKeyField(DepartmentUser, backref='users', on_delete='CASCADE', column_name='departmentUserId')
    # groupUser = ForeignKeyField(GroupUser, backref='users', on_delete='CASCADE', column_name='groupUserId')
    
    country = ForeignKeyField(bigo.Country, backref='users', on_delete='CASCADE', column_name='countryId', null=True)
    province = ForeignKeyField(bigo.Province, backref='users', on_delete='CASCADE', column_name='provinceId', null=True)
    city = ForeignKeyField(bigo.City, backref='users', on_delete='CASCADE', column_name='cityId', null=True)
    county = ForeignKeyField(bigo.County, backref='users', on_delete='CASCADE', column_name='countyId', null=True)
    
    # 详细地址
    @property
    def addressDetail(self):
        return self.country.name + self.province.name + self.city.name + self.county.name + self.address
    
    # 年龄
    @property
    def age(self):
        if self.birthday:
            return datetime.now().year - self.birthday.year - ((datetime.now().month, datetime.now().day) < (self.birthday.month, self.birthday.day))
        return 0

    # 性别
    @property
    def sexText(self):
        sexs = {'male': '男', 'female': '女', 'secret': '保密', 'unknown': '未知'}
        return sexs.get(self.sex, '未知')

    # 名称
    @property
    def name(self):
        # 优先级 realName > nickName > userName
        return self.realName if self.realName else (self.nickName if self.nickName else self.userName)
