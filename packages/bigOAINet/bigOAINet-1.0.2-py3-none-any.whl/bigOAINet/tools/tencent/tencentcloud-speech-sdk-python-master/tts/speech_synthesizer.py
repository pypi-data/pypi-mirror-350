# -*- coding: utf-8 -*-
import sys
import hmac
import hashlib
import base64
import time
import json
import uuid
import requests
from mxupy import mu


def is_python3():
    if sys.version > '3':
        return True
    return False


_PROTOCOL = "https://"
_HOST = "tts.cloud.tencent.com"
_PATH = "/stream"
_ACTION = "TextToStreamAudio"


class SpeechSynthesisListener:
    '''
    reponse:  
    所有回调均包含session_id字段
    on_message与on_message包含data字段
    on_fail包含Code、Message字段。

    字段名	     类型    说明
    session_id  String  本次请求id
    data        String  语音数据
    Code	    String  错误码
    Message	    String  错误信息
    '''

    def on_message(self, response):
        # a = response
        # print(a)
        pass

    def on_complete(self, response):
        a = response
        # print(a)
        
        with open('F:\\T\\3.mp3', 'wb') as f:
            f.write(response['data'])
        f.close()
        pass

    def on_fail(self, response):
        a = response
        print(a)
        pass


class SpeechSynthesizer:

    def __init__(self, appid, credential, voice_type, listener):
        self.appid = appid
        self.credential = credential
        self.voice_type = voice_type
        self.codec = "mp3"
        self.sample_rate = 16000
        self.volume = 0
        self.speed = 0
        self.listener = listener

    def set_voice_type(self, voice_type):
        self.voice_type = voice_type

    def set_codec(self, codec):
        self.codec = codec

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate

    def set_speed(self, speed):
        self.speed = speed

    def set_volume(self, volume):
        self.volume = volume

    def synthesis(self, text):
        session_id = str(uuid.uuid1())
        params = self.__gen_params(session_id, text)
        signature = self.__gen_signature(params)
        headers = {
            "Content-Type": "application/json",
            "Authorization": str(signature)
        }
        url = _PROTOCOL + _HOST + _PATH
        r = requests.post(url, headers=headers,
                          data=json.dumps(params), stream=True)
        data = None
        response = dict()
        response["session_id"] = session_id
        for chunk in r.iter_content(None):
            if data is None:
                try:
                    rsp = json.loads(chunk)
                    response["Code"] = rsp["Response"]["Error"]["Code"]
                    response["Message"] = rsp["Response"]["Error"]["Message"]
                    self.listener.on_fail(response)
                    return
                except:
                    data = chunk
                    response["data"] = data
                    self.listener.on_message(response)
                    continue
            data = data + chunk
            response["data"] = data
            self.listener.on_message(response)
        response["data"] = data
        self.listener.on_complete(response)

    def __gen_signature(self, params):
        sort_dict = sorted(params.keys())
        sign_str = "POST" + _HOST + _PATH + "?"
        for key in sort_dict:
            sign_str = sign_str + key + "=" + str(params[key]) + '&'
        sign_str = sign_str[:-1]
        hmacstr = hmac.new(self.credential.secret_key.encode('utf-8'),
                           sign_str.encode('utf-8'), hashlib.sha1).digest()
        s = base64.b64encode(hmacstr)
        s = s.decode('utf-8')
        return s

    def __sign(self, signstr, secret_key):
        hmacstr = hmac.new(secret_key.encode('utf-8'),
                           signstr.encode('utf-8'), hashlib.sha1).digest()
        s = base64.b64encode(hmacstr)
        s = s.decode('utf-8')
        return s

    def __gen_params(self, session_id, text):
        params = dict()
        params['Action'] = _ACTION
        params['AppId'] = int(self.appid)
        params['SecretId'] = self.credential.secret_id
        params['ModelType'] = 1
        params['VoiceType'] = self.voice_type
        params['Codec'] = self.codec
        params['SampleRate'] = self.sample_rate
        params['Speed'] = self.speed
        params['Volume'] = self.volume
        params['SessionId'] = session_id
        params['Text'] = text

        timestamp = int(time.time())
        params['Timestamp'] = timestamp
        params['Expired'] = timestamp + 24 * 60 * 60
        return params

# self.secret_id = 'AKIDntTPSf2JBFiT72Gqdh19XA8G58OrYXwh'
# self.secret_key = 'Flx7BTdgd5Sjw4991sgR4bzHUfjrtsnv'
# appid, credential, voice_type, listener

# 1300909230
# AKIDntTPSf2JBFiT72Gqdh19XA8G58OrYXwh
credential = mu.dict_to_obj({'secret_id':'AKIDntTPSf2JBFiT72Gqdh19XA8G58OrYXwh','secret_key':'Flx7BTdgd5Sjw4991sgR4bzHUfjrtsnv'})
tts = SpeechSynthesizer('1300909230', credential, 101001, SpeechSynthesisListener())
# a = tts.synthesis('涵盖了所有涉及合成有机化学领域，容翔实地记载了实验流程，完整地描述了所有重要新产品，提供了可靠的研究成果和科学原始数据。')
a = tts.synthesis('经过近一年的需求调研和规划，贝一科技新的业务线”点未云游“正式提上实现阶段议程。 2019年5月18日进行了第一次点未云游戏项目参与全员会议。 会中，点未云游创始人我司CTO，将点未云游这个新项目的整个心路历程、调研结果、未来展望')
print(a)
