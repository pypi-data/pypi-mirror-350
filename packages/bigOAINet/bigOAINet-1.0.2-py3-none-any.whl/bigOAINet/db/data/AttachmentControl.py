import mxupy as mu
from datetime import datetime
from bigOAINet.db.data.m.Attachment import Attachment

class AttachmentControl(mu.EntityXControl):
    class Meta:
        model_class = Attachment
        
#     @staticmethod
#     def get_instance():
#         if AttachmentControl.instance is None:
#             AttachmentControl.instance = AttachmentControl()
#         return AttachmentControl.instance

#     def add_attachment(self, path, link_id, link_type, file_type="attachment",
#                         userId=-1, name="", code="", desc="", is_exists_verify=True):
#         if not path:
#             return IM.error("添加失败，附件路径为空。")

#         attachment, created = Attachment.get_or_create(
#             userId=userId,
#             path=path,
#             link_id=link_id,
#             link_type=link_type,
#             type=file_type,
#             name=name,
#             code=code,
#             desc=desc
#         )

#         if path.lower().startswith("http"):
#             attachment.name = name if name else path
#             attachment.file_type = "http"
#         else:
#             if self._file_control_exists(path):
#                 file_meta = self._get_file_meta(path)
#                 attachment.size = file_meta.size
#                 attachment.creation_time = file_meta.creation_time
#                 attachment.modify_time = file_meta.modify_time
#                 attachment.name = name if name else file_meta.name
#                 attachment.file_type = file_meta.type
#             else:
#                 if is_exists_verify:
#                     return IM.error("添加失败，附件不存在。")
#                 attachment.name = name if name else path
#                 attachment.file_type = "unknown"

#         attachment.save()
#         return IM.success(attachment)

#     def update_attachment(self, attachment_id, **kwargs):
#         attachment = Attachment.get_by_id(attachment_id)
#         if not attachment:
#             return IM.error("附件不存在")

#         for key, value in kwargs.items():
#             setattr(attachment, key, value)

#         attachment.save()
#         return IM.success(attachment)

#     def delete_attachment(self, attachment_id):
#         attachment = Attachment.get_by_id(attachment_id)
#         if not attachment:
#             return IM.error("附件不存在")

#         attachment.delete_instance()
#         return IM.success(f"附件 {attachment_id} 删除成功。")

#     def download_attachment(self, attachment_id):
#         attachment = Attachment.get_by_id(attachment_id)
#         if not attachment:
#             return IM.error("附件不存在")

#         attachment.downloads += 1
#         attachment.save()

#         im = IM.success(attachment)
#         im.data = attachment.path
#         im.count = attachment.downloads
#         return im

#     def _file_control_exists(self, path):
#         # Implement your logic to check if the file exists
#         return True  # or False

#     def _get_file_meta(self, path):
#         # Implement your logic to get file metadata
#         return type('FileMeta', (object,), {'size': 1024, 'creation_time': datetime.now(), 'modify_time': datetime.now(), 'name': 'example', 'type': 'txt'})

# # Usage
# attachment_control = AttachmentControl.get_instance()
# result = attachment_control.add_attachment(path="/path/to/attachment", link_id=1, link_type="type", type="attachment")

