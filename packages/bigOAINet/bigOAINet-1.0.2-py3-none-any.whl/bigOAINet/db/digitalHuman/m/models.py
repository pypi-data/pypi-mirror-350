from datetime import datetime
from peewee import Model, AutoField,IntegerField, CharField, BooleanField, TextField,DoubleField, ForeignKeyField, MySQLDatabase,DateTimeField
import mxupy as mu
import bigOAINet as bigo

# 语音模型
class MyDHVoiceModel(mu.EntityX):
    
    myDHVoiceModelId = AutoField()
    
    # 名称、克隆用的原声地址、文本、是否训练、添加时间
    name = CharField()
    referUrl = CharField()
    text = TextField(null=True)
    isFinish = BooleanField(default=False)
    addTime = DateTimeField(default=datetime.now)
    
    # 用户
    user = ForeignKeyField(bigo.User, backref='myDHVoiceModels', column_name='userId', on_delete='CASCADE')
    
    class Meta:
        database = bigo.db
        name = '语音模型'

# 语音结果
class MyDHVoice(mu.EntityX):
    
    myDHVoiceId = AutoField()
    
    # 名称、路径、时长、生成音频用的文本
    name = CharField()
    url = CharField()
    duration = DoubleField(default=0.00)
    text = TextField(null=True)
    addtime = DateTimeField(default=datetime.now)
    
    myDHVoiceModel = ForeignKeyField(MyDHVoiceModel, backref='myDHVoices', column_name='myDHVoiceModelId', on_delete='CASCADE')
    user = ForeignKeyField(bigo.User, backref='myDHVoices', column_name='userId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '真人语音'

# 视频模型
class MyDHVideoModel(mu.EntityX):
    
    myDHVideoModelId = AutoField()
    
    # 名称、宽、高、缩略图、添加时间
    name = CharField()
    width = IntegerField(default=1080)
    height = IntegerField(default=1920)
    thumb = CharField(null=True)
    addTime = DateTimeField(default=datetime.now)
    
    user = ForeignKeyField(bigo.User, backref='myDHVideoModels', column_name='userId', on_delete='CASCADE')
    
    class Meta:
        database = bigo.db
        name = '数字人模型'
        
# 数字人模型动作
class MyDHVideoModelAction(mu.EntityX):
    
    myDHVideoModelActionId = AutoField()
    
    # 名称、地址、缩略图、类型
    name = CharField()
    url = CharField()
    thumb = CharField(null=True)
    type = CharField(default='static')
    
    # 用户、视频模型
    user = ForeignKeyField(bigo.User, backref='myDHVideoModelActions', column_name='userId', on_delete='CASCADE')
    myDHVideoModel = ForeignKeyField(MyDHVideoModel, backref='myDHVideoModelActions', column_name='myDHVideoModelId', on_delete='CASCADE')
    
    
    # 当用户只传入了一个静态视频 做了这个处理之后 再进行合成 （0个动作）
    # concatVideoWithReverse
    # 一个视频进行拼接反向
    # 不需要考虑音频时长
    
    # 如果传入静态（1个）+ 动作（1个或多个） 
    # 要考虑音频时长（函数已经做了处理）
    # 函数名暂定
    
    # 进入 和 离开 在特定情况下才会有
    
    
    @property
    def typeText(self):
        txt = {
            'static': '静态', 'enter': '进入', 'left': '离开', 'action': '动作'        
        }
        return txt.get(self.type, '静态')
    
    class Meta:
        database = bigo.db
        name = '数字人模型动作'

# 视频(两种生成路径)
# 1、文本 + 语音模型 + 视频模型 -> 语音 + 视频模型 -> 视频
# 2、语音 + 视频模型 -> 视频
class MyDHVideo(mu.EntityX):
    
    myDHVideoId = AutoField()
        
    # 名称、缩略图、宽、高、类型、文本
    name = CharField()
    thumb = CharField(null=True)
    width = IntegerField(default=1080)
    height = IntegerField(default=1920)
    text = TextField(null=True)
    
    # 声度、视频路径、生成结果路径、完成否、是否使用语音、添加时间
    voiceSpeed = IntegerField(default=1)
    videoUrl = CharField(null=True)
    resultUrl = CharField(null=True)
    isFinish = BooleanField(default=False)
    
    # 使用语音：表明采用第一种生成路径，不使用语音：表明采用第二种生成路径
    useVoice = BooleanField(default=True)
    addTime = DateTimeField(default=datetime.now)
    finishTime = DateTimeField(null=True)
    
    # 用户、语音、语音模型、视频模型
    user = ForeignKeyField(bigo.User, backref='myDHVideos', column_name='userId', on_delete='CASCADE')
    myDHVoice = ForeignKeyField(MyDHVoice, backref='myDHVideos', column_name='myDHVoiceId', on_delete='CASCADE', null=True)
    myDHVoiceModel = ForeignKeyField(MyDHVoiceModel, backref='myDHVideos', column_name='myDHVoiceModelId', on_delete='CASCADE', null=True)
    myDHVideoModel = ForeignKeyField(MyDHVideoModel, backref='myDHVideos', column_name='myDHVideoModelId', on_delete='CASCADE')
    
    class Meta:
        database = bigo.db
        name = '数字人视频'





# 我的名片
class MyDHCard(mu.EntityX):
    
    myDHCardId = AutoField()
    
    # 名称
    name = CharField()
    defaultCardModelId = IntegerField(null=True)
    
    # 默认名片模型、用户
    # myDHDefaultCardModel = ForeignKeyField(bigo.MyDHCardModel, backref='myDHCards', column_name='myDHCardId', on_delete='CASCADE')
    # myDHDefaultCardModel = ForeignKeyField('MyDHCardModel', backref='myDHCards', column_name='myDHCardId', on_delete='CASCADE')
    user = ForeignKeyField(bigo.User, backref='myDHCards', column_name='userId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '我的名片'

# 我的名片模型
class MyDHCardModel(mu.EntityX):
    
    myDHCardModelId = AutoField()
    
    # 名称、语速
    name = CharField()
    voiceSpeed = IntegerField(default=1)
    
    # 名片、数字人模型、语音模型、用户
    myDHCard = ForeignKeyField(MyDHCard, backref='myDHCardModels', column_name='myDHCardId', on_delete='CASCADE')
    myDHVideoModel = ForeignKeyField(MyDHVideoModel, backref='myDHCardModels', column_name='myDHVideoModelId', on_delete='CASCADE')
    myDHVoiceModel = ForeignKeyField(MyDHVoiceModel, backref='myDHCardModels', column_name='myDHVoiceModelId', on_delete='CASCADE', null=True)
    user = ForeignKeyField(bigo.User, backref='myDHCardModels', column_name='userId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '我的名片模型'



# 问答集
class MyDHQA(mu.EntityX):
    
    myDHQAId = AutoField()
    
    # 问题、答案、字幕、视频路径
    question = CharField()
    answer = TextField()
    subtitle = TextField(null=True)
    videoUrl = CharField(null=True)
    
    # 用户
    user = ForeignKeyField(bigo.User, backref='myDHQAs', column_name='userId', on_delete='CASCADE')

    class Meta:
        database = bigo.db
        name = '问答集'

# 问答记录
class MyDHQARecord(mu.EntityX):
    
    myDHQARecordId = AutoField()
    
    # 问题、记录时间
    question = TextField()
    addTime = DateTimeField(default=datetime.now)
    
    # 用户、问答集
    user = ForeignKeyField(bigo.User, backref='myDHQARecords', column_name='userId', on_delete='CASCADE')
    myDHQA = ForeignKeyField(MyDHQA, backref='myDHQARecords', column_name='myDHQAId', on_delete='CASCADE')
    # myDHCard = ForeignKeyField(MyDHCard, backref='myDHQARecords', column_name='myDHCardId', on_delete='CASCADE')
    # myDHVideoModel = ForeignKeyField(MyDHVideoModel, backref='myDHQARecords', column_name='myDHVideoModelId', on_delete='CASCADE')
    
    class Meta:
        database = bigo.db
        name = '问答记录'
        
# 我的名片模型和问答集
class MyDHCardModelAndQA(mu.EntityX):
    
    cardModelAndQAId = AutoField()

    # 是否生成、生成视频路径
    isFinish = BooleanField(default=False)
    videoUrl = CharField(null=True)
    
    # 问答集、我的名片模型
    myDHQA = ForeignKeyField(MyDHQA, backref='myDHCardModelAndQAs', column_name='myDHQAId', on_delete='CASCADE')
    myDHCardModel = ForeignKeyField(MyDHCardModel, backref='myDHCardModelAndQAs', column_name='myDHCardModelId', on_delete='CASCADE')
    
    class Meta:
        database = bigo.db
        name = '我的名片模型和问答集'
 
           
        













        
        
# # 脚本
# class MyDHScript(mu.EntityX):
    
#     myDHScriptId = AutoField()
    
#     # 名称、内容
#     name = CharField()
#     content = TextField()
    
#     # 用户
#     user = ForeignKeyField(bigo.User, backref='myDHScripts', column_name='userId', on_delete='CASCADE')

#     class Meta:
#         database = bigo.db
#         name = '脚本'


# # 问答集附件
# class MyDHQAAttachment(mu.EntityX):
    
#     catechismAttachmentId = AutoField()
    
#     # 附加名称、附件路径、附件类型
#     attachmentName = CharField()
#     attachmentUrl = CharField()
#     attachmentType = CharField()
    
#     # 问答集
#     myDHQA = ForeignKeyField(MyDHQA, column_name='myDHQAId', backref='myDHQAAttachments', on_delete='CASCADE')

#     class Meta:
#         database = bigo.db
#         name = '问答集附件'

# # 新闻
# class DHNews(mu.EntityX):
    
#     newsId = AutoField()

#     # 标题、作者、正文、分类、时间
#     title = CharField()
#     author = CharField()
#     content = CharField()
#     category = CharField()
#     addTime = DateTimeField(default=datetime.now)

#     class Meta:
#         database = bigo.db
#         name = '新闻'

# # 新闻附件
# class DHNewsAttachment(mu.EntityX):
    
#     dhNewsAttachmentId = AutoField()

#     # 名称，全路径，类型，基础路径
#     Name = CharField()
#     Path = CharField()
#     Type = CharField()
#     BasePath = CharField()
    
#     # 下载次数、创建时间
#     downloads = IntegerField(default=0)
#     createTime = DateTimeField(default=datetime.now)

#     # 新闻
#     news = ForeignKeyField(DHNews, backref='dhNewsAttachments', on_delete='CASCADE')

#     class Meta:
#         database = bigo.db
#         name = '新闻附件'

# # 视频
# class MyDHVideo(mu.EntityX):
    
#     myDHVideoId = AutoField()
    
#     # 名称、路径、缩略图、类型、时长
#     name = CharField()
#     url = CharField()
#     thumb = CharField()
#     type = CharField(default='static')
#     duration = DoubleField(default=0.00)
    
#     # 数字人模型id
#     myDHVideoModel = ForeignKeyField(MyDHVideoModel, column_name='myDHVideoModelId', backref='myDHVideos', on_delete='CASCADE')
    
#     @property
#     def typeText(self):
#         txt = {
#             'static': '静态', 'enter': '进入', 'left': '离开', 'action': '动作'        
#         }
#         return txt.get(self.type, '静态')

#     class Meta:
#         database = bigo.db
#         name = '数字人视频'
        
# # 我的项目
# class MyDHProject(mu.EntityX):
    
#     myDHProjectId = AutoField()
    
#     # 名称、缩略图、影片宽、影片高
#     name = CharField()
#     thumb = CharField(null=True)
#     width = IntegerField(default=1080)
#     height = IntegerField(default=1920)
#     type = CharField(default='static')
    
#     # 声音速度、声音结果路径、预览合成路径、生成状态、是否使用声音
#     voiceSpeed = IntegerField(default=1)
#     # 【声音voice的immortalVoiceUrl】 或者 语音模型 + 脚本生成的
#     voiceUrl = CharField(null=True)
#     renderUrl = CharField(null=True)
#     isFinish = BooleanField(default=False)
#     # true：直接用语音 false：脚本+语音模型生成
#     useVoice = BooleanField(default=True)
    
#     # 用户、数字人模型、脚本、真人语音模型、声音
#     user = ForeignKeyField(bigo.User, backref='myDHProjects', column_name='userId', on_delete='CASCADE')
#     myDHVideoModel = ForeignKeyField(MyDHVideoModel, backref='myDHProjects', column_name='myDHVideoModelId', on_delete='CASCADE')
#     # 声音和脚本二选一
#     myDHVoiceModel = ForeignKeyField(MyDHVoiceModel, backref='myDHProjects', column_name='myDHVoiceModelId', on_delete='CASCADE', null=True)
#     myDHVoice = ForeignKeyField(MyDHVoice, backref='myDHProjects', column_name='myDHVoiceId', on_delete='CASCADE', null=True)
    
#     @property
#     def typeText(self):
#         txt = {
#             'static': '静态', 'enter': '进入', 'left': '离开', 'action': '动作'        
#         }
#         return txt.get(self.type, '静态')
    
#     class Meta:
#         database = bigo.db
#         name = '数字人视频'
