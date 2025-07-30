# -*- coding: utf-8 -*-

import time
import sys
import threading
from datetime import datetime
import json
# sys.path.append("../..")
from ...tools.tencent.common import credential
from ...tools.tencent.asr import flash_recognizer

import mxupy as mu
ENGINE_TYPE = "16k_zh"

class ASR(mu.ApiControl):
    
    def __init__(self):
        
        self.APPID = '1300909230'
        self.SECRET_ID = 'AKIDntTPSf2JBFiT72Gqdh19XA8G58OrYXwh'
        self.SECRET_KEY = 'Flx7BTdgd5Sjw4991sgR4bzHUfjrtsnv'
        
    def call(self, filename, userId):
        
        if self.APPID == "":
            print("Please set APPID!")
            exit(0)
        if self.SECRET_ID == "":
            print("Please set SECRET_ID!")
            exit(0)
        if self.SECRET_KEY == "":
            print("Please set SECRET_KEY!")
            exit(0)

        credential_var = credential.Credential(self.SECRET_ID, self.SECRET_KEY)
        # 新建FlashRecognizer，一个recognizer可以执行N次识别请求
        recognizer = flash_recognizer.FlashRecognizer(self.APPID, credential_var)

        # 新建识别请求
        req = flash_recognizer.FlashRecognitionRequest(ENGINE_TYPE)
        req.set_filter_modal(0)
        req.set_filter_punc(0)
        req.set_filter_dirty(0)
        req.set_voice_format("wav")
        req.set_word_info(0)
        req.set_convert_num_mode(1)
        
        # dir = 'D:/server/BigOAINet/userdata/'
        dir = 'D:/AI项目/BIGOAINET/userdata/'
        path = dir + str(userId) + '/' + filename
        # 音频路径
        # audio = "D://AI项目/BIGOAINET/tools/tencent/tencentcloud-speech-sdk-python-master/examples/asr/test.wav"
        # audio = "https://api.bigoainet.com/userdata/2/b47a4476ff914e419bc2af4b40d249f5.mp3"

        with open(path, 'rb') as f:
            #读取音频数据
            data = f.read()
            #执行识别
            resultData = recognizer.recognize(req, data)
            resp = json.loads(resultData)
            request_id = resp["request_id"]
            code = resp["code"]
            if code != 0:
                print("recognize faild! request_id: ", request_id, " code: ", code, ", message: ", resp["message"])
                exit(0)

            print("request_id: ", request_id)
            #一个channl_result对应一个声道的识别结果
            #大多数音频是单声道，对应一个channl_result
            text = ''
            for channl_result in resp["flash_result"]:
                print("channel_id: ", channl_result["channel_id"])
                print(channl_result["text"])
                text += channl_result["text"]
            return text

if __name__=="__main__":
    text = ASR().call('b47a4476ff914e419bc2af4b40d249f5.mp3', 2)
    print(text)