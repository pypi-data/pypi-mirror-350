from peewee import IntegerField, CharField, DateTimeField, ForeignKeyField, BooleanField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class AgentUser(EntityX):
    class Meta:
        database = bigo.db
        name = '智能体用户'

    agentUserId = AutoField()
    agent = ForeignKeyField(bigo.Agent, backref='agentUsers', column_name='agentId')
    user = ForeignKeyField(bigo.User, backref='agentUsers', column_name='userId')
    

    
