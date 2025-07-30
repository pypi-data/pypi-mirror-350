from datetime import datetime
from peewee import AutoField, IntegerField, CharField, DateTimeField
from mxupy import TreeEntityX
import bigOAINet as bigo

class Category(TreeEntityX):
    categoryId = AutoField()
    
    name = CharField(max_length=200, null=True)
    namePath = CharField(max_length=200, null=True)
    logCount = IntegerField(null=True)
    addTime = DateTimeField(default=datetime.now)

    class Meta:
        database = bigo.db
        name = '日志分类'