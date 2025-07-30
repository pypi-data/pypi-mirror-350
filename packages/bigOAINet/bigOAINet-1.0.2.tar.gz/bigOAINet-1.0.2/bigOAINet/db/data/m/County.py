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

class County(EntityX):
    class Meta:
        database = bigo.db
        name = '县区'
        
    countyId = IntegerField(primary_key=True)
    
    # 名称、英文名称、编码
    name = CharField(max_length=200)
    enname = CharField(max_length=200)
    code = CharField(max_length=200)
    
    # 市
    city = ForeignKeyField(bigo.City, backref='countyList', column_name='cityId', on_delete='CASCADE')
    
if __name__ == '__main__':
    
    rc = County()
    print(rc._meta)