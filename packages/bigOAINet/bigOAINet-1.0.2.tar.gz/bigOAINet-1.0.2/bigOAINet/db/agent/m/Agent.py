from peewee import (
    IntegerField,
    CharField,
    TextField,
    DateTimeField,
    ForeignKeyField,
    BooleanField,
    AutoField,
)
from mxupy import EntityX
import bigOAINet as bigo

class Agent(EntityX):
    
    class Meta:
        database = bigo.db
        name = "智能体"

    agentId = AutoField()

    # 名称、标签集、logo、描述
    name = CharField()
    tags = CharField()
    logo = CharField()
    desc = TextField()

    # 是否可以多人，意思是群聊，此信息只有智能体本身才能确定
    # 当可以群聊时，界面上会出现聊天、会话历史的面板
    canGroup = BooleanField(null=False)
    canChat = BooleanField(null=False)

    # 类型，可以是智能体Agent、工作流Workflow、聊天助手ChatAssistant、文本生成应用TextGen、Chatflow
    # 注意工具无法直接调用，dify没有给出对应的api，工具直接嵌入到智能体就可以了
    type = CharField()

    # 唯一标识，在服务器端、只有标识正确的智能体才能正确调用
    apiKey = CharField()
    
    # 管理界面、展示界面
    adminUrl = CharField()
    showUrl = CharField()
    
    agentCatalog = ForeignKeyField(bigo.AgentCatalog, backref='agents', column_name='agentCatalogId')
    
