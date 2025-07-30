import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
import bigOAINet as bigo
from mxupy import IM

import os,json

class MyDHVideoModelControl(mu.EntityXControl):
    class Meta:
        model_class = bigo.MyDHVideoModel
        
    def __init__(self, *args, **kwargs):
        self.sub_dir = 'digitalHuman/videoModel/'
        super().__init__(*args, **kwargs)

    def gen111(self, model, accessToken):
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
            
            file_dir = mu.file_dir('user', model.userId) + 'digitalHuman/'
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(model.userId, accessToken)
            if im.error:
                return im
            
            output_dir = file_dir + str(int(datetime.strptime(model.addTime, "%Y-%m-%dT%H:%M:%S").timestamp())) + '.mp4'
            
            # 获取视频模型
            im = self.get_one_by_id(id=model.myDHVideoModelId, to_dict=True, recurse=True, backrefs=True)
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
            static_url = file_dir + mu.dict_to_obj(static).url
            
            actions1 = mu.array_find_all(actions, 'type', 'action')
            try:
                if len(actions1) == 0:
                    mu.concatVideoWithReverse(static_url, output_dir)
                else:
                    action_urls = []
                    for action in actions1:
                        action_urls.append(file_dir + mu.dict_to_obj(action).url)
                    mu.genMatchVideo(static_url, action_urls, file_dir + '1.mp3', output_dir)
            except Exception as e:
                return IM(False, '生成失败。' + str(e))
                
            return im

        return self.run(_do)
    
    def add1(self, model, userId, accessToken, actions):
        """
            添加

        Args:
            model (MyDHVideoModel): 视频模型
            userId (int): 用户id
            accessToken (str): 访问令牌
            actions (list[MyDHVideoModelAction]): 视频列表，一个视频模型对应多个视频
        Returns:
            IM：结果
        """
        def _do():
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            im = self.add(model)
            if im.error:
                return im
            
            # 添加动作
            if len(actions) == 0:
                return im
            
            mId = im.data.myDHVideoModelId
            for act in actions:
                vd = mu.dict_to_obj(act)
                vd.myDHVideoModelId = mId
                im = bigo.MyDHVideoModelActiveControl.inst().add(vd)
                if im.error:
                    return im
            
            return im

        return self.run(_do)

    def delete1(self, id, userId, accessToken):
        """
            删除

        Args:
            self: 当前对象的引用。
            id (int): 要删除的资源的唯一标识符。
            userId (int): 请求删除操作的用户的唯一标识符。
            accessToken (str): 用于身份验证的访问令牌。

        Returns:
            IM：结果
        """
        def _do():
            im = IM()
            
             # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            cs = [{'myDHVideoModelId': id}, {'userId': userId}]
            
            # 查询是否存在 modelId 这条数据
            im = self.get_one(where=cs)
            if im.error:
                return im
            model = im.data
            
            # 视频是否引用了这个视频模型
            im = bigo.MyDHVideoControl.inst().exists(where=cs)
            if im.error:
                return im
            if im.data:
                return IM(False, '删除失败。已有视频选中了此视频模型。')
            
            # 名片是否引用了这个视频模型
            im = bigo.MyDHCardModelControl.inst().exists(where=cs)
            if im.error:
                return im
            if im.data:
                return IM(False, '删除失败。已有名片选中了此视频模型。')

            # # 收集所有的文件路径
            # filePathList = []
            # filePathList.append(model.thumb)
            
            # filePath = mu.file_dir('user',userId) + '\\'

            # # 数字人名片 静态视频 会生成 m3u8 和 ts 文件
            # videoList = list(model.videoList)

            # for action in videoList:
            #     filePathList.append(action.url)
            #     filePathList.append(action.thumb)

            # filepath, shotname, extension = mu.fileParts(videoList[0].url)
            # dataPath = mu.file_dir('user',userId)
            # filePathList.append(shotname + '.m3u8')
            # for root, dirs, files in os.walk(filePath):
            #     for file in files:
            #         if file.endswith(".ts") and file.startswith(shotname):
            #             filePathList.append(file)

            # # 删除对应视频
            # im = bigo.MyDHVideoControl.inst().delete(where={'myDHVideoModelId': id})
            # if im.error:
            #     return im

            # 删除
            im = self.delete_by_id(id, recursive=True)
            if im.error:
                return im

            # # 去重后删除全部关联文件
            # filePathListSet = list(set(filePathList))
            # mu.removeFileList(filePathListSet,filePath)

        return self.run(_do)
    
    def upload_file(self,file,userId,keep,override):
        # 上传视频
        print('API:upload_file_model_voide called.', userId, keep)
        upath = mu.file_dir('user',userId)
        os.makedirs(upath, exist_ok=True)
        voidePath = upath + '\\' + file.filename
        _, name, ext = mu.fileParts(file.filename)
        if not keep:
            uuid3 = uid.uuid4().hex
            voidePath = upath + '\\' + uuid3 + ext
        try:
            if os.path.exists(voidePath) is False or override:
                # 接受上传的文件，并保存到服务器
                with open(voidePath, "wb") as f:
                    f.write(file.file.read())
                    f.close()

                # 权重和索引文件特殊处理
                # if ext == '.pth':
                #     shutil.copy(voidePath, os.path.join(module_dir, './RVC/assets/weights/'))
                # if ext == '.index':
                #     shutil.copy(voidePath, os.path.join(module_dir, './RVC/assets/indexes/'))
        except Exception as e:
            print('API:upload_file_model_voide error.', str(e))

            return json.dumps({
                'success': False,
                'msg': mu.getErrorStackTrace()
            })
        
        # 检测视频是否符合要求
        success,msg = mu.checkVideo(voidePath)

        if success is False:
            # 失败了删除文件
            mu.removeFile(voidePath)

            return json.dumps({
                'success': False,
                'msg': msg
            })

        width, height = mu.getVideoSize(voidePath)
        if width == 0 and height == 0:
            # 失败了删除文件
            mu.removeFile(voidePath)

            return json.dumps({
                'success': False,
                'msg': "获取视频宽高失败"
            })

        pngPath = upath + '\\' + name + ".png"
        # 获取一帧图像 去除绿幕
        if mu.captureVideoFrame(voidePath, pngPath, 1, True) is False:
            # 失败了删除文件
            mu.removeFile(voidePath)
            mu.removeFile(pngPath)
            return json.dumps({
                'success': False,
                'msg': "获取一帧图像去除绿幕失败"
            })
        
        return json.dumps({
            'success': True,
            "voidePath": voidePath,
            "pngPath": pngPath,
            "width": width,
            "height": height,
        })
