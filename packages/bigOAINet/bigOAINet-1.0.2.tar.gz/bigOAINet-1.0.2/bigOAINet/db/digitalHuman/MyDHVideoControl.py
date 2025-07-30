import uuid as uid
import mxupy as mu
import bigOAINet as bigo

from peewee import *
from datetime import datetime
from mxupy import IM

class MyDHVideoControl(mu.EntityXControl):
    """ 视频控制器
    """
    class Meta:
        model_class = bigo.MyDHVideo
        
    def __init__(self, *args, **kwargs):
        self.sub_dir = 'digitalHuman/video/'
        super().__init__(*args, **kwargs)

    def add1(self, model, userId, accessToken):
        """
            添加

        Args:
            model (MyDHVideoModel|dict): 视频
            userId (int): 用户id
            accessToken (str): 访问令牌
            
        Returns:
            IM：结果
        """
        def _do():
            
            im = IM()
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            im = self.add(model)
            if im.error:
                return im

            # # 创建新数字人
            # newVideo = bigo.MyDHVideo.create(
            #     userId=userId,
            #     name=model.name,
            #     thumb=model.thumb,
            #     modelId=model.modelId,
            #     width=model.width,
            #     height=model.height,
            #     scriptId=None if model.scriptId == -1 else model.scriptId,
            #     # voiceModelId=model.voiceModelId,
            #     voiceModelId=None if model.voiceModelId == -1 else model.voiceModelId,
            #     # voiceId=model.voiceId,
            #     voiceId=None if model.voiceId == -1 else model.voiceId,
            #     voiceSpeed=model.voiceSpeed,
            #     voiceUrl=model.voiceUrl,
            #     renderUrl=model.renderUrl,
            #     renderStatus=model.renderStatus,
            #     useVoice=model.useVoice,
            # )

            # im.msg = '恭喜！保存项目成功。'
            # im.data = model_to_dict(newVideo, False)

            return im

        return self.run(_do)

    def update1(self, model, userId, accessToken):
        """
            修改

        Args:
            model (MyDHVideoModel|dict): 视频
            userId (int): 用户id
            accessToken (str): 访问令牌
            
        Returns:
            IM：结果
        """
        def _do():
            
            im = IM()
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            im = self.update_by_id(model.myDHVideoId, model)
            if im.error:
                return im
            
            return im
            
            
            # obj = mu.dict_to_obj(model)
            
            # cs = [{'myDHVideoId': obj.myDHVideoId}, {'userId': userId}]
            # # 视频是否引用了这个视频模型
            # im = bigo.MyDHVideoControl.inst().exists(where=cs)
            # if im.error:
            #     return im
            # if im.data:
            #     return IM(False, '删除失败。已有视频选中了此视频模型。')

            # project = bigo.MyDHVideo.select().where(bigo.MyDHVideo.projectId == model.projectId, bigo.MyDHVideo.userId == userId).first()
            # if mu.isN(project):
            #     im.success = False
            #     im.msg = '项目不存在'
            #     return im

            # project.name=model.name
            # project.thumb=model.thumb
            # project.modelId=model.modelId
            # project.width=model.width
            # project.height=model.height
            # project.voiceModelId=None if model.voiceModelId == -1 else model.voiceModelId
            # project.voiceId=None if model.voiceId == -1 else model.voiceId
            # project.voiceSpeed=model.voiceSpeed
            # project.voiceUrl=model.voiceUrl
            # project.renderUrl=model.renderUrl
            # project.renderStatus=model.renderStatus
            # project.useVoice=model.useVoice
            # project.save()

            # im.msg = '恭喜！修改项目成功。'
            # im.data = model_to_dict(project, False)

            return im

        return self.run(_do)

    def delete1(self, id, userId, accessToken):
        """
            删除

        Args:
            model (MyDHVideoModel|dict): 视频
            userId (int): 用户id
            accessToken (str): 访问令牌
            
        Returns:
            IM：结果
        """
        def _do():
            
            im = IM()
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            im = self.delete_by_id(id)
            if im.error:
                return im
            
            return im
            
            # # 查询是否存在 projectId 这条数据
            # im1 = self.get_one(where={'projectId': projectId,'userId': userId})
            # if im1.success is False:
            #     return im1
                
            # project = im1.data
            # # 删除自己
            # im3 = self.delete_by_id(projectId)
            # if im3.success is False:
            #     return im3

            # if mu.isNN(project.voiceUrl):
            #     mu.removeFile(mu.file_dir('user',userId) + '\\'  + project.voiceUrl)
            # if mu.isNN(project.renderUrl):
            #     mu.removeFile(mu.file_dir('user',userId) + '\\'  + project.renderUrl)

        return self.run(_do)
    
    def gen(self, model, accessToken):
        """
            生成视频

            如果只有一个static动作，则使用 concatVideoWithReverse
            如果有一个或多个action动作，则使用 genMatchVideo
        Args:
            model (MyDHVideoModel): 视频模型
            accessToken (str): 访问令牌
        Returns:
            IM：结果
        """
        def _do():
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(model.userId, accessToken)
            if im.error:
                return im
            
            im = bigo.MyDHVoiceControl.inst().get_one_by_id(id=model.myDHVoiceId, select=['url'])
            if im.error:
                return im
            if im.data is None:
                return im.set_error('生成失败。语音不存在。')
            voiceUrl = im.data.url
            
            parent_file_dir = mu.file_dir('user', model.userId)
            video_file_dir = parent_file_dir + self.sub_dir
            voice_file_dir = parent_file_dir + bigo.MyDHVoiceControl.inst().sub_dir
            videoModelAction_file_dir = parent_file_dir + bigo.MyDHVideoModelActionControl.inst().sub_dir
            
            # file_dir = mu.file_dir('user', model.userId) + self.sub_dir
            file_name = str(uid.uuid4()) + '.mp4'
            output_dir = video_file_dir + file_name
            
            # 获取视频模型
            im = bigo.MyDHVideoModelControl.inst().get_one_by_id(id=model.myDHVideoModelId, to_dict=True, recurse=True, backrefs=True)
            if im.error:
                return im
            
            if im.data is None:
                return IM(False, '生成失败。视频模型不存在。')
            
            vm = mu.dict_to_obj(im.data)
            # 获取视频模型的动作列表
            actions = vm.myDHVideoModelActions
            if len(actions) == 0:
                return IM(False, '生成失败。视频模型没有动作。')
            
            static = mu.array_find(actions, 'type', 'static')
            if static is None:
                return IM(False, '生成失败。视频模型没有静态动作。')
            static_url = videoModelAction_file_dir + mu.dict_to_obj(static).url
            
            actions1 = mu.array_find_all(actions, 'type', 'action')
            try:
                if len(actions1) == 0:
                    mu.concatVideoWithReverse(static_url, output_dir)
                else:
                    action_urls = []
                    for action in actions1:
                        action_urls.append(videoModelAction_file_dir + mu.dict_to_obj(action).url)
                    mu.genMatchVideo(static_url, action_urls, voice_file_dir + voiceUrl, output_dir)
            except Exception as e:
                return IM(False, '生成失败。' + str(e))
            
            model.videoUrl = file_name
            im = self.update_by_id(model.myDHVideoId, model, fields=['videoUrl'])
            if im.error:
                return im
            
            return im

        return self.run(_do)
    
    def finish(self, model, accessToken):
        """
            修改

        Args:
            model (MyDHVideoModel|dict): 视频
            accessToken (str): 访问令牌
            
        Returns:
            IM：结果
        """
        def _do():
            
            im = IM()
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(model.userId, accessToken)
            if im.error:
                return im
            
            model.isFinish = True
            model.finishTime = datetime.now()
            
            im = self.update_by_id(model.myDHVideoId, model, fields=['isFinish','finishTime','resultUrl'])
            if im.error:
                return im
            
            return im

        return self.run(_do)

    