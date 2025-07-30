from peewee import *
import os
import mxupy as mu
from mxupy import IM
from playhouse.shortcuts import model_to_dict
import bigOAINet as bigo

import numpy as np
from gensim.models import KeyedVectors
from gensim.utils import simple_preprocess
from scipy.spatial.distance import cosine
import jieba

from pathlib import Path


import soundfile as sf

from bigOAINet.tools.TextSimilarityProcessor.TextSimilarityProcessor import TextSimilarityProcessor

# PRETRAINED_MODEL_PATH = "nlp_starter/light_Tencent_AILab_ChineseEmbedding.bin"


class MyDHQAControl(mu.EntityXControl):

    class Meta:
        model_class = bigo.MyDHQA
        
    def __init__(self, *args, **kwargs):
        
        # self.q_vectors = None
        
        # if not hasattr(self, 'word2VecModel'):
        #     self.word2VecModel = KeyedVectors.load_word2vec_format(PRETRAINED_MODEL_PATH, binary=True)
            
        # if not hasattr(self, 'voice_recognizer'):
        #     self.voice_recognizer = self.create_recognizer()
            
        super().__init__(*args, **kwargs)
        
    # def create_recognizer(self):
    #     import sherpa_onnx
    #     model = "./models/sherpa-onnx-paraformer-zh-2024-03-09/model.onnx"
    #     tokens = "./models/sherpa-onnx-paraformer-zh-2024-03-09/tokens.txt"
    #     rule_fsts = "./models/sherpa-onnx-paraformer-zh-2024-03-09/itn_zh_number.fst"

    #     if (
    #         not Path(model).is_file()
    #         or not Path(tokens).is_file()
    #         or not Path(rule_fsts).is_file()
    #     ):
    #         raise ValueError(
    #             """Please download model files from
    #             https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models
    #             """
    #         )
    #     return sherpa_onnx.OfflineRecognizer.from_paraformer(
    #         paraformer=model,
    #         tokens=tokens,
    #         debug=True,
    #         rule_fsts=rule_fsts,
    #     )
        
    # # 使用 jieba 进行分词
    # def preprocess_sentence(self, sentence):
    #     return list(jieba.cut(sentence))
    
    # # 将句子转换为向量
    # def sentence_to_vector(self, sentence, model):
    #     words = self.preprocess_sentence(sentence)
    #     vectors = [model[word] for word in words if word in model]
    #     if vectors:
    #         return np.mean(vectors, axis=0)
    #     else:
    #         return np.zeros(model.vector_size)

    # # 计算句子之间的余弦相似度
    # def cosine_similarity(self, vec1, vec2):
    #     return 1 - cosine(vec1, vec2)

    # # 主函数
    # def find_most_similar_question(self, question, qs):
    #     # 将用户问题和问答集中的问题转换为向量
    #     user_question_vector = self.sentence_to_vector(question, self.word2VecModel)
    #     if self.q_vectors is None:
    #         self.q_vectors = [self.sentence_to_vector(q, self.word2VecModel) for q in qs]
    #     # 计算相似度
    #     similarities = [self.cosine_similarity(user_question_vector, vec) for vec in self.q_vectors]
    #     # 获取相似度最高的问题
    #     most_similar_index = np.argmax(similarities)
    #     most_similar_question = qs[most_similar_index]
    #     highest_similarity = similarities[most_similar_index]
        
    #     return most_similar_question, highest_similarity
    
    def update1(self, model, userId, accessToken):
        """
            修改

        Args:
            model (MyDHQA): 实体
            userId (int): 用户id。
            accessToken (str): 访问令牌。

        Returns:
            IM：结果
        """
        def _do():
            im = IM()
            
            obj = mu.dict_to_obj(model)
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            # 修改
            im = self.update_by_id(obj.myDHQAId, model=model)
            if im.error:
                return im
            
            return im

            # qa = bigo.MyDHQA.select().where(bigo.MyDHQA.qaId == model.qaId,bigo.MyDHQA.userId == userId).first()
            # if mu.isN(qa):
            #     im.success = False
            #     im.msg = '问答不存在'
            #     return im

            # qa.question=model.question
            # qa.answer=model.answer
            # qa.renderStatus=model.renderStatus
            # # 删除老的生成视频
            # if mu.isNN(qa.videoFile) and qa.videoFile != model.videoFile:
            #     mu.removeFile(mu.file_dir('user',userId) + '\\'  + qa.videoFile)
            # qa.videoFile=model.videoFile
            # qa.save()

            # im.msg = '恭喜！修改问答成功。'
            # im.data = model_to_dict(qa, False)

        return self.run(_do)
    
    def delete1(self, id, userId, accessToken):
        """
            删除

        Args:
            id (int): 主键id
            userId (int): 用户id。
            accessToken (str): 访问令牌。

        Returns:
            IM：结果
        """
        def _do():
            
            # 检验访问令牌
            im = bigo.UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im
            
            # 查询是否存在 qaId 这条数据
            im = self.get_one(where={'myDHQAId': id, 'userId': userId})
            if im.error:
                return im
            qa = im.data

            # # 收集所有的文件路径
            # filePathList = []
            
            # if mu.isNN(qa.videoFile):
            #     filePathList.append(qa.videoFile)

            # filePath = mu.file_dir('user',userId) + '\\'

            # filepath, shotname, extension = mu.fileParts(qa.videoFile)
            # dataPath = mu.file_dir('user',userId)
            # filePathList.append(shotname + '.m3u8')
            # for root, dirs, files in os.walk(filePath):
            #     for file in files:
            #         if file.endswith(".ts") and file.startswith(shotname):
            #             filePathList.append(file)

            # attachmentList = list(qa.attachmentList)

            # for attachment in attachmentList:
            #     filePathList.append(attachment.attachmentUrl)

            # 删除自己
            im = self.delete_by_id(id)
            if im.error:
                return im
            
            return im
            
            # # 去重后删除全部关联文件
            # filePathListSet = list(set(filePathList))
            # mu.removeFileList(filePathListSet, filePath)

        return self.run(_do)
    
    def reply(self, question, qs):
        """
            删除

        Args:
            question (str): 问题

        Returns:
            IM：结果
        """
        def _do():
            
            im = IM()
            q, similarity = TextSimilarityProcessor().find_most_similar_question(question, qs)
            im.data = {
                'userQuestion': question,
                'question': q,
                'similarity': similarity,
            }
            return im
        return self.run(_do)
        
    def reply_with_voice(self, userId, qs):
        """
            删除

        Args:
            question (str): 问题

        Returns:
            IM：结果
        """
        def _do():
            
            im = IM()
            
            voice_path = mu.file_dir('user', userId) + '/digitalHuman/qaVoice/' + 'question_audio.wav'
            
            # recognizer = self.create_recognizer()
            # wave_filename = "./models/sherpa-onnx-paraformer-zh-2024-03-09/test_wavs/0.wav"
            
            if not Path(voice_path).is_file():
                raise ValueError(
                    """Please download model files from
                    https://github.com/k2-fsa/sherpa-onnx/releases/tag/asr-models
                    """
                )
            audio, sample_rate = sf.read(voice_path, dtype="float32", always_2d=True)
            # 仅使用第一个通道
            audio = audio[:, 0]

            recognizer = self.voice_recognizer
            stream = recognizer.create_stream()
            stream.accept_waveform(sample_rate, audio)
            recognizer.decode_stream(stream)
            # print(voice_path)
            # print(stream.result)
            q = stream.result.text
            im = self.reply(q, qs)
            
            return im
            

        return self.run(_do)
    
    
