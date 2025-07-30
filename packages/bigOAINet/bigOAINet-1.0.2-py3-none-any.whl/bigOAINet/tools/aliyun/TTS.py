import os
import time
from mxupy import ApiControl

class TTS(ApiControl):
    """
        空间: tools.aliyun.TTS
        名称：语音合成（文字转语音）
        参考网址: https://help.aliyun.com/zh/dashscope/developer-reference/sambert-speech-synthesis/?spm=a2c4g.11186623.0.0.3fd544b7UHpj64
        # 语音转文本（Text-to-Speech）
        
        sambert
        模型列表: https://help.aliyun.com/zh/model-studio/developer-reference/model-list?spm=a2c4g.11186623.0.0.10851d1cVbLRRJ
        | **音色**       | **model参数**          | **特色**     | **语言**  | **默认采样率(Hz)** | **更新日期** |
        | -------------- | ---------------------- | ------------ | --------- | ------------------ | ------------ |
        | 知厨           | sambert-zhichu-v1      | 舌尖男声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知薇           | sambert-zhiwei-v1      | 萝莉女声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知祥           | sambert-zhixiang-v1    | 磁性男声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知德           | sambert-zhide-v1       | 新闻男声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知佳           | sambert-zhijia-v1      | 标准女声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知楠           | sambert-zhinan-v1      | 广告男声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知琪           | sambert-zhiqi-v1       | 温柔女声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知倩           | sambert-zhiqian-v1     | 资讯女声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知茹           | sambert-zhiru-v1       | 新闻女声     | 中文+英文 | 48k                | 2023.6.20    |
        | 知妙（多情感） | sambert-zhimiao-emo-v1 | 多种情感女声 | 中文+英文 | 16k                | 2023.6.20    |
        | 知达           | sambert-zhida-v1       | 标准男声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知飞           | sambert-zhifei-v1      | 激昂解说     | 中文+英文 | 16k                | 2023.6.20    |
        | 知柜           | sambert-zhigui-v1      | 直播女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知浩           | sambert-zhihao-v1      | 咨询男声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知婧           | sambert-zhijing-v1     | 严厉女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知伦           | sambert-zhilun-v1      | 悬疑解说     | 中文+英文 | 16k                | 2023.6.20    |
        | 知猫           | sambert-zhimao-v1      | 直播女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知茗           | sambert-zhiming-v1     | 诙谐男声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知墨           | sambert-zhimo-v1       | 情感男声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知娜           | sambert-zhina-v1       | 浙普女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知树           | sambert-zhishu-v1      | 资讯男声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知硕           | sambert-zhishuo-v1     | 自然男声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知莎           | sambert-zhistella-v1   | 知性女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知婷           | sambert-zhiting-v1     | 电台女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知笑           | sambert-zhixiao-v1     | 资讯女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知雅           | sambert-zhiya-v1       | 严厉女声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知晔           | sambert-zhiye-v1       | 青年男声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知颖           | sambert-zhiying-v1     | 软萌童声     | 中文+英文 | 16k                | 2023.6.20    |
        | 知媛           | sambert-zhiyuan-v1     | 知心姐姐     | 中文+英文 | 16k                | 2023.6.20    |
        | 知悦           | sambert-zhiyue-v1      | 温柔女声     | 中文+英文 | 16k                | 2023.6.20    |
        | Camila         | sambert-camila-v1      | 西班牙语女声 | 西班牙语  | 16k                | 2023.6.20    |
        | Perla          | sambert-perla-v1       | 意大利语女声 | 意大利语  | 16k                | 2023.6.20    |
        | Indah          | sambert-indah-v1       | 印尼语女声   | 印尼语    | 16k                | 2023.6.20    |
        | Clara          | sambert-clara-v1       | 法语女声     | 法语      | 16k                | 2023.6.20    |
        | Hanna          | sambert-hanna-v1       | 德语女声     | 德语      | 16k                | 2023.6.20    |
        | Beth           | sambert-beth-v1        | 咨询女声     | 美式英文  | 16k                | 2023.6.20    |
        | Betty          | sambert-betty-v1       | 客服女声     | 美式英文  | 16k                | 2023.6.20    |
        | Cally          | sambert-cally-v1       | 自然女声     | 美式英文  | 16k                | 2023.6.20    |
        | Cindy          | sambert-cindy-v1       | 对话女声     | 美式英文  | 16k                | 2023.6.20    |
        | Eva            | sambert-eva-v1         | 陪伴女声     | 美式英文  | 16k                | 2023.6.20    |
        | Donna          | sambert-donna-v1       | 教育女声     | 美式英文  | 16k                | 2023.6.20    |
        | Brian          | sambert-brian-v1       | 客服男声     | 美式英文  | 16k                | 2023.6.20    |
        | Waan           | sambert-waan-v1        | 泰语女声     | 泰语      | 16k                | 2023.6.20    |
        
        音色列表: https://help.aliyun.com/zh/model-studio/developer-reference/timbre-list?spm=a2c4g.11186623.0.0.2004621ayEqyNE
        当 model 为 cosyvoice-v1 的时候， 可指定下列 voice 参数：
        | **音色** | **voice 参数** | **适用场景**                                                 | **语言**     | **默认采样率（Hz）** | **默认音频格式** |
        | -------- | -------------- | ------------------------------------------------------------ | ------------ | -------------------- | ---------------- |
        | 龙婉      | longwan        | 语音助手、导航播报、聊天数字人                                | 中文普通话 | 22050                    | mp3  |
        | 龙橙      | longcheng      | 语音助手、导航播报、聊天数字人                                | 中文普通话 | 22050                    | mp3  |
        | 龙华      | longhua        | 语音助手、导航播报、聊天数字人                                | 中文普通话 | 22050                    | mp3  |
        | 龙小淳   | longxiaochun   | 语音助手、导航播报、聊天数字人                               | 中文+英文    | 22050                | mp3              |
        | 龙小夏   | longxiaoxia    | 语音助手、聊天数字人                                         | 中文         | 22050                | mp3              |
        | 龙小诚   | longxiaocheng  | 语音助手、导航播报、聊天数字人                               | 中文+英文    | 22050                | mp3              |
        | 龙小白   | longxiaobai    | 聊天数字人、有声书、语音助手                                 | 中文         | 22050                | mp3              |
        | 龙老铁   | longlaotie     | 新闻播报、有声书、语音助手、直播带货、导航播报               | 中文东北口音 | 22050                | mp3              |
        | 龙书     | longshu        | 有声书、语音助手、导航播报、新闻播报、智能客服               | 中文         | 22050                | mp3              |
        | 龙硕     | longshuo       | 语音助手、导航播报、新闻播报、客服催收                       | 中文         | 22050                | mp3              |
        | 龙婧     | longjing       | 语音助手、导航播报、新闻播报、客服催收                       | 中文         | 22050                | mp3              |
        | 龙妙     | longmiao       | 客服催收、导航播报、有声书、语音助手                         | 中文         | 22050                | mp3              |
        | 龙悦     | longyue        | 语音助手、诗词朗诵、有声书朗读、导航播报、新闻播报、客服催收 | 中文         | 22050                | mp3              |
        | 龙媛     | longyuan       | 有声书、语音助手、聊天数字人                                 | 中文         | 22050                | mp3              |
        | 龙飞     | longfei        | 会议播报、新闻播报、有声书                                   | 中文         | 22050                | mp3              |
        | 龙杰力豆 | longjielidou   | 新闻播报、有声书、聊天助手                                   | 中文+英文    | 22050                | mp3              |
        | 龙彤     | longtong       | 有声书、导航播报、聊天数字人                                 | 中文         | 22050                | mp3              |
        | 龙祥     | longxiang      | 新闻播报、有声书、导航播报                                   | 中文         | 22050                | mp3              |
        | Stella   | loongstella    | 语音助手、直播带货、导航播报、客服催收、有声书               | 中文+英文    | 22050                | mp3              |
        | Bella    | loongbella     | 语音助手、客服催收、新闻播报、导航播报                       | 中文         | 22050                | mp3              |

    """
    def __init__(self, model='', voice=None, format='mp3', volume=50, speech_rate=1.0, pitch_rate=1.0, word_timestamp_enabled=False, phoneme_timestamp_enabled=False):
        """ 初始化

        Args:
            model (str): 模型名
            voice (str): 音色名， 当模型为 cosyvoice-v1 的 时候，此参数才有意义
            format (str|obj): 编码格式，支持pcm/wav/mp3格式。当模型为 cosyvoice-v1 的 时候，此参数为下列的一种
                WAV_8000HZ_MONO_16BIT
                WAV_16000HZ_MONO_16BIT
                WAV_22050HZ_MONO_16BIT
                WAV_24000HZ_MONO_16BIT
                WAV_44100HZ_MONO_16BIT
                WAV_48000HZ_MONO_16BIT
                MP3_8000HZ_MONO_128KBPS
                MP3_16000HZ_MONO_128KBPS
                MP3_22050HZ_MONO_256KBPS
                MP3_24000HZ_MONO_256KBPS
                MP3_44100HZ_MONO_256KBPS
                MP3_48000HZ_MONO_256KBPS
                PCM_8000HZ_MONO_16BIT
                PCM_16000HZ_MONO_16BIT
                PCM_22050HZ_MONO_16BIT
                PCM_24000HZ_MONO_16BIT
                PCM_44100HZ_MONO_16BIT
                PCM_48000HZ_MONO_16BIT
            volume (int): 音量，取值范围是0~100
            speech_rate (float): 语速，取值范围0.5~2
            pitch_rate (double): 语调，取值范围：0.5~2。
            word_timestamp_enabled (bool): 是否开启字级别时间戳。
            phoneme_timestamp_enabled (bool): 是否在开启字级别时间戳的基础上，显示音素时间戳。
            
        Returns:
            无
        """
        # setx ALIYUN_API_KEY 你的APIKey 设置后需要重启
        self.api_key = 'sk-879c45ea8b464c94a5fc4316652315e8'
        # self.api_key = os.getenv('ALIYUN_API_KEY')
        import dashscope
        dashscope.api_key = self.api_key
        
        self.model = model
        self.voice = voice if model == 'cosyvoice-v1' else None
        
        self.format = self.getFormat(format.upper()) if model == 'cosyvoice-v1' else format.lower()
        
        self.sample_rate = self.getSampleRate(model)
        
        self.volume = volume
        self.speech_rate = speech_rate
        self.pitch_rate = pitch_rate
        
        self.word_timestamp_enabled = word_timestamp_enabled
        self.phoneme_timestamp_enabled = phoneme_timestamp_enabled
        
        self.synthesizer = None
    
    def getValue(self, name, value):
        """ 如果函数中指定了属性值，则直接用此属性值，否则用类实例化时指定的默认值
            Args:
                format (str): 格式：如 WAV_8000HZ_MONO_16BIT
            Returns:
                音频格式: 如 AudioFormat.WAV_8000HZ_MONO_16BIT
        """
        return getattr(self, name) if value == None else value
    
    def getSampleRate(self, model):
        """ 通过模型名 获取采样率
            Args:
                model (str): 模型名
            Returns:
                sample_rate (int): 如 48000
        """
        models = [
            'sambert-zhichu-v1',
            'sambert-zhiwei-v1',
            'sambert-zhixiang-v1',
            'sambert-zhide-v1',
            'sambert-zhijia-v1',
            'sambert-zhinan-v1',
            'sambert-zhiqi-v1',
            'sambert-zhiqian-v1',
            'sambert-zhiru-v1',
        ]
        return 48000 if model in models else 16000
        
    def getFormat(self, format):
        """ 通过字符串得到音频对应的输出格式
            Args:
                format (str): 格式：如 WAV_8000HZ_MONO_16BIT
            Returns:
                音频格式: 如 AudioFormat.WAV_8000HZ_MONO_16BIT
        """
        from dashscope.audio.tts_v2 import AudioFormat
        
        if format == None: 
            return AudioFormat.DEFAULT
        
        if not isinstance(format, str):
            return format
        
        audio_format_map = {
            'WAV_8000HZ_MONO_16BIT': AudioFormat.WAV_8000HZ_MONO_16BIT,
            'WAV_16000HZ_MONO_16BIT': AudioFormat.WAV_16000HZ_MONO_16BIT,
            'WAV_22050HZ_MONO_16BIT': AudioFormat.WAV_22050HZ_MONO_16BIT,
            'WAV_24000HZ_MONO_16BIT': AudioFormat.WAV_24000HZ_MONO_16BIT,
            'WAV_44100HZ_MONO_16BIT': AudioFormat.WAV_44100HZ_MONO_16BIT,
            'WAV_48000HZ_MONO_16BIT': AudioFormat.WAV_48000HZ_MONO_16BIT,
            'MP3_8000HZ_MONO_128KBPS': AudioFormat.MP3_8000HZ_MONO_128KBPS,
            'MP3_16000HZ_MONO_128KBPS': AudioFormat.MP3_16000HZ_MONO_128KBPS,
            'MP3_22050HZ_MONO_256KBPS': AudioFormat.MP3_22050HZ_MONO_256KBPS,
            'MP3_24000HZ_MONO_256KBPS': AudioFormat.MP3_24000HZ_MONO_256KBPS,
            'MP3_44100HZ_MONO_256KBPS': AudioFormat.MP3_44100HZ_MONO_256KBPS,
            'MP3_48000HZ_MONO_256KBPS': AudioFormat.MP3_48000HZ_MONO_256KBPS,
            'PCM_8000HZ_MONO_16BIT': AudioFormat.PCM_8000HZ_MONO_16BIT,
            'PCM_16000HZ_MONO_16BIT': AudioFormat.PCM_16000HZ_MONO_16BIT,
            'PCM_22050HZ_MONO_16BIT': AudioFormat.PCM_22050HZ_MONO_16BIT,
            'PCM_24000HZ_MONO_16BIT': AudioFormat.PCM_24000HZ_MONO_16BIT,
            'PCM_44100HZ_MONO_16BIT': AudioFormat.PCM_44100HZ_MONO_16BIT,
            'PCM_48000HZ_MONO_16BIT': AudioFormat.PCM_48000HZ_MONO_16BIT,
        }
        
        return audio_format_map.get(format, AudioFormat.DEFAULT)
        
        # if format == 'WAV_8000HZ_MONO_16BIT': return AudioFormat.WAV_8000HZ_MONO_16BIT
        # elif format == 'WAV_16000HZ_MONO_16BIT': return AudioFormat.WAV_16000HZ_MONO_16BIT
        # elif format == 'WAV_22050HZ_MONO_16BIT': return AudioFormat.WAV_22050HZ_MONO_16BIT
        # elif format == 'WAV_24000HZ_MONO_16BIT': return AudioFormat.WAV_24000HZ_MONO_16BIT
        # elif format == 'WAV_44100HZ_MONO_16BIT': return AudioFormat.WAV_44100HZ_MONO_16BIT
        # elif format == 'WAV_48000HZ_MONO_16BIT': return AudioFormat.WAV_48000HZ_MONO_16BIT
        # elif format == 'MP3_8000HZ_MONO_128KBPS': return AudioFormat.MP3_8000HZ_MONO_128KBPS
        # elif format == 'MP3_16000HZ_MONO_128KBPS': return AudioFormat.MP3_16000HZ_MONO_128KBPS
        # elif format == 'MP3_22050HZ_MONO_256KBPS': return AudioFormat.MP3_22050HZ_MONO_256KBPS
        # elif format == 'MP3_24000HZ_MONO_256KBPS': return AudioFormat.MP3_24000HZ_MONO_256KBPS
        # elif format == 'MP3_44100HZ_MONO_256KBPS': return AudioFormat.MP3_44100HZ_MONO_256KBPS
        # elif format == 'MP3_48000HZ_MONO_256KBPS': return AudioFormat.MP3_48000HZ_MONO_256KBPS
        # elif format == 'PCM_8000HZ_MONO_16BIT': return AudioFormat.PCM_8000HZ_MONO_16BIT
        # elif format == 'PCM_16000HZ_MONO_16BIT': return AudioFormat.PCM_16000HZ_MONO_16BIT
        # elif format == 'PCM_22050HZ_MONO_16BIT': return AudioFormat.PCM_22050HZ_MONO_16BIT
        # elif format == 'PCM_24000HZ_MONO_16BIT': return AudioFormat.PCM_24000HZ_MONO_16BIT
        # elif format == 'PCM_44100HZ_MONO_16BIT': return AudioFormat.PCM_44100HZ_MONO_16BIT
        # elif format == 'PCM_48000HZ_MONO_16BIT': return AudioFormat.PCM_48000HZ_MONO_16BIT
        # return AudioFormat.DEFAULT
                  
    def gen(self, text, timeoutMillis=None, model=None, voice=None, format=None, volume=None, speech_rate=None, pitch_rate=None, 
            word_timestamp_enabled=None, phoneme_timestamp_enabled=None):
        """ 合成

        Args:
            text (str): 文本
            timeoutMillis (int): 超时长度，单位毫秒
            model (str): 模型名
            voice (str): 音色名
            format (str): 编码格式
            sample_rate (int): 采样率
            volume (int): 音量
            speech_rate (bool): 语速
            pitch_rate (double): 语调
            word_timestamp_enabled (bool): 字级别时间戳。
            phoneme_timestamp_enabled (bool): 音素时间戳
        Returns:
            data(bite): 
        """
        
        model = self.getValue('model', model)
        if model=='cosyvoice-v1':
            from dashscope.audio.tts_v2 import SpeechSynthesizer
            
            synthesizer = SpeechSynthesizer(
                model, 
                voice=self.getValue('voice', voice), 
                format=self.getFormat(self.getValue('format', format)), 
                volume=self.getValue('volume', volume), 
                speech_rate=self.getValue('speech_rate', speech_rate), 
                pitch_rate=self.getValue('pitch_rate', pitch_rate)
            )
            result = synthesizer.call(text, timeoutMillis)
            return result
        else:
            # sambert
            from dashscope.audio.tts import SpeechSynthesizer
            result = SpeechSynthesizer.call(
                model=self.getValue('model', model),
                format=self.getValue('format', format),
                
                volume=self.getValue('volume', volume),
                sample_rate=self.getSampleRate(self.getValue('model', model)),
                rate=self.getValue('speech_rate', speech_rate),
                pitch=self.getValue('pitch_rate', pitch_rate),
                
                word_timestamp_enabled=self.getValue('word_timestamp_enabled', word_timestamp_enabled),
                phoneme_timestamp_enabled=self.getValue('phoneme_timestamp_enabled', phoneme_timestamp_enabled),
                
                text=text
            )
            return result.get_audio_data()
    
    def to_file(self, text, path, timeoutMillis=None, model=None, voice=None, format=None, volume=None, speech_rate=None, pitch_rate=None, 
               word_timestamp_enabled=False, phoneme_timestamp_enabled=False):
        """ 转成文件

        Args:
            text (str): 文本
            path (str): 路径
            timeoutMillis (int): 超时长度，单位毫秒
            model (str): 模型名
            voice (str): 音色名
            format (str): 编码格式
            volume (int): 音量
            speech_rate (bool): 语速
            pitch_rate (double): 语调
            word_timestamp_enabled (bool): 字级别时间戳。
            phoneme_timestamp_enabled (bool): 音素时间戳
        Returns:
            input_tokens: 输入令牌数
            status_code: 响应码
            request_id: 会话id
            response: 响应结果
        """
        data = self.gen(text, timeoutMillis, model, voice, format, volume, speech_rate, pitch_rate, word_timestamp_enabled, phoneme_timestamp_enabled)
        with open(path, 'wb') as f:
            f.write(data)
    
    def genAsync(self, text, timeoutMillis=None, model=None, voice=None, 
                 on_open=None, on_data=None, on_event=None, on_complete=None, on_error=None, on_close=None, 
                 format=None, volume=None, speech_rate=None, pitch_rate=None,  word_timestamp_enabled=False, phoneme_timestamp_enabled=False):
        """ 合成

        Args:
            text (str): 文本
            path (str): 路径
            timeoutMillis (int): 超时长度，单位毫秒
            
            on_open (function): 
            on_data (function): 
            on_event (function): 
            on_complete (function): 
            on_error (function): 
            on_close (function): 关闭时调用
            
            model (str): 模型名
            voice (str): 音色名
            format (str): 编码格式
            volume (int): 音量
            speech_rate (bool): 语速
            pitch_rate (double): 语调
            word_timestamp_enabled (bool): 字级别时间戳。
            phoneme_timestamp_enabled (bool): 音素时间戳
        Returns:
            input_tokens: 输入令牌数
            status_code: 响应码
            request_id: 会话id
            response: 响应结果
        """
        
        from dashscope.audio.tts_v2 import ResultCallback, SpeechSynthesizer
        
        class Callback(ResultCallback):
            
            def on_open(self):
                print("websocket is open.")
                
                if on_open != None:
                    on_open(self)
                
            def on_data(self, data: bytes) -> None:
                print("tts result length:", len(data))
                
                if on_data != None:
                    on_data(self, data)
                
            def on_event(self, message):
                print(f"recv speech synthsis message {message}")
                
                if on_event != None:
                    on_event(self, message)

            def on_complete(self):
                print("speech synthesis task complete successfully.")
                
                if on_complete != None:
                    on_complete(self)

            def on_error(self, message: str):
                print(f"speech synthesis task failed, {message}")

                if on_error != None:
                    on_error(self, message)

            def on_close(self):
                print("websocket is closed.")
                
                if on_close != None:
                    on_close(self)

        SpeechSynthesizer(
            model=self.getValue('model', model),
            voice=self.getValue('voice', voice), 
            
            format=self.getFormat(self.getValue('format', format)), 
            volume=self.getValue('volume', volume), 
            speech_rate=self.getValue('speech_rate', speech_rate), 
            pitch_rate=self.getValue('pitch_rate', pitch_rate),
            
            # word_timestamp_enabled=self.getValue('word_timestamp_enabled', word_timestamp_enabled),
            # phoneme_timestamp_enabled=self.getValue('phoneme_timestamp_enabled', phoneme_timestamp_enabled),
            
            callback=Callback(),
        ).call(text, timeoutMillis)
    
    def stream(self, texts, sleep=0.5, model=None, voice=None, format=None, sample_rate=None, volume=None, speech_rate=None, pitch_rate=None):
        """ 合成

        Args:
            text (list[str]): 文本集
            timeoutMillis (int): 超时长度，单位毫秒
            model (str): 模型名
            voice (str): 音色名
            format (str): 编码格式
            sample_rate (int): 采样率
            volume (int): 音量
            speech_rate (bool): 语速
            pitch_rate (double): 语调
            word_timestamp_enabled (bool): 字级别时间戳。
            phoneme_timestamp_enabled (bool): 音素时间戳
        Returns:
            input_tokens: 输入令牌数
            status_code: 响应码
            request_id: 会话id
            response: 响应结果
        """
        # def streaming_call(self, String text):
        # def streaming_complete(self, complete_timeout_millis=10000):
        # def async_streaming_complete(self):
        # def streaming_cancel(self):
        
        model = self.getValue('model', model)
        if model=='cosyvoice-v1':
            from dashscope.audio.tts_v2 import SpeechSynthesizer
            synthesizer = SpeechSynthesizer(
                model, 
                voice=self.getValue('voice', voice), 
                format=self.getFormat(self.getValue('format', format)), 
                volume=self.getValue('volume', volume), 
                speech_rate=self.getValue('speech_rate', speech_rate), 
                pitch_rate=self.getValue('pitch_rate', pitch_rate)
            )
            for text in texts:
                synthesizer.streaming_call(text)
                time.sleep(sleep)
            self.synthesizer = synthesizer
            return synthesizer
        else:
            print('sambert 不支持。')
        
    def st(self, text):
        print(text)
        return text
    
    @staticmethod
    def pt(text):
        print(text)
        return text
    
