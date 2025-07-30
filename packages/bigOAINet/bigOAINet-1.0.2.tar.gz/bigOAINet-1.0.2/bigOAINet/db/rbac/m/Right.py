from peewee import IntegerField, CharField, BooleanField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class Right(EntityX):
    rightId = AutoField()
    
    # 名称、编码、编码路径、描述、是默认的、有数据否、排序
    name = CharField(max_length=200)
    code = CharField(max_length=200)
    codePath = CharField(max_length=200, null=True)
    desc = CharField(max_length=200, null=True)
    isDefault = BooleanField(default=True)
    hasData = BooleanField(default=False)
    sort = IntegerField(default=0)
    
    rightCategory = ForeignKeyField(bigo.RightCategory, backref='rightList', column_name='rightCategoryId', on_delete='CASCADE')

    # @property
    # def datas(self):
    #     if self._datas is None:
    #         self._datas = RightAndData.select().where(RightAndData.rightId == self.rightId)
    #     return self._datas

    @property
    def valueList(self):
        values = []
        for data in self.datas:
            if data.v1:
                values.append(data.v1)
            if data.v2:
                values.append(data.v2)
            if data.v3:
                values.append(data.v3)
            if data.v4:
                values.append(data.v4)
            if data.v5:
                values.append(data.v5)
            if data.v6:
                values.append(data.v6)
        return values

    @property
    def values(self):
        return ','.join(self.valueList)

    class Meta:
        database = bigo.db
        name = '权限'
        
