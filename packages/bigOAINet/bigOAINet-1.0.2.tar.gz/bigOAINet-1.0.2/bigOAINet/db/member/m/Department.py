from peewee import (
    AutoField, ForeignKeyField,
    IntegerField,
    CharField, TextField,
    BooleanField
)
from mxupy import TreeEntityX
import bigOAINet as bigo


class Department(TreeEntityX):
    class Meta:
        database = bigo.db
        name = '部门'
        
    departmentId = AutoField()
    
    # 名称、简称、缩略图、描述
    name = CharField(max_length=200)
    abbreviation = CharField(max_length=200, null=True)
    thumb = CharField(max_length=200, null=True)
    desc = TextField(null=True)
    
    # 主部门、激活
    isMaster = BooleanField(default=True)
    isActive = BooleanField(null=True)
    
    # 印章、传真、电话、职务电话
    seal = CharField(max_length=200, null=True)
    fax = CharField(max_length=200, null=True)
    phone = CharField(max_length=200, null=True)
    ondutyPhone = CharField(max_length=200, null=True)
    
    # 邮政编码、省、市、区、地址
    zipCode = CharField(max_length=200, null=True)
    provinceId = IntegerField(null=True)
    cityId = IntegerField(null=True)
    countyId = IntegerField(null=True)
    address = CharField(max_length=200, null=True)
    
    # 子部门、深度、路径、排序、名称路径、英文名称、英文名称路径
    # hasChildren = BooleanField(default=False)
    # depth = IntegerField(index=True)
    # path = CharField(max_length=200, index=True)
    sort = IntegerField(default=0)
    namePath = CharField(max_length=200, index=True)
    enname = CharField(max_length=200)
    enNamePath = CharField(max_length=200, index=True)

    # 定义与其它模型的关系
    # departmentUserList = ManyToManyField('self', backref='departmentUserList')
    # departmentAndSubjectList = ManyToManyField('self', backref='departmentAndSubjectList')
    
    enterprise = ForeignKeyField(bigo.Enterprise, backref='departmentList', column_name='enterpriseId', on_delete='CASCADE')
    departmentType = ForeignKeyField(bigo.DepartmentType, backref='departmentList', column_name='departmentTypeId', on_delete='CASCADE')
    
    # # 计算属性
    # @property
    # def enterprise(self):
    #     if self.enterpriseId:
    #         return BeCoolMemberEnterprise.get_by_id(self.enterpriseId)
    #     return None

    # @property
    # def departmentType(self):
    #     if self.departmentTypeId:
    #         return BeCoolMemberDepartmentType.get_by_id(self.departmentTypeId)
    #     return None

    # @property
    # def parentDepartment(self):
    #     if self.parentDepartmentId:
    #         return BeCoolMemberDepartment.get_by_id(self.parentDepartmentId)
    #     return None

    # @property
    # def province(self):
    #     if self.provinceId:
    #         return BeCoolDataProvince.get_by_id(self.provinceId)
    #     return None

    # @property
    # def city(self):
    #     if self.cityId:
    #         return BeCoolDataCity.get_by_id(self.cityId)
    #     return None

    # @property
    # def county(self):
    #     if self.countyId:
    #         return BeCoolDataCounty.get_by_id(self.countyId)
    #     return None

    # @property
    # def rbacMix(self):
    #     # 这里需要根据实际情况来实现获取RBACMix的逻辑
    #     pass


# # 你可能需要定义其它相关的模型
# class BeCoolMemberEnterprise(TreeEntityObjectEx):
#     pass

# class BeCoolMemberDepartmentType(TreeEntityObjectEx):
#     pass

# class BeCoolDataProvince(TreeEntityObjectEx):
#     pass

# class BeCoolDataCity(TreeEntityObjectEx):
#     pass

# class BeCoolDataCounty(TreeEntityObjectEx):
#     pass

# 使用Peewee时，通常需要先创建表
# if __name__ == '__main__':
#     db.connect()
#     db.create_tables([Department, BeCoolMemberEnterprise, BeCoolMemberDepartmentType, BeCoolDataProvince, BeCoolDataCity, BeCoolDataCounty], safe=True)