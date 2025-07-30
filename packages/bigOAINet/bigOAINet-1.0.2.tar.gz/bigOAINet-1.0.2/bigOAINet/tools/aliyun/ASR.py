import re
import json
from http import HTTPStatus
from urllib import request
from mxupy import ApiControl
import mxupy as mu

class ASR(ApiControl):
    
    '''
    
        空间: tools.aliyun.ASR
        名称：语音识别
        参考网址: https://help.aliyun.com/zh/model-studio/developer-reference/quick-start-sensevoice?spm=a2c4g.11186623.0.0.78f56499zQ4wJV
        语音转文字(Automatic Speech Recognition)
        
        SenseVoice
        语言列表: https://help.aliyun.com/zh/model-studio/developer-reference/supported-languages?spm=a2c4g.11186623.0.0.642314fc4G2mNg
        zh:中文 en:英文 yue:粤语 ja:日语 ko:韩语 ru:俄语 fr:法语 it:意大利语 de:德语 es:西班牙语
        支持的文件格式
        aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv

    '''
    def __init__(self):
        ''' 初始化
        Args:
            language_code (str): 指定识别语音中语言代码。sensevoice-v1模型只支持配置一个语种。默认使用“auto”自动检测语种。
            zh:中文 en:英文 yue:粤语 ja:日语 ko:韩语 ru:俄语 fr:法语 it:意大利语 de:德语 es:西班牙语
        Returns:
            无
        '''
        import dashscope
        # setx ALIYUN_API_KEY 你的APIKey 设置后需要重启
        # self.api_key = os.getenv('ALIYUN_API_KEY')
        self.api_key = 'sk-879c45ea8b464c94a5fc4316652315e8'
        dashscope.api_key = self.api_key
        
    def parse_sensevoice_result(self, data, keep_trans=True, keep_emotions=True, keep_events=True):
        '''
            解析 sensevoice 识别结果
            keep_trans (bool): 是否保留转写文本
            keep_emotions (bool): 是否保留情感标签
            keep_events (bool): 是否保留事件标签
        '''
        # 定义要保留的标签（表情、事件）
        emotion_list = ['NEUTRAL', 'HAPPY', 'ANGRY', 'SAD']
        event_list = ['Speech', 'Applause', 'BGM', 'Laughter']

        # 所有支持的标签
        all_tags = ['Speech', 'Applause', 'BGM', 'Laughter', 'NEUTRAL', 'HAPPY', 'ANGRY', 'SAD', 'SPECIAL_TOKEN_1']
        
        tags_to_cleanup = []
        for tag in all_tags:
            tags_to_cleanup.append(f'<|{tag}|> ')
            tags_to_cleanup.append(f'<|/{tag}|>')
            tags_to_cleanup.append(f'<|{tag}|>')

        def get_clean_text(text: str):
            for tag in tags_to_cleanup:
                text = text.replace(tag, '')
            pattern = r"\s{2,}"
            text = re.sub(pattern, " ", text).strip()
            return text

        for item in data['transcripts']:
            for sentence in item['sentences']:
                if keep_emotions:
                    # 提取 emotion
                    emotions_pattern = r'<\|(' + '|'.join(emotion_list) + r')\|>'
                    emotions = re.findall(emotions_pattern, sentence['text'])
                    sentence['emotion'] = list(set(emotions))
                    if not sentence['emotion']:
                        sentence.pop('emotion', None)

                if keep_events:
                    # 提取 event
                    events_pattern = r'<\|(' + '|'.join(event_list) + r')\|>'
                    events = re.findall(events_pattern, sentence['text'])
                    sentence['event'] = list(set(events))
                    if not sentence['event']:
                        sentence.pop('event', None)

                if keep_trans:
                    # 提取纯文本
                    sentence['text'] = get_clean_text(sentence['text'])
                else:
                    sentence.pop('text', None)

            if keep_trans:
                item['text'] = get_clean_text(item['text'])
            else:
                item.pop('text', None)
                
            item['sentences'] = list(filter(lambda x: 'text' in x or 'emotion' in x or 'event' in x, item['sentences']))
        
        return data
    
    def call(self, file_urls, model='sensevoice-v1', channel_id=[0], disfluency_removal_enabled=False, language_code='auto'):
        """ 
            异步调用，可以同时传多个文件

        Args:
            file_urls (str|list[str]): 文件集，必须是网络路径，格式必须为下列格式的一种
                ['aac', 'amr', 'avi', 'flac', 'flv', 'm4a', 'mkv', 'mov', 'mp3', 'mp4', 'mpeg', 'ogg', 'opus', 'wav', 'webm', 'wma', 'wmv']
            model (str): 模型名
            channel_id (list): 通道
            disfluency_removal_enabled (bool): 过滤语气词，默认关闭。true：表示不关闭
            language_code (str): 语言码

        Returns:
            str: 文本
        """
        import dashscope
        
        im = mu.IM()
        
        if not file_urls:
            im.success = False
            im.msg = '路径不能为空。'
            return im
        
        if not isinstance(file_urls, list):
            file_urls = [file_urls]
        
        fus = []
        for fu in file_urls:
            if not fu.startswith('http'):
                im.success = False
                im.msg = '文件必须是网络路径。'
                return im
            
            fus.append(fu.replace('https://api.bigoainet.com/', 'http://210.16.189.23:8089/'))
            
        task_response = dashscope.audio.asr.Transcription.async_call(
            api_key=self.api_key,
            model=model,
            file_urls=fus,
            language_hints=[language_code],
            channel_id=channel_id,
            disfluency_removal_enabled=disfluency_removal_enabled,
        )
        transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
        texts = []
        if transcribe_response.status_code == HTTPStatus.OK:
            for transcription in transcribe_response.output['results']:
                if transcription['subtask_status'] == 'FAILED':
                    print('Error: ', transcription['code'], transcription['message'])
                    return mu.IM(False, transcription['code'] + ' ' + transcription['message'], None, 500)
                else:
                    url = transcription['transcription_url']
                    result = json.loads(request.urlopen(url).read().decode('utf8'))
                    data = self.parse_sensevoice_result(result, keep_trans=True, keep_emotions=False, keep_events=False)
                    texts.append(data['transcripts'][0]['text'])
                # print(self.parse_sensevoice_result(result, keep_trans=True, keep_emotions=False, keep_events=False))
                # print(json.dumps(self.parse_sensevoice_result(result, keep_trans=True, keep_emotions=False, keep_events=False), indent=4, ensure_ascii=False))
        else:
            print('Error: ', transcribe_response.output.message)
            im.success = False
            im.msg = transcribe_response.output.message
            return im
        
        return '\n'.join(texts)
    
    @staticmethod
    def init(model='sensevoice-v1', language_code='auto'):
        print(model, language_code)
        
