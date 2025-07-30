from peewee import Model, IntegerField, CharField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class ProRank(EntityX):
    class Meta:
        database = bigo.db
        name = '业务'
    proRankId = AutoField()
    
    # 名称、英文名称、描述、缩略图、排序
    name = CharField(max_length=200, null=False)
    enName = CharField(max_length=200, null=True)
    desc = CharField(null=True)
    thumb = CharField(max_length=200, null=True)
    sort = IntegerField()

    def __str__(self):
        return self.name or self.enName or str(self.proRankId)
