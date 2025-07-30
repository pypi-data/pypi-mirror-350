from datetime import datetime
from peewee import IntegerField, CharField, DateTimeField, ForeignKeyField, AutoField, FloatField, BooleanField
from mxupy import EntityX
import bigOAINet as bigo


class Attachment(EntityX):
    
    class Meta:
        database = bigo.db
        name = '附件'
        
    attachmentId = AutoField()
    
    # 名称、类型、编码、图标、路径、描述
    name = CharField()
    type = CharField(default='attachment')
    code = CharField(null=True)
    icon = CharField(null=True)
    path = CharField()
    desc = CharField(null=True)
    
    # 大小、文件类型、添加时间、创建时间、修改时间
    size = FloatField()
    fileType = CharField(null=True)
    addTime = DateTimeField(default=datetime.now)
    creationTime = DateTimeField(null=True)
    modifyTime = DateTimeField(null=True)
    
    # 链接ID、链接类型、下载次数、下载URL
    linkId = IntegerField()
    linkType = CharField(null=True)
    downloads = IntegerField(default=0)
    downloadUrl = CharField(max_length=255, default='')

    # 文件版本ID、文件ID
    fileVersionId = CharField(null=True)
    fileId = CharField(null=True)
    
    # 用户
    # user = ForeignKeyField(User, backref='attachmentList', column_name='userId', on_delete='CASCADE')

    @property
    def isExistsVerify(self):
        return True
    
    @property
    def typeText(self):
        types = {
            "thumb": "缩略图", "smallthumb": "小缩略图", "bigthumb": "大缩略图", 
            "image": "图片", "video": "视频", "music": "音乐", "audio": "音频", 
            "config": "配置", "attachment": "附件", "winrar": "压缩包", "other": "其他"
        }
        return types.get(self.type.lower(), "其他")

    @property
    def typeEnum(self):
        types = {
            "thumb": 0, "smallthumb": 1, "bigthumb": 2,
            "image": 3, "video": 4,  "music": 5, "audio": 6,
            "config": 7, "attachment": 8, "winrar": 9, "other": 10
        }
        return types.get(self.type.lower(), 10)

    @property
    def previewUrl(self):
        if not self.path:
            return ""
        if self.fileType.lower() in ["doc", "docx", "xls", "xlsx", "ppt", "pptx"] and self.path.startswith("http"):
            return "/BeCool/Base/OfficeDocumentPreview.aspx?path=" + self.path
        if self.path.lower().endswith(".pdf"):
            return "/BeCool/Base/PDFPreview.aspx?path=" + self.path
        return self.path


    # @property
    # def sizeText(self):
    #     # 假设存在一个函数来转换文件大小为易读的格式
    #     return convert_size_to_readable_format(self.size)

    # @property
    # def fileTypeText(self):
    #     # 假设存在一个函数来获取文件类型的文本描述
    #     return get_file_type_text_description(self.fileType)