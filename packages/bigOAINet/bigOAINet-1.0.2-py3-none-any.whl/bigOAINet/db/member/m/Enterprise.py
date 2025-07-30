from datetime import datetime
from peewee import IntegerField, CharField, DateTimeField, ForeignKeyField, BooleanField, TextField, AutoField
from mxupy import TreeEntityX
import bigOAINet as bigo


class Enterprise(TreeEntityX):
    class Meta:
        database = bigo.db
        name = '企业'
        
    enterpriseId = AutoField()
    
    # 父企业
    parentEnterpriseId = IntegerField(null=True)
    
    # 名称、类型、描述、logo、添加时间
    name = CharField(max_length=200)
    type = CharField(max_length=200, default='enterprise')
    desc = TextField(null=True)
    logo = CharField(max_length=200)
    addTime = DateTimeField(default=datetime.now)
    
    # 注册号、组织机构代码、税务登记号、三证合一号
    registrationNo = CharField(max_length=200)
    organizationCode = CharField(max_length=200)
    taxNo = CharField(max_length=200)
    number = CharField(max_length=200)
    
    # 传真、电话、邮箱、邮编、主页、地址
    fax = CharField(max_length=200)
    phone = CharField(max_length=200)
    email = CharField(max_length=200)
    zipCode = CharField(max_length=200)
    url = CharField(max_length=200)
    address = CharField(max_length=200)
    
    # 注册时间、注册资金（万）、成立时间
    registerTime = DateTimeField(null=True)
    registerFund = IntegerField(null=True)
    foundTime = DateTimeField(null=True)
    
    # 公有制否、营业面积、注册地址、营业范围、年产规模、公司规模、社保状况、备注
    isPublic = BooleanField(default=True)
    businessArea = IntegerField(null=True)
    registerAddress = CharField(max_length=200)
    runRange = CharField(max_length=200)
    annualScale = CharField(max_length=200)
    scale = CharField(max_length=200)
    socialSecurity = CharField(max_length=200)
    remark = TextField(null=True)
    
    # 验证否、验证人、验证时间、激活否、激活人、激活时间、注销否、注销时间
    isValidate = BooleanField(default=False)
    validatorId = IntegerField(null=True)
    validateTime = DateTimeField(null=True)
    isActive = BooleanField(default=True)
    activeUserId = IntegerField(null=True)
    activeTime = DateTimeField(null=True)
    isLogout = BooleanField(default=False)
    logoutTime = DateTimeField(null=True)
    
    # 联系人、联系人邮箱、联系人电话、法人邮箱、法人电话
    linkmanCardId = IntegerField(null=True)
    linkmanEmail = CharField(max_length=200)
    linkmanPhone = CharField(max_length=200)
    legalPersonEmail = CharField(max_length=200)
    legalPersonPhone = CharField(max_length=200)
    
    # 行业、国家、省、市、区、用户、法人证件
    industry = ForeignKeyField(bigo.Industry, backref='enterpriseList', column_name='industryId', on_delete='CASCADE')
    country = ForeignKeyField(bigo.Country, backref='enterpriseList', column_name='countryId', on_delete='CASCADE')
    province = ForeignKeyField(bigo.Province, backref='enterpriseList', column_name='provinceId', on_delete='CASCADE')
    city = ForeignKeyField(bigo.City, backref='enterpriseList', column_name='cityId', on_delete='CASCADE')
    county = ForeignKeyField(bigo.County, backref='enterpriseList', column_name='countyId', on_delete='CASCADE')
    # # user = ForeignKeyField(User, backref='enterpriseList', column_name='userId', on_delete='CASCADE')
    legalPersonCard = ForeignKeyField(bigo.Card, backref='enterpriseList', column_name='legalPersonCardId', on_delete='CASCADE')
    
    @property
    def type_text(self):
        if not self.type:
            return "企业"
        
        types = {
            "enterprise": "企业",
            "school": "学校",
            "government": "政府",
            "organization": "组织"
        }
        
        return types.get(self.type.lower(), "企业")
    