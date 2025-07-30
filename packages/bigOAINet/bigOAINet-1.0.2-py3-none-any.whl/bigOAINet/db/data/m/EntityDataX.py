from datetime import datetime
from peewee import IntegerField, CharField, DateTimeField, ForeignKeyField, AutoField, FloatField, BooleanField
from mxupy import EntityX
import mxupy as mu
import bigOAINet as bigo


class EntityDataX(EntityX):
    
    def __init__(self, *args, db=None, **kwargs):
        super().__init__(*args, db=db, **kwargs)
        
        self._attachment = None
        self._attachmentThumb = None
        self._attachmentPath = None
        self._attachmentList = None
        self._attachmentPaths = None
        self._hasAttachment = False
        
        self._linkConditions = self.link_conditions()

    def link_conditions(self):
        return [{'linkType':self.table_name}, {'linkId':mu.get_attr(self, self.key_name)}, {'linkId':('!=', 0)}]

    @property
    def attachment(self):
        """附件实体（第一个）"""
        if self._attachment is not None:
            return self._attachment
        
        if not self.hasAttachment:
            return None

        im = bigo.AttachmentControl.inst().get_one(where=self._linkConditions)
        if im.error:
            return None
        self._attachment = im.data
            
        return self._attachment

    @attachment.setter
    def attachment(self, value):
        self._attachment = value

    # @property
    # def attachmentPath(self):
    #     """附件路径（第一个）"""
    #     if self._entityInfo.isAdditional:
    #         return ""

    #     if self._attachmentPath is None and self._attachment is not None:
    #         self._attachmentPath = self._attachment.vString("Path")

    #     return self._attachmentPath

    # @attachmentPath.setter
    # def attachmentPath(self, value):
    #     self._attachmentPath = value

    # @property
    # def attachmentList(self):
    #     """对应附件列表"""
    #     if self._attachmentList is not None:
    #         return self._attachmentList

    #     if self._selectFieldsAndExtendsInfo.isNeedExtend("AttachmentList"):
    #         if self._entityInfo.isAdditional:
    #             return []

    #         if not self.hasAttachment:
    #             return []

    #         if self._attachmentList is None:
    #             # 假设 AttachmentControl 是一个类，Instance 是单例
    #             self._attachmentList = bigo.AttachmentControl.inst().get_list(
    #                 self._linkConditions, None, 1, -1,
    #                 self._selectFieldsAndExtendsInfo.selectExtends.get("AttachmentList")
    #             )
    #     return self._attachmentList

    # @attachmentList.setter
    # def attachmentList(self, value):
    #     self._attachmentList = value

    # @property
    # def attachmentPaths(self):
    #     """附件路径集合"""
    #     if self._entityInfo.isAdditional:
    #         return []

    #     if self._attachmentPaths is None and self._attachmentList is not None:
    #         # 假设 SelectOn 是一个方法，用于获取指定字段的值
    #         self._attachmentPaths = [item.vString("Path") for item in self._attachmentList]
    #     return self._attachmentPaths

    # @attachmentPaths.setter
    # def attachmentPaths(self, value):
    #     self._attachmentPaths = value

    @property
    def hasAttachment(self):
        """是否有附件"""
        im = bigo.AttachmentControl.inst().exists(self._linkConditions)
        if im.error:
            return False
        self._hasAttachment = im.data
        return self._hasAttachment