if __name__ == '__main__':
    # 实例化控制类并调用方法
    control = MyDHQAControl()
    
    import soundfile as sf
    
    # import sounddevice as sd  # pip install sounddevice

    # audio, sr = load_audio_fixed("recorded-audio.wav")
    # print(f"播放音频: {audio.shape} {sr}Hz")
    # sd.play(audio, sr, blocking=True)

    # audio, sample_rate = sf.read("F:/T/1/recorded-audio.wav")
    # print(f"采样率: {sample_rate} Hz")
    # print(f"音频形状: {audio.shape}")  # 应为 (样本数, 声道数)
    # print(f"数据类型: {audio.dtype}")  # 应为 float32 或 int16
    # print(f"取值范围: [{audio.min()}, {audio.max()}]")  # float32应在[-1,1]，int16应在[-32768,32767]
    
    # im = control.reply_with_voice('F:/T/1/digitalHuman/voice/20250426045424.wav', ['你好', '你好吗', '你好啊'])
    im = control.reply_with_voice(1, ['你好', '你好吗', '你好啊'])
    # im = control.reply_with_voice('F:/T/1/123.wav', ['你好', '你好吗', '你好啊'])
    
    # filepath = 'D:/AI项目/BIGOAINET/models/sherpa-onnx-paraformer-zh-2024-03-09/test_wavs/0.wav'
    # im = control.reply_with_voice(filepath, ['你好', '你好吗', '你好啊'])
    print(im)
    
    