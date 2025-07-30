from peewee import IntegerField, CharField, DateTimeField, ForeignKeyField, BooleanField, AutoField
from mxupy import EntityX

import bigOAINet as bigo


class KB(EntityX):
    class Meta:
        database = bigo.db
        name = '知识库'

    KBId = AutoField()

    name = CharField(max_length=200)
    enterprise = ForeignKeyField(bigo.Enterprise, backref='kbs', column_name='enterpriseId', null=True)
    user = ForeignKeyField(bigo.User, backref='kbs', column_name='userId', null=True)
    # dify 知识库id
    uuid = CharField(max_length=200)
