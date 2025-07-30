
from datetime import datetime
from peewee import (
    Model, MySQLDatabase, 
    AutoField, ForeignKeyField,
    IntegerField,
    CharField, TextField,
    FloatField, DoubleField,
    BooleanField, DateTimeField
)
from mxupy import EntityX
import bigOAINet as bigo


class Country(EntityX):
    class Meta:
        database = bigo.db
        name = '国家'
        
    countryId = IntegerField(primary_key=True)
    
    # 国际标准化组织、名称、英文名称
    iso = CharField(max_length=200)
    name = CharField(max_length=200)
    enname = CharField(max_length=200)


    