from peewee import *
import base64
import json
import os
import shutil
import mxupy as mu
import subprocess
from mxupy import IM

import uuid as uid
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends
router = APIRouter()

module_dir = os.path.dirname(__file__)

from bigOAINet.tools.aliyun.Qwen import Qwen
client_id = str(uid.uuid4())
qwen = Qwen(history_tokens=0, history_percent=0.8, min_history_length=5, record_error_log=False, client_id=client_id)

class Basics(mu.ApiControl):
    def getCatechismQwen(self,catechismList, question, userId):
        im = IM()
        try:
            messages = [
                {
                    'role': 'system',
                    'content': '你是一个数字人'
                },
                {
                    'role': 'user',
                    'content': '现在有一个问题：\n--------------------\n'+question+'\n--------------------\n对应的问题集为：\n--------------------\n'+catechismList+'--------------------\n请告诉我本问题类似问题集中的哪项，仅返回问题集项编号，如果没有类似问题，返回-1'
                },
            ]
            # print(messages)
            t = qwen.call(messages, '', max_tokens=20, model="qwen-max")

            # 获取序号
            count = int(t['output']['choices'][0]['message']['content'])
            im.data = count
        except Exception as e:
            im.success = False
            im.msg = str(e)

        return im

    def mp4_to_m3u8(self, path, userId,accesstoken):
        im = IM()

        try:
            filepath, shotname, extension = mu.fileParts(path)
            dataPath = mu.file_dir('user',userId)
            m3u8Path = dataPath + "\\" + shotname + '.m3u8'
            if os.path.exists(m3u8Path) is False:
                mu.convertMp4ToM3u8(dataPath + "\\" + path,dataPath)
                mu.convertTSUrlOfM3u8(m3u8Path,"?filename={tsUrl}&userId="+str(userId)+"&type=user&download=false")
        except Exception as e:
            im.success = False
            im.msg = str(e)
        
        return im

    def file_exists(self,file_path, userId):
        im = IM()
        
        upath = mu.file_dir('user',userId)
        path2 = upath + '\\' + os.path.basename(file_path)
        try:
            if os.path.exists(path2):
                # print('exists: ',path2)
                im.data = {
                    'exists': True,
                    "filename": path2
                }
            else:
                # print('not exists: ',path2)
                im.data = {
                    'exists': False,
                    "filename": path2
                }
        except Exception as e:
            im.success = False
            im.msg = str(e)

        return im

    def file_list_exists(self,file_path_list, userId):
        im = IM()

        file_path_list = json.loads(file_path_list)
        
        upath = mu.file_dir('user',userId)+'\\'
        
        exists = []
        not_exists = []
        try:
            exists,not_exists = mu.existsFileList(file_path_list,upath)

            im.data = {
                'existsAll': True,
                "exists": exists,
                "not_exists": not_exists,
            }
        except Exception as e:
            im.success = False
            im.msg = str(e)

        return im

    def hello(self):
        return "HI, I am bigOAINet!"

    def render3(self,userId, catechismId, content, accesstoken):
        im = IM()
        im.data = mu.glb["config"]["schedule"]
        return im

    def get_task_info3(self,userId, catechismId):
        im = IM()
        mu.glb["config"]["schedule"] = mu.glb["config"]["schedule"] + 25
        if mu.glb["config"]["schedule"] == 100:
            mu.glb["config"]["schedule"] = 0
            im.data = {
                'total': mu.glb["config"]["schedule"],
                'url':'WeChat_20230826145531.mp4',
                'finished':True,
            }
        else:
            im.data = {
                'total': mu.glb["config"]["schedule"],
                'finished':False,
            }
        return im

    def train2(self,userId, voiceModelId, audioFile, accesstoken):
        im = IM()

        im.data = mu.glb["config"]["schedule"]
        return im

    def render2(self,userId, voiceModelId, content, accesstoken):
        im = IM()

        im.data = mu.glb["config"]["schedule"]
        return im

    def get_task_info2(self,userId, voiceModelId):
        im = IM()

        mu.glb["config"]["schedule"] = mu.glb["config"]["schedule"] + 25
        if mu.glb["config"]["schedule"] == 100:
            mu.glb["config"]["schedule"] = 0
            im.data = {
                'total':mu.glb["config"]["schedule"],
                'url':'1258a1.mp3',
                'finished':True
            }
        else:
            im.data = {
                'total':mu.glb["config"]["schedule"],
                'finished':False
            }

        return im

    def render(self,userId, projectId,voiceUrl, staticFile, actionFiles, accesstoken):
        im = IM()
        im.data = mu.glb["config"]["schedule"]
        return im

    def get_task_info(self,userId, projectId):
        im = IM()
        mu.glb["config"]["schedule"] = mu.glb["config"]["schedule"] + 25
        if mu.glb["config"]["schedule"] == 100:
            mu.glb["config"]["schedule"] = 0
            im.data = {
                'total': mu.glb["config"]["schedule"],
                'url':'WeChat_20230826145531.mp4',
                'finished':True,
            }
        else:
            im.data = {
                'total': mu.glb["config"]["schedule"],
                'finished':False,
            }
        
        return im