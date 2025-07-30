# -*- coding: utf-8 -*-
# 引用 SDK
import wave
import time
import uuid as uid
from mxupy import mu

from .common import credential
from .common import speech_synthesizer_ws as ssws
from .common.log import logger

class MySpeechSynthesisListener(ssws.SpeechSynthesisListener):
    
    def __init__(self, id, codec, sample_rate):
        self.start_time = time.time()
        self.id = id
        self.codec = codec.lower()
        self.sample_rate = sample_rate

        self.audio_file = ''
        self.error_code = ''
        self.error_msg = ''
        self.audio_data = bytes()
    
    def set_audio_file(self, filename):
        self.audio_file = filename

    def on_synthesis_start(self, session_id):
        '''
        session_id: 请求session id，类型字符串
        '''
        super().on_synthesis_start(session_id)
        
        # TODO 合成开始，添加业务逻辑
        if not self.audio_file:
            self.audio_file = "speech_synthesis_output." + self.codec
        self.audio_data = bytes()

    def on_synthesis_end(self):
        super().on_synthesis_end()

        # # TODO 合成结束，添加业务逻辑
        # logger.info("write audio file, path={}, size={}".format(
        #     self.audio_file, len(self.audio_data)
        # ))
        
        if self.codec in ["pcm", "wav"]:
            # wav_fp = wave.open(self.audio_file + ".wav", "wb")
            wav_fp = wave.open(self.audio_file, "wb")
            wav_fp.setnchannels(1)
            wav_fp.setsampwidth(2)
            wav_fp.setframerate(self.sample_rate)
            wav_fp.writeframes(self.audio_data)
            wav_fp.close()
        elif self.codec == "mp3":
            fp = open(self.audio_file, "wb")
            fp.write(self.audio_data)
            fp.close()
        # else:
        #     logger.info("codec {}: sdk NOT implemented, please save the file yourself".format(
        #         self.codec
        #     ))

    def on_audio_result(self, audio_bytes):
        '''
        audio_bytes: 二进制音频，类型 bytes
        '''
        super().on_audio_result(audio_bytes)
        
        # TODO 接收到二进制音频数据，添加实时播放或保存逻辑
        self.audio_data += audio_bytes

    def on_text_result(self, response):
        '''
        response: 文本结果，类型 dict，如下
        字段名       类型         说明
        code        int         错误码（无需处理，SpeechSynthesizer中已解析，错误消息路由至 on_synthesis_fail）
        message     string      错误信息
        session_id  string      回显客户端传入的 session id
        request_id  string      请求 id，区分不同合成请求，一次 websocket 通信中，该字段相同
        message_id  string      消息 id，区分不同 websocket 消息
        final       bool        合成是否完成（无需处理，SpeechSynthesizer中已解析）
        result      Result      文本结果结构体

        Result 结构体
        字段名       类型                说明
        subtitles   array of Subtitle  时间戳数组
        
        Subtitle 结构体
        字段名       类型     说明
        Text        string  合成文本
        BeginTime   int     开始时间戳
        EndTime     int     结束时间戳
        BeginIndex  int     开始索引
        EndIndex    int     结束索引
        Phoneme     string  音素
        '''
        super().on_text_result(response)

        # TODO 接收到文本数据，添加业务逻辑
        result = response["result"]
        subtitles = []
        if "subtitles" in result and len(result["subtitles"]) > 0:
            subtitles = result["subtitles"]

    def on_synthesis_fail(self, response):
        '''
        response: 文本结果，类型 dict，如下
        字段名 类型
        code        int         错误码
        message     string      错误信息
        '''
        super().on_synthesis_fail(response)
        self.error_code =  response["code"]
        self.error_msg = response["message"]
        
class TTS(mu.ApiControl):

    def __init__(self):
        
        self.appid = '1300909230'
        self.secret_id = 'AKIDntTPSf2JBFiT72Gqdh19XA8G58OrYXwh'
        self.secret_key = 'Flx7BTdgd5Sjw4991sgR4bzHUfjrtsnv'
        
    def run(self):
        listener = MySpeechSynthesisListener(0, self.codec, self.sample_rate)
        credential_var = credential.Credential(self.secret_id, self.secret_key)
        synthesizer = ssws.SpeechSynthesizer(self.appid, credential_var, listener)
        
        
        listener.set_audio_file(self.path)
        
        synthesizer.set_text(self.text)
        synthesizer.set_voice_type(self.voice_type)
        synthesizer.set_codec(self.codec)
        synthesizer.set_sample_rate(self.sample_rate)
        synthesizer.set_enable_subtitle(self.enable_subtitle)
        
        synthesizer.start()
        synthesizer.wait()

        # logger.info("process done")
        
        return listener.error_code, listener.error_msg
    
    def call(self, text, user_id, voice_type=501006, codec='mp3', sample_rate = 16000, volume=0, speed=0, log_path=''):
        
        codec = codec if codec != 'wav' else 'pcm'
        ext = '.wav' if codec != 'mp3' else '.mp3'
        fn = str(int(time.time())) + ext
        path = mu.file_dir('user', user_id) + '\\' + fn
        
        self.text = text
        self.path = path
        self.voice_type = voice_type
        self.codec = codec
        self.sample_rate = sample_rate
        self.volume = volume
        self.speed = speed
        self.enable_subtitle = False
        
        code, msg = self.run()
        if code:
            return mu.IM(False, msg, fn, code, 'TTS')
        return mu.IM(True, '', fn, 200, 'TTS')
    
    # def call(self, text, path, voice_type=501006, codec='mp3', sample_rate = 16000, volume=0, speed=0, log_path=''):
        
    #     self.text = text
    #     self.path = path
    #     self.voice_type = voice_type
    #     self.codec = codec
    #     self.sample_rate = sample_rate
    #     self.volume = volume
    #     self.speed = speed
    #     self.enable_subtitle = False
        
    #     self.run()
        
    #     return mu.IM(True, '', path, 200, 'TTS')
        
if __name__ == "__main__":
    
    text = '经过近一年的需求调研和规划，贝一科技新的业务线”点未云游“正式提上实现阶段议程。'
    im = TTS().call(text, 1)
    print(im)
        
        