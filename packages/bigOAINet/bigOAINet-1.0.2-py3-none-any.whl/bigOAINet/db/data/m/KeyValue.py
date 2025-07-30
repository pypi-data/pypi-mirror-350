from peewee import IntegerField, CharField, AutoField
from mxupy import EntityX
import bigOAINet as bigo

class KeyValue(EntityX):
    class Meta:
        database = bigo.db
        name = '键值对'
        
    keyValueId = AutoField()
    
    # 链接ID、链接类型
    linkId = IntegerField()
    linkType = CharField(max_length=200)
    
    # k:key v:value t:title d:data
    k1 = CharField(max_length=200)
    v1 = CharField(max_length=200)
    t1 = CharField(max_length=200, null=True)
    d1 = CharField(max_length=200, null=True)

    k2 = CharField(max_length=200, null=True)
    v2 = CharField(max_length=200, null=True)
    t2 = CharField(max_length=200, null=True)
    d2 = CharField(max_length=200, null=True)

    k3 = CharField(max_length=200, null=True)
    v3 = CharField(max_length=200, null=True)
    t3 = CharField(max_length=200, null=True)
    d3 = CharField(max_length=200, null=True)

    k4 = CharField(max_length=200, null=True)
    v4 = CharField(max_length=200, null=True)
    t4 = CharField(max_length=200, null=True)
    d4 = CharField(max_length=200, null=True)

    k5 = CharField(max_length=200, null=True)
    v5 = CharField(max_length=200, null=True)
    t5 = CharField(max_length=200, null=True)
    d5 = CharField(max_length=200, null=True)
    
    k6 = CharField(max_length=200, null=True)
    v6 = CharField(max_length=200, null=True)
    t6 = CharField(max_length=200, null=True)
    d6 = CharField(max_length=200, null=True)

    label1 = CharField(max_length=200, null=True)
    label2 = CharField(max_length=200, null=True)
    label3 = CharField(max_length=200, null=True)
    label4 = CharField(max_length=200, null=True)
    label5 = CharField(max_length=200, null=True)
    label6 = CharField(max_length=200, null=True)

    desc5 = CharField(null=True)
    desc6 = CharField(null=True)
    desc1 = CharField(null=True)
    desc2 = CharField(null=True)
    desc3 = CharField(null=True)
    desc4 = CharField(null=True)