if __name__ == '__main__':
    import re

    def get_title(text):

        # 使用正则表达式匹配《》内的内容
        pattern = r'《(.*?)》'
        match = re.search(pattern, text)

        # 检查是否找到了匹配的内容
        if match:
            content = match.group(1)  # group(1) 表示第一个捕获组，即《》内的内容
            print(content)  # 输出: 特定内容
        else:
            print("没有找到《》内的内容")
            
        return content

    texts = [
        '故事一：《雨中的小花伞》    那是一个暴雨天，街上的行人都在匆忙赶路。你带着年幼的孩子走在回家的路上，雨越下越大，你们只有一把小小的花伞。    你把孩子紧紧地搂在怀里，尽量把伞往孩子那边倾斜，自己的半边身子都被雨水淋湿了。孩子抬起头，用稚嫩的声音说：“妈妈 / 爸爸，你都湿了，伞要一起打。” 你笑着对他说：“宝贝，你不能淋湿，不然会生病的。”    回到家后，你有些狼狈，孩子却拿出毛巾，学着大人的样子为你擦头发。他说：“你保护我，我也要保护你。” 那一刻，你心中充满了温暖，仿佛这场雨带来的寒冷都被孩子的举动驱散了。',
        '故事二：《星空下的秘密》    夏日的夜晚，你带着孩子来到院子里乘凉。天空中繁星闪烁，孩子兴奋地指着星星，眼中充满了好奇。你们躺在草地上，孩子依偎在你身边。    孩子突然问你：“天上的星星有没有家呢？” 你笑着回答：“有呀，就像我们的家一样。” 你们开始聊起了星星的故事，孩子的想象力像插上了翅膀，他说星星在玩捉迷藏，有的藏在云朵后面。    最后，孩子凑到你耳边，悄悄地说：“这是我们的秘密哦，不能告诉别人。” 你点头答应，和孩子一起沉浸在这美好的星空下，那是只属于你们的亲子时光，温馨而甜蜜。',
        '故事三：《生病的陪伴》    孩子生病了，发着高烧，小脸烧得通红。你心急如焚，守在孩子的床边一夜未眠。你不停地用湿毛巾给孩子擦额头、喂水、喂药。    孩子在睡梦中难受地哼哼，你轻轻地握住他的小手，轻声安慰。当孩子醒来，看到你疲惫却又充满关爱的眼神，他虚弱地说：“妈妈 / 爸爸，你一直在呀。” 你点点头，为他擦去眼角的泪花。    在你的细心照料下，孩子的病情逐渐好转。他康复后的笑容，就像阳光照进你的心房，让你觉得所有的辛苦都是值得的。这段生病陪伴的日子，加深了你们之间的亲情羁绊。',
        '故事四：《第一次放风筝》阳光明媚的春日，你带着孩子去公园放风筝。风筝在你们手中组装起来，孩子拿着风筝线，兴奋地跑来跑去。    可是风筝怎么也飞不起来，孩子有些沮丧。你耐心地教他如何判断风向，如何放线。终于，风筝在天空中高高飞起，孩子高兴得手舞足蹈。他拉着风筝线，看着天空中的风筝，对你说：“这是我们一起放起来的呢！”    你们在草地上追逐着风筝，笑声回荡在公园。那一刻，孩子的快乐就是你最大的幸福，这次放风筝的经历成为了你们心中美好的回忆。',
        '故事五：《亲子绘画》    周末，你和孩子坐在桌前准备画画。你拿出画笔和画纸，孩子迫不及待地开始构思。他想要画一个超级英雄的世界。    你们一起讨论着画面的内容，你画着高楼大厦，孩子画着超级英雄在拯救世界。他用五颜六色的画笔涂抹着，脸上满是认真的神情。    在绘画过程中，孩子不小心把颜料涂到了手上，他笑着把颜料抹在你的脸上，你们开始了一场小小的颜料大战。最后，看着充满童趣的画作和彼此花猫似的脸，你们笑得前仰后合。这次亲子绘画不仅创造了一幅有趣的作品，更拉近了你们的心。',
        '故事六：《睡前故事》    每天晚上，孩子都会缠着你讲睡前故事。你坐在床边，打开故事书，柔和的灯光洒在你们身上。    这天，你讲着一个关于友谊的故事，孩子听得津津有味。讲到一半，你故意停顿，让孩子猜猜接下来会发生什么。孩子眨着大眼睛，说出了他的想法，虽然有些稚嫩，但充满了创意。    讲完故事后，孩子抱着你，在你脸颊上亲了一下，说：“晚安，我爱你。” 你为他盖好被子，看着他甜甜的睡脸，你知道，这些睡前故事的时光，是你们之间最温馨的时刻，编织着孩子美好的梦境。',
        '故事七：《动物园之旅》    你带着孩子来到动物园，孩子就像一只欢快的小鸟。他拉着你的手，从一个动物馆跑到另一个动物馆。    在熊猫馆，孩子看到憨态可掬的大熊猫正在吃竹子，他兴奋地模仿着熊猫的动作，逗得你哈哈大笑。在虎山，威风凛凛的老虎让孩子有些害怕，他躲在你身后，你告诉他老虎虽然凶猛，但有玻璃和围栏保护我们。当看到美丽的孔雀开屏时，孩子欢呼起来。这次动物园之旅，孩子认识了很多新的动物，你也记录下了孩子每一个好奇和快乐的瞬间，这是一次充满趣味的亲子冒险。',
        '故事八：《厨房小助手》    你在厨房准备晚餐，孩子跑进来，想要帮忙。你给他系上小围裙，让他帮忙洗菜。孩子认真地洗着青菜，虽然水溅得到处都是，但他做得有模有样。    之后，你教他打鸡蛋，孩子小心翼翼地拿着鸡蛋，在碗边轻轻一磕，金黄色的蛋黄和蛋清流到碗里。他开心地说：“我会打鸡蛋啦！” 你们一起制作晚餐，孩子感受到了劳动的快乐，当吃着自己参与制作的晚餐时，他的满足感溢于言表，而你也享受着这特别的亲子时光。',
        '故事九：《海边的贝壳》    在海边度假，孩子在沙滩上奔跑。海浪一波一波地涌来，沙滩上留下了许多贝壳。    孩子兴奋地捡起贝壳，他把贝壳捧在手心，跑到你面前，说：“看，这些贝壳好漂亮。” 你们一起沿着沙滩寻找贝壳，有白色的、彩色的，形状各异。孩子把贝壳装满了小桶，还挑选了几个最漂亮的送给你。    你们在海边堆沙堡，看着夕阳渐渐落下，孩子的笑脸被余晖映照得格外灿烂。这次海边之旅，贝壳成为',
        
        '故事十：《失落的气球与拥抱》    你带着孩子在游乐园玩，孩子拿着心爱的气球，脸上洋溢着幸福。可突然一阵风，气球飞走了，孩子的笑容瞬间消失，眼泪在眼眶里打转。你蹲下来，紧紧抱住他，轻声说：“宝贝，气球飞走了，但我们还有更有趣的游戏呢。” 然后拉着他去玩旋转木马。孩子慢慢忘记了气球，重新露出笑容，依偎在你怀里。那一刻，你的拥抱治愈了他的小失落，亲子间的温暖胜过了一切玩具。',
        '故事十一：《公园里的小鸭子》    在公园的湖边，有一群小鸭子在游水。孩子被吸引，趴在栏杆上看得入神。小鸭子们排着队，嘎嘎叫着。孩子兴奋地模仿它们的叫声，还拉着你一起看。你给他讲鸭子的生活习性，孩子眼中闪烁着好奇的光芒。你们在湖边待了很久，孩子的快乐感染了你。这种简单的陪伴，看着他对世界充满好奇的样子，让亲子间的情感在大自然的美好中升温。',
        '故事十二：《拼搭积木的合作》    你和孩子一起拼搭积木，准备建造一座城堡。孩子负责找积木，你负责搭建。一开始并不顺利，城堡总是倒塌，但你们没有放弃。孩子不断给你出主意，当城堡终于建成，孩子欢呼雀跃。他抱着你说：“我们好棒！” 你们一起欣赏着成果，这次合作让孩子懂得坚持，也让亲子关系更加亲密，那座积木城堡是你们共同的骄傲。',
        '故事十三：《雪地里的脚印》    下雪了，外面是一个银白的世界。你带着孩子出门玩雪，雪地上留下了你们一串串脚印。孩子在雪地里奔跑、打滚，你和他一起堆雪人。孩子把自己的围巾给雪人戴上，还把胡萝卜插在雪人的脸上当鼻子。玩累了，你们坐在雪地上，看着那片被脚印和雪人点缀的雪地，孩子的脸蛋冻得红红的，但笑容灿烂。在这洁白的雪世界里，你们共享了欢乐的亲子时光。',
        '故事十四：《书店的奇妙之旅》    你带着孩子去书店，一进门，孩子就被五颜六色的书籍吸引。他穿梭在书架间，挑选着自己喜欢的书。最后，孩子选了一本有精美插画的故事书，你和他坐在角落一起阅读。孩子安静下来，沉浸在故事中，还不时问你问题。在书店的静谧氛围中，你们共享了知识的乐趣，亲子间的交流在书本的世界里变得更加深刻。',
        '故事十五：《旧照片里的回忆》    你和孩子一起翻看旧照片，照片里有孩子小时候的模样，有一家人的旅行。孩子指着照片问这问那，你给他讲述每张照片背后的故事。他听得津津有味，还指着自己小时候的照片哈哈大笑。那些回忆在讲述中变得鲜活，孩子感受到家庭的温暖历程，和你之间的距离也因为这些共同的回忆而更近，仿佛时间在这一刻变得温馨而缓慢。',
        '故事十六：《登山的挑战》    你和孩子一起登山，山路有些崎岖，但孩子充满斗志。他拉着你的手，一步一步往上爬。途中孩子累了，你鼓励他坚持。当到达山顶，俯瞰着山下的美景，孩子兴奋地大喊。他的眼中满是自豪，你和他一起享受着成功的喜悦。这次登山之旅，让孩子学会克服困难，也让亲子间的信任和依赖在挑战中加深。',
        '故事十七：《宠物的陪伴》    家里养了一只可爱的宠物，孩子和它形影不离。你和孩子一起给宠物喂食、洗澡。宠物调皮地围着孩子转，孩子笑得合不拢嘴。有一次宠物生病了，孩子很担心，你和孩子一起照顾它。当宠物康复，孩子开心地抱着它。在照顾宠物的过程中，孩子懂得了责任，你和孩子也因为共同的爱而更加亲密，宠物成为了家庭温暖的一部分。',
        '故事十八：《校园表演的鼓励》    孩子要在学校表演节目，他有些紧张。你陪着他在家练习，不断给他鼓励。表演那天，你坐在观众席，用微笑和眼神给他支持。当孩子完成表演，看到台下的你，他跑过来抱住你。你夸奖他表现得非常棒，孩子眼中闪烁着自信的光芒。这次经历让孩子成长，你的鼓励是他最坚强的后盾，亲子间的爱让他勇敢面对挑战。',
        '故事十九：《节日的装饰》    节日到了，你和孩子一起装饰家里。你们挂彩灯、贴窗花、布置圣诞树。孩子拿着装饰品，兴奋地跑来跑去，按照自己的想法装饰。看着家里在你们的努力下变得充满节日氛围，孩子开心地说：“我们的家好漂亮。” 你们在装饰过程中欢笑不断，节日的喜悦在亲子间传递，让家更有温馨的味道。'    
    ]      
    for i in range(len(texts)):
        title = get_title(texts[i])
        url = 'D:\\测试文件\\生成的文件\\语音\\' + str(i + 1) + '.' + title + '.mp3'
        
        tts = TTS('sambert-zhiqi-v1') if i > 9 else TTS('cosyvoice-v1', 'longwan')
        tts.to_file(texts[i], url, speech_rate=1)
    
    
    # titles = [        
    #     '雨中的温暖',
    #     '星空下的约定',
    #     '勇敢的挑战',
    #     '爱的早餐',
    #     '秘密花园',
    #     '海边的回忆',
    #     '温暖的拥抱',
    #     '雨中的笑声',
    #     '星空下的梦想',
    #     '爱心早餐',
    # ]
    # texts = [
    #     '故事一：《雨中的温暖》    一个阴雨绵绵的周末，小明和妈妈决定宅在家里一起做手工。他们找来了彩纸、剪刀和胶水，准备制作一个漂亮的纸灯笼。小明在妈妈的耐心指导下，认真地折叠、裁剪着彩纸。突然，小明不小心剪坏了一张纸，他有些沮丧。妈妈微笑着说：“没关系，我们可以想办法把它变得更好看。” 于是，妈妈和小明一起用彩笔在剪坏的纸上画了一些可爱的图案，纸灯笼变得更加独特了。窗外的雨还在淅淅沥沥地下着，但屋里却充满了温暖和欢笑。',
    #     '故事二：《星空下的约定》    夏日的夜晚，小美和爸爸来到院子里看星星。小美躺在爸爸的怀里，指着天空中的星星问：“爸爸，那颗最亮的星星叫什么名字呀？” 爸爸笑着回答：“那是北极星，它可以为迷路的人指引方向。” 小美眨着眼睛说：“我也想成为像北极星一样的人，帮助别人。” 爸爸轻轻抚摸着小美的头说：“好呀，那我们一起努力。” 他们在星空下许下了一个美好的约定。',
    #     '故事三：《勇敢的挑战》    周末，小刚和妈妈一起去爬山。一开始，小刚充满了活力，蹦蹦跳跳地走在前面。但随着山路越来越陡峭，小刚开始感到疲惫和害怕。妈妈鼓励他说：“小刚，你是最勇敢的孩子，只要坚持下去，我们一定能爬到山顶。” 在妈妈的鼓励下，小刚鼓起勇气，一步一步地往上爬。终于，他们到达了山顶，看着美丽的风景，小刚感到无比自豪。',
    #     '故事四：《爱的早餐》    早上，妈妈轻轻地走进小悦的房间，叫醒了还在睡梦中的小悦。小悦揉着眼睛说：“妈妈，我还想再睡一会儿。” 妈妈笑着说：“宝贝，今天妈妈给你做了特别的早餐哦。” 小悦一听，立刻来了精神。他们一起走进厨房，看到桌子上摆着一份精美的三明治和一杯热牛奶。小悦开心地吃着早餐，感受着妈妈的爱。',
    #     '故事五：《秘密花园》    小琳和爸爸在院子里开辟了一个小花园。他们一起翻土、播种、浇水，期待着花朵的绽放。日子一天天过去，小花园里长出了嫩绿的芽。小琳每天都会去看看她的小花园，和爸爸一起照顾这些小生命。终于，花园里开满了五颜六色的花朵。小琳和爸爸坐在花园里，享受着这美丽的风景，心中充满了幸福。',
    #     '故事六：《海边的回忆》    夏日的午后，阳光洒在金色的沙滩上，小宇和妈妈来到了海边。小宇兴奋地奔跑着，追逐着海浪。妈妈在一旁微笑着看着他，时不时提醒他小心别摔倒。小宇突然停下来，捡起一个漂亮的贝壳，跑到妈妈身边说：“妈妈，这个贝壳好漂亮，送给你。” 妈妈接过贝壳，眼中满是感动。他们一起坐在沙滩上，看着远方的大海，妈妈给小宇讲起了关于大海的故事。小宇听得入了迷，他想象着自己也能像故事里的主人公一样，在大海上勇敢地冒险。夕阳西下，他们手牵着手，留下了一串幸福的脚印。',
    #     '故事七：《温暖的拥抱》    小萱最近在学校遇到了一些不开心的事情，心情很低落。回到家后，她一声不吭地走进了自己的房间。妈妈察觉到了小萱的异常，轻轻地敲了敲门，走了进去。妈妈坐在小萱的床边，温柔地问她发生了什么事。小萱扑进妈妈的怀里，哭着说出了自己的委屈。妈妈紧紧地抱着她，轻轻地拍着她的背说：“没关系，宝贝，有妈妈在。” 在妈妈温暖的拥抱中，小萱的心情渐渐好了起来。她知道，无论遇到什么困难，妈妈都会一直陪伴着她。',
    #     '故事八：《雨中的笑声》    一场突如其来的大雨，让小明和爸爸被困在了公园里。他们找了一个亭子躲雨，看着外面的雨景。小明有些无聊，爸爸便提议一起玩猜谜语的游戏。他们你一个我一个地猜着谜语，笑声在亭子里回荡。雨渐渐小了，爸爸带着小明在雨中奔跑着，感受着雨水带来的清凉。他们的衣服都被淋湿了，但他们的脸上却洋溢着快乐的笑容。回到家后，妈妈看到他们湿漉漉的样子，虽然有些生气，但也被他们的快乐所感染。',
    #     '故事九：《星空下的梦想》    夜晚，小辉和妈妈一起躺在草地上，看着满天的星星。小辉指着一颗最亮的星星说：“妈妈，我长大后想当一名宇航员，去探索宇宙。” 妈妈微笑着说：“那你要努力学习哦，实现自己的梦想。” 小辉点了点头，眼中充满了憧憬。他们一起想象着宇宙的奥秘，谈论着未来的可能。在星空下，小辉的梦想变得更加坚定。',
    #     '故事十：《爱心早餐》    周末的早上，小琪早早地起了床，决定给爸爸妈妈做一份爱心早餐。她学着妈妈平时的样子，打开冰箱，拿出鸡蛋、面包和牛奶。小琪小心翼翼地煎着鸡蛋，虽然有些手忙脚乱，但最终还是成功了。她把早餐摆放在餐桌上，然后去叫醒爸爸妈妈。爸爸妈妈看到小琪做的早餐，非常感动。他们一起坐在餐桌前，享受着这份充满爱的早餐，心中充满了幸福。',
    # ]

    # # sambert-zhimiao-emo-v1

    # for i in range(len(texts)):
    #     url = 'D:\\测试文件\\生成的文件\\语音\\' + str(i + 1) + '.' + titles[i] + '.mp3'
    #     tts = TTS('sambert-zhimiao-emo-v1')
    #     tts.to_file(texts[i], url, speech_rate=1)
    
    
    import sys
    
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    
    tts = TTS(sys.argv[1])
    tts.to_file(sys.argv[2], 'D:\\测试文件\\生成的文件\\语音\\' + sys.argv[3] + '.mp3', speech_rate=1.3)
    
    # import asyncio
    # import platform
    # if platform.system() == 'Windows':
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    # import uuid
    # client_id = str(uuid.uuid4())
    
    # tts = TTS('cosyvoice-v1', 'longmiao', 'MP3_16000HZ_MONO_128KBPS')
    # tts.to_file('你好啊，你还记得我吗？', 'D:\\测试文件\\生成的文件\\语音\\2.mp3')
    
    # text = '今天的福利力度相当的到位，相当的大，是您在外面都看不到的福利，而且我们家不管任何一个链接，' + \
    #     '它的使用时间呢，写的很清楚，包括大家买了之后呢，它都是可以随时退的，过期过后也都是可以退的，' + \
    #     '自动退哦，就是大家不用担心时间到了没有用掉的问题，完全没有任何的后顾之忧，都可以放心去拍，' + \
    #     '大家有任何的问题呢，都可以直接扣在我们的公屏上，像评论区这位小美姐一样哈。'
        
    # text = 'The welfare benefits today are quite generous, quite substantial, and are benefits that you will not see elsewhere. ' + \
    #     'Moreover, for any link on our site, the usage time is clearly stated. Including after you have made a purchase, ' + \
    #     'you can return it at any time, and it can be automatically refunded after expiration, ' + \
    #     'so you do not have to worry about the issue of not using it by the deadline. You can fully rest assured and go ahead and make your purchase. ' + \
    #     'If you have any questions, you can directly post them on our public screen, just like this commenter, Sister Xiaomei.'
    
    # text = '你好啊，你还记得我吗？'
    # models = [      
    #     'sambert-zhichu-v1',
    #     'sambert-zhiwei-v1',
    #     'sambert-zhixiang-v1',
    #     'sambert-zhide-v1',
    #     'sambert-zhijia-v1',
    #     'sambert-zhinan-v1',
    #     'sambert-zhiqi-v1',
    #     'sambert-zhiqian-v1',
    #     'sambert-zhiru-v1',
    #     'sambert-zhimiao-emo-v1',
    #     'sambert-zhida-v1',
    #     'sambert-zhifei-v1',
    #     'sambert-zhigui-v1',
    #     'sambert-zhihao-v1',
    #     'sambert-zhijing-v1',
    #     'sambert-zhilun-v1',
    #     'sambert-zhimao-v1',
    #     'sambert-zhiming-v1',
    #     'sambert-zhimo-v1',
    #     'sambert-zhina-v1',
    #     'sambert-zhishu-v1',
    #     'sambert-zhishuo-v1',
    #     'sambert-zhistella-v1', 
    #     'sambert-zhiting-v1',
    #     'sambert-zhixiao-v1',
    #     'sambert-zhiya-v1',
    #     'sambert-zhiye-v1',
    #     'sambert-zhiying-v1',
    #     'sambert-zhiyuan-v1',
    #     'sambert-zhiyue-v1',
    #     'sambert-camila-v1',
    #     'sambert-perla-v1',
    #     'sambert-indah-v1',
    #     'sambert-clara-v1',
    #     'sambert-hanna-v1',
    #     'sambert-beth-v1', 
    #     'sambert-betty-v1',
    #     'sambert-cally-v1',
    #     'sambert-cindy-v1',
    #     'sambert-eva-v1',
    #     'sambert-donna-v1',
    #     'sambert-brian-v1',
    #     'sambert-waan-v1',
    # ]
    # names = [
    #     '知厨-舌尖男声-中文+英文-48k',
    #     '知薇-萝莉女声-中文+英文-48k',
    #     '知祥-磁性男声-中文+英文-48k',
    #     '知德-新闻男声-中文+英文-48k',
    #     '知佳-标准女声-中文+英文-48k',
    #     '知楠-广告男声-中文+英文-48k',
    #     '知琪-温柔女声-中文+英文-48k',
    #     '知倩-资讯女声-中文+英文-48k',
    #     '知茹-新闻女声-中文+英文-48k',
    #     '知妙(多情感)-多种情感女声-中文+英文-16k',
    #     '知达-标准男声-中文+英文-16k',
    #     '知飞-激昂解说-中文+英文-16k',
    #     '知柜-直播女声-中文+英文-16k',
    #     '知浩-咨询男声-中文+英文-16k',
    #     '知婧-严厉女声-中文+英文-16k',
    #     '知伦-悬疑解说-中文+英文-16k',
    #     '知猫-直播女声-中文+英文-16k',
    #     '知茗-诙谐男声-中文+英文-16k',
    #     '知墨-情感男声-中文+英文-16k',
    #     '知娜-浙普女声-中文+英文-16k',
    #     '知树-资讯男声-中文+英文-16k',
    #     '知硕-自然男声-中文+英文-16k',
    #     '知莎-知性女声-中文+英文-16k',
    #     '知婷-电台女声-中文+英文-16k',
    #     '知笑-资讯女声-中文+英文-16k',
    #     '知雅-严厉女声-中文+英文-16k',
    #     '知晔-青年男声-中文+英文-16k',
    #     '知颖-软萌童声-中文+英文-16k',
    #     '知媛-知心姐姐-中文+英文-16k',
    #     '知悦-温柔女声-中文+英文-16k',
    #     'Camila-西班牙语女声-西班牙语-16k',
    #     'Perla-意大利语女声-意大利语-16k',
    #     'Indah-印尼语女声-印尼语-16k',
    #     'Clara-法语女声-法语-16k',
    #     'Hanna-德语女声-德语-16k',
    #     'Beth-咨询女声-美式英文-16k',
    #     'Betty-客服女声-美式英文-16k',
    #     'Cally-自然女声-美式英文-16k',
    #     'Cindy-对话女声-美式英文-16k',
    #     'Eva陪伴女声-美式英文-16k',
    #     'Donna-教育女声-美式英文-16k',
    #     'Brian-客服男声-美式英文-16k',
    #     'Waan-泰语女声-泰语-16k'
    # ]
    # for i in range(len(models)):
    #     tts = TTS(models[i])
    #     tts.to_file(text, 'D:\\测试文件\\生成的文件\\语音\\' + names[i] + '.mp3', speech_rate=1.3)
        
    
        
    
    
    # voice = [
    #     'longwan',
    #     'longcheng',
    #     'longhua',
    #     'longxiaochun',
    #     'longxiaoxia',
    #     'longxiaocheng',
    #     'longxiaobai',
    #     'longlaotie',
    #     'longshu',
    #     'longshuo',
    #     'longjing',
    #     'longmiao',
    #     'longyue',
    #     'longyuan',
    #     'longfei',
    #     'longjielidou',
    #     'longtong',
    #     'longxiang',
    #     'loongstella',
    #     'loongbella'
    # ]
    # names = [
    #     '龙婉-语音助手、导航播报、聊天数字人-中文普通话',
    #     '龙橙-语音助手、导航播报、聊天数字人-中文普通话',
    #     '龙华-语音助手、导航播报、聊天数字人-中文普通话',
    #     '龙小淳-语音助手、导航播报、聊天数字人-中文+英文',
    #     '龙小夏-语音助手、聊天数字人-中文',
    #     '龙小诚-语音助手、导航播报、聊天数字人-中文+英文',
    #     '龙小白-聊天数字人、有声书、语音助手-中文',
    #     '龙老铁-新闻播报、有声书、语音助手、直播带货、导航播报-中文东北口音',
    #     '龙书-有声书、语音助手、导航播报、新闻播报、智能客服-中文',
    #     '龙硕-语音助手、导航播报、新闻播报、客服催收-中文',
    #     '龙婧-语音助手、导航播报、新闻播报、客服催收-中文',
    #     '龙妙-客服催收、导航播报、有声书、语音助手-中文',
    #     '龙悦-语音助手、诗词朗诵、有声书朗读、导航播报、新闻播报、客服催收-中文',
    #     '龙媛-有声书、语音助手、聊天数字人-中文',
    #     '龙飞-会议播报、新闻播报、有声书-中文',
    #     '龙杰力豆新闻播报、有声书、聊天助手-中文+英文',
    #     '龙彤-有声书、导航播报、聊天数字人-中文',
    #     '龙祥-新闻播报、有声书、导航播报-中文',
    #     'Stella-语音助手、直播带货、导航播报、客服催收、有声书-中文+英文',
    #     'Bella-语音助手、客服催收、新闻播报、导航播报-中文'
    # ]
    # for i in range(len(voice)):
    #     v = voice[i]
    #     tts = TTS('cosyvoice-v1')
    #     tts.to_file(text, voice=v, path='D:\\测试文件\\生成的文件\\语音\\' + names[i] + '.mp3')
    
    
    
    
    # def on_open(data):
    #     print("这是一个命名函数")
        
    # def on_data(call, data):
    #     a = data
    #     # print("这是一个命名函数" + str(data))
        
    # tts = TTS('cosyvoice-v1', 'longmiao', 'MP3_16000HZ_MONO_128KBPS')
    # tts.genAsync('你好啊，你还记得我吗？', on_open=on_open, on_data=on_data)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    