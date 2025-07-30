import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
from .m.models import *
from .MyModelAndVideosControl import *
from mxupy import IM

import os,json

class MyModelControl(mu.EntityXControl):
    class Meta:
        model_class = MyModel

    def upload_file_model_voide(self,file,userId,keep,override):
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

    def add_model_and_action(self,model,userId,accesstoken):
        def _do():
            im = IM()

            modelData = json.loads(model)

            # 创建新数字人模型
            newModel = MyModel.create(
                userId=userId,
                name=modelData['name'],
                thumb=modelData['thumb'],
                width=modelData['width'],
                height=modelData['height'],
            )
            print(newModel)

            for action in modelData['videoList']:
                # 创建新数字人动作
                ModelAndVideos = MyModelAndVideos.create(
                    modelId=newModel.modelId,
                    name=action['name'],
                    url=action['url'],
                    thumb=action['thumb'],
                    type=action['type'],
                )
                # ModelAndVideos.save()
                print(ModelAndVideos)

            im.msg = '恭喜！注册数字人成功。'
            im.data = model_to_dict(newModel, False)
            return im

        return self.run(_do)


    def del_model_and_associated_data(self,modelId,userId,accesstoken):
        def _do():
            im = IM()
            # 查询是否存在 modelId 这条数据
            im1 = self.get_one(where={'modelId': modelId,'userId': userId})
            if im1.success is False:
                return im1
            
            # 查询项目是否引用了这个数字人模型
            project = MyProject.select().where(MyProject.userId == userId,MyProject.modelId == modelId).first()
            if project is not None:
                im.success = False
                im.msg = '已有项目选中了这个数字人模型,无法删除，如以修改请先保存项目'
                return im

            # 查询名片是否引用了这个语音模型
            card = MyCard.select().where(MyCard.userId == userId,MyCard.modelId == modelId).first()
            if card is not None:
                im.success = False
                im.msg = '已有项目选中了这个数字人模型,无法删除，如以修改请先保存名片'
                return im

            model = im1.data
            # 收集所有的文件路径
            filePathList = []
            filePathList.append(model.thumb)
            
            filePath = mu.file_dir('user',userId) + '\\'

            # 数字人名片 静态视频 会生成 m3u8 和 ts 文件
            videoList = list(model.videoList)

            for action in videoList:
                filePathList.append(action.url)
                filePathList.append(action.thumb)

            filepath, shotname, extension = mu.fileParts(videoList[0].url)
            dataPath = mu.file_dir('user',userId)
            filePathList.append(shotname + '.m3u8')
            for root, dirs, files in os.walk(filePath):
                for file in files:
                    if file.endswith(".ts") and file.startswith(shotname):
                        filePathList.append(file)

            # 先删除关联外键数据
            im2 = MyModelAndVideosControl.inst().delete(where={
                'modelId': modelId,
            })
            if im2.success is False:
                return im2

            # 删除自己
            im3 = self.delete_by_id(modelId)
            if im3.success is False:
                return im3

            # 去重后删除全部关联文件
            filePathListSet = list(set(filePathList))
            mu.removeFileList(filePathListSet,filePath)


        return self.run(_do)