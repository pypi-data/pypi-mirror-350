from datetime import datetime
from peewee import Model, AutoField,IntegerField, CharField, BooleanField, TextField,DoubleField, ForeignKeyField, MySQLDatabase,DateTimeField
import mxupy as mu
import bigOAINet as bigo

class AgentCatalog(mu.EntityX):
    
    class Meta:
        database = bigo.db
        name = '智能体分类'
        
    agentCatalogId = AutoField()
    
    # 名称、logo、应用数量
    name = CharField()
    logo = CharField()
    count = IntegerField(default=0)
    
    