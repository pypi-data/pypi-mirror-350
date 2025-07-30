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

class City(EntityX):
    class Meta:
        database = bigo.db
        name = '城市'
        
    cityId = IntegerField(primary_key=True)
    
    # 名称、英文名称
    name = CharField(max_length=200)
    enname = CharField(max_length=200)
    
    # 省
    province = ForeignKeyField(bigo.Province, backref='cityList', column_name='provinceId', on_delete='CASCADE')