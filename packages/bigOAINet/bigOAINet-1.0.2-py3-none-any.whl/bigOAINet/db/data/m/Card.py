from peewee import IntegerField, CharField, DateTimeField, ForeignKeyField, BooleanField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class Card(EntityX):
    class Meta:
        database = bigo.db
        name = '证件'
        
    cardId = AutoField()
    
    # 名称、类别、号码、短号码
    name = CharField(max_length=200)
    type = CharField(max_length=200, default='identificationCard')
    number = CharField(max_length=200)
    shortNumber = CharField(max_length=200)
    
    # 文件、外链id、外链类型
    file = CharField(max_length=200, null=True)
    linkId = IntegerField(default=-1)
    linkType = CharField(max_length=200, null=True)
    
    # 生效时间、过期时间、签发机关
    effectiveTime = DateTimeField(null=True)
    expireTime = DateTimeField(null=True)
    authority = CharField(max_length=200)
    
    # 真名、性别、民族、生日、地址、籍贯
    trueName = CharField(max_length=200)
    gender = CharField(max_length=200, default='secret')
    ethnicity = CharField(max_length=200)
    birthday = DateTimeField(null=True)
    address = CharField(max_length=200)
    origo = CharField(max_length=200)
    
    # 军官衔级、军官部门、职务
    rank = CharField(max_length=200)
    officerDepartment = CharField(max_length=200)
    position = CharField(max_length=200)
    
    # user = ForeignKeyField(User, backref='cardList', column_name='userId', on_delete='CASCADE')

    @property
    def typeText(self):
        types = {
            "identificationcard": "身份证",
            "officercard": "军官证",
            "cliniccard": "门诊卡"
        }
        return types.get(self.type.lower(), "身份证")

    @property
    def genderText(self):
        genders = {
            "male": "男",
            "female": "女",
            "secret": "保密",
            "unknow": "未知",
        }
        return genders.get(self.gender.lower(), "未知")