if __name__ == '__main__':
    # import inspect
    
    # clazz = ASR
    
    # method = getattr(clazz(), 'init', None)
    # if inspect.ismethod(method):
    #     print('true')
    # else:
    #     print('false')
    # method = getattr(clazz(), 'async_call', None)
    # if inspect.ismethod(method):
    #     print('true')
    # else:
    #     print('false')
    
    # asr_instance = clazz()
    
    # method = getattr(clazz(), 'async_call', None)
    # print(inspect.ismethod(method))
    # print(inspect.ismethod(asr_instance.async_call))
    # print(hasattr(method, '__self__'))
    # print(hasattr(asr_instance.async_call, '__self__'))
    
    # method = getattr(clazz(), 'init', None)
    # print(inspect.ismethod(method))
    # print(inspect.ismethod(asr_instance.init))
    # print(hasattr(method, '__self__'))
    # print(hasattr(asr_instance.init, '__self__'))
    
    # print(inspect.ismethod(asr_instance.init))
    # print(hasattr(asr_instance.init, '__self__'))
    
    # print(inspect.ismethod(asr_instance.async_call))
    # print(hasattr(asr_instance.async_call, '__self__'))
    
    
    # method = getattr(clazz(), 'init', None)
    # if inspect.isfunction(method) and inspect.ismethod(method):
    #     print('true')
    # else:
    #     print('false')
    # method = getattr(clazz(), 'async_call', None)
    # if inspect.isfunction(method) and inspect.ismethod(method):
    #     print('true')
    # else:
    #     print('false')
    
    # asr_instance = ASR()
    # print(inspect.ismethod(asr_instance.async_call))  # 应该返回 True
    # print(inspect.ismethod(asr_instance.init))        # 应该返回 False，因为 init 是静态方法

    # # 检查 async_call 是否是实例方法
    # if inspect.ismethod(ASR.async_call):
    #     print("async_call is an instance method.")
    # else:
    #     print("async_call is not an instance method.")

    # # 检查 init 是否是静态方法
    # if inspect.isfunction(ASR.init) and not inspect.ismethod(ASR.init):
    #     print("init is a static method.")
    # else:
    #     print("init is not a static method.")
    
    
    # tts = ASR('sensevoice-v1')
    
    # 文件必须是网络路径
    # text = tts.async_call('http://www.xtbeiyi.com/fy/1.wav')
    # text = tts.async_call('http://www.xtbeiyi.com/fy/1.mp3')
    
    # 一次可以同时传多个文件
    # text = ASR().call(['http://www.xtbeiyi.com/fy/1.wav', 'http://www.xtbeiyi.com/fy/1.mp3'], model='sensevoice-v1')
    # text = ASR().call(['http://www.xtbeiyi.com/fy/1.wav'], model='sensevoice-v1')
    # text = ASR().call(['https://api.bigoainet.com/file?userId=2&type=user&download=true&filename=b47a4476ff914e419bc2af4b40d249f5.mp3'], model='sensevoice-v1')
    # text = ASR().call(['https://api.bigoainet.com/file/?userId=6&type=user&download=false&filename=1.mp3'], model='sensevoice-v1')
    # text = ASR().call(['http://www.xtbeiyi.com/fy/b47a4476ff914e419bc2af4b40d249f5.mp3?a=b'], model='sensevoice-v1')
    
    # text = ASR().call(['http://www.xtbeiyi.com/fy/b47a4476ff914e419bc2af4b40d2491f5.mp3?userId=2&filename=b47a4476ff914e419bc2af4b40d249f5.mp3'], model='sensevoice-v1')
    # text = ASR().call(['https://www.bigoainet.com/userdata/2/b47a4476ff914e419bc2af4b40d249f5.mp3'], model='sensevoice-v1')
    # text = ASR().call(['https://www.bigoainet.com/file/?filename=b47a4476ff914e419bc2af4b40d249f5.mp3&userId=2'], model='sensevoice-v1')
    # text = ASR().call(['http://8.148.22.143/file/?filename=1732334861.mp3&userId=1&download=false'], model='sensevoice-v1')
    
    # text = ASR().call(['http://210.16.189.23:8089/file/?filename=b47a4476ff914e419bc2af4b40d249f5.mp3&userId=2'], model='sensevoice-v1')
    text = ASR().call(['http://file.bigoainet.com:8081?filename=b47a4476ff914e419bc2af4b40d249f5.mp3&userId=2'], model='sensevoice-v1')
    # http://file.bigoainet.com/?userId=...............
    print(text)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    