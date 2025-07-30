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

class Province(EntityX):
    class Meta:
        database = bigo.db
        name = '省份'
        
    provinceId = IntegerField(primary_key=True)
    
    # 名称、英文名称
    name = CharField(max_length=200)
    enname = CharField(max_length=200)
    
    # 国家
    country = ForeignKeyField(bigo.Country, backref='provinceList', column_name='countryId', on_delete='CASCADE')
