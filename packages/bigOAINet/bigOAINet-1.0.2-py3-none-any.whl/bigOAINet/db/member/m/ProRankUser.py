from peewee import Model, IntegerField, ForeignKeyField, AutoField
from mxupy import EntityX
import bigOAINet as bigo


class ProRankUser(EntityX):
    class Meta:
        database = bigo.db
        name = '用户业务'
    proRankUserId = AutoField()

    # 用户、职务等级
    # user = ForeignKeyField(User, backref='proRankUserList', column_name='userId', on_delete='CASCADE')
    proRank = ForeignKeyField(
        bigo.ProRank, backref='proRankUserList', column_name='proRankId', on_delete='CASCADE')

    def __str__(self):
        return f"{self.proRank} - {self.user}"
