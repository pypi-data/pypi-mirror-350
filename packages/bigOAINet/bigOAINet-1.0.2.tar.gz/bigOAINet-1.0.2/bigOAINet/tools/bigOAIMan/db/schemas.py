from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

#接收一组字符串内容
class Contents (BaseModel):
    content: List[str]

# 定义一个模型来存储投票信息
class VoteRequest(BaseModel):
    scheduleId: int
    voteTitle: str
    voteItemContent: Contents
#作业模型
class AssignmentsRequest(BaseModel):
    assignmentsId: Optional[int] = None
    assignmentsName: Optional[str] = None
    assignmentsAnswer: Optional[str] = None
    creater: Optional[int] = None  # 假设这里是用户的 ID 而不是 User 对象
    rule: Optional[str] = None
    createTime: Optional[datetime] = datetime.now
    course: Optional[int] = None  # 课程 ID
    assignmentsFile: Optional[int] = None
#作业模型数组
class AssignmentsRequestList(BaseModel):
    assignmentsList: List[AssignmentsRequest]

#试题模型
class TestsRequest(BaseModel):
    testId : Optional[int] = None
    testContent:Optional[str] = None  # 试题内容
    testAnswer:Optional[str] = None # 试题标准答案
    createTime: Optional[datetime] = datetime.now # 创建时间，默认为当前时间
    creater: Optional[int] = None # 创建者 ID，假设 User 模型中有 userId 字段
    course: Optional[int] = None # 课程 ID
    testFile: Optional[int] = None  # 属于哪个试题文件，方便以后针对文件删除
#试题模型数组
class TestsRequestList(BaseModel):
    testList: List[TestsRequest]


#讨论模型
class DiscussRequest(BaseModel):
    discussId: Optional[int] = None
    title: Optional[str] = None
    discussAnswer: Optional[str] = None
    creater: Optional[int] = None
    course: Optional[int] = None
    createTime: Optional[datetime] = datetime.now 
#讨论模型数组
class DiscussRequestList(BaseModel):
    discussList: List[DiscussRequest]

# 分页模型
class Pagination(BaseModel):
    pageNum: Optional[int] = 1  # 第一页
    pageSize: Optional[int] = 10  # 每页数量


def pagination_params(pageNum: int = 1, pageSize: int = 10) -> Pagination:
    return Pagination(pageNum=pageNum, pageSize=pageSize)



# 响应模型
class ResponseMessage(BaseModel):
    success: bool
    message: str


# 新闻一对多返回模型
class NewsWithAttachments(BaseModel):
    newsId: int
    title: str
    content: Optional[str] = None
    newsTime: Optional[datetime]
    author: str
    attachments: List[dict]


class AddNewsRequest(BaseModel):
    title: str
    content: str
    category: str
    author: str


# 课堂表
class UpdateScheduleRequest(BaseModel):
    scheduleId: int
    course: Optional[int] = None  # 课程ID，对应course表
    scheduleName: Optional[str] = None  # 课堂名称
    invitationCode: Optional[str] = None  # 课堂邀请码
    robotUserId: Optional[int] = None  # 机器人用户ID，对应user表 --6.29新增


# 课程表
class UpdateCourseRequest(BaseModel):
    courseId: int
    # 下面多出一个课程老师表，指定课程与老师多对多关联。此字段取消。teacherId=IntegerField()# 老师ID，对应user表
    courseName: Optional[str] = None  # 课程名称
    courseDesc: Optional[str] = None  # 课程介绍
    startTime: Optional[datetime] = None  # 课程开始时间
    endTime: Optional[datetime] = None  # 课程结束时间
    isOpen: Optional[int] = 1  # 是否公开，0-非公开，1-公开 默认0
    kbName: Optional[str] = None  # 此课程的知识库名称


class News(BaseModel):
    newsId: int
    title: Optional[str] = None  # 标题
    content: Optional[str] = None  # 正文
    newsTime: Optional[datetime] = datetime.now  # 时间
    author: Optional[str] = None  # 作者


class NewsAttachments(BaseModel):
    # 名称，全路径，类型，下载次数，newsId，添加时间
    newsAttachmentsId: int
    attachmentsName: Optional[str] = None  # 名称
    attachmentsPath: Optional[str] = None  # 路径
    attachmentsBasePath: Optional[str] = None  # 全路径
    attachmentsType: Optional[str] = None  # 类型
    downloadNum: Optional[int] = None  # 下载次数
    addTime: Optional[datetime] = datetime.now
    newsId: Optional[int] = None  # 属于哪个新闻


# 更新知识库文件表单
class UpdateKnowledgeFileForm(BaseModel):
    knowledgeFileId: int
    knowledgeName: str
    knowledgeDesc: str


class UpdateKnowledgeForm(BaseModel):
    knowledgeId: Optional[int] = None
    course:Optional[int] = None
    knowledgeNickname: Optional[str] = None
    knowledgeRole: Optional[str] = None
    knowledgeLimit: Optional[str] = None


# 删除知识库文件表单
class DelKnowledgeFileRequest(BaseModel):
    knowledgeFileId: int


class SyncKnowledgeRequest(BaseModel):
    knowledgeId: int


class UpdateAvatarRequest(BaseModel):
    avatar: str


class UpdatePasswordRequest(BaseModel):
    oldPassword: str
    newPassword: str


class DeleteCourseRequest(BaseModel):
    courseId: int


class AddCourseRequest(BaseModel):
    courseName: str
    courseDesc: str
    startTime: Optional[datetime] = datetime.now  # 课程开始时间
    endTime: Optional[datetime] = datetime.now  # 课程结束时间


class DeleteScheduleRequest(BaseModel):
    scheduleId: int


class RegisterVerifyRequest(BaseModel):
    key: str
    value: str


class RegisterRequest(BaseModel):
    userName: str
    nickName: str
    password: str
    qqNum: int
    phone: str
    email: str
    num: str
    role: str
    school: int
    college: int
    dept: int


class LoginRequest(BaseModel):
    userName: str
    password: str


class AddChatRecordRequest(BaseModel):
    chatType: str
    targetId: int


class JoinScheduleRequest(BaseModel):
    scheduleId: int
    userId: int
    invitationCode: str
    userRole: str


class JoinCourseRequest(BaseModel):
    courseId: int
    userId: int


class AddScheduleRequest(BaseModel):
    scheduleName: str
    courseId: int
    invitationCode: str


class AddAdminRequest(BaseModel):
    password: str
    userName: str
    school: int
    college: int
    dept: int


class DelAdminRequest(BaseModel):
    adminId: int


class ApprovedTeacherRequest(BaseModel):
    teacherId: int


class UpdateMessageRequest(BaseModel):
    chatMessageId: int
    status: int
    userId: int


class AddScheduleAssignmentRequest(BaseModel):
    scheduleId: Optional[int] = None
    assignmentName:  str
    rule: str
    courseId: Optional[int] = None


class AddScheduleDiscussRequest(BaseModel):
    scheduleId: Optional[int] = None
    title: str
    courseId: Optional[int] = None


class JudgeAssignmentsScoreRequest(BaseModel):
    scheduleAssignmentsSubmissions: int
    score: float
    judgeContent: str


class ImportTestToScheduleRequest(BaseModel):
    scheduleId: int
    testIds: Optional[List[int]] = None
    courseId: Optional[int] = None


class AddFavRequest(BaseModel):
    messageType: str
    messageUuid: str


class DelFavRequest(BaseModel):
    userFavId: int
