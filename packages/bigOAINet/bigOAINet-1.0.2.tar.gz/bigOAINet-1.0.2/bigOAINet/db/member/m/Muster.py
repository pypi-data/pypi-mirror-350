from peewee import Model, CharField, IntegerField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class Muster(EntityX):
    class Meta:
        database = bigo.db
        name = '主'
        
    musterId = AutoField()
    
    # 名称、描述、英文名、缩略图
    name = CharField(max_length=200, null=True)
    desc = CharField(null=True)
    enName = CharField(max_length=200, null=True)
    thumb = CharField(max_length=200, null=True)

    def __str__(self):
        return self.name or self.enName or str(self.musterId)
    