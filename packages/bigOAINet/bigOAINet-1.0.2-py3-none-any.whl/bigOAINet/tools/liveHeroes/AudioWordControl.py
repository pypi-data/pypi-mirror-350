import mxupy as mu

from liveheroes.m.Models import *
from liveheroes.UserControl import UserControl

class AudioWordControl(mu.EntityXControl):

    class Meta:
        model_class = AudioWord
    
    def delete_by_id(self, audioWordId, userId, accesstoken):
        """ 删除语音文本，需校验令牌

        Args:
            audioWordId (int): 讲解音id
            userId (int): 用户id
            accesstoken (str): 令牌

        Returns:
            IM: 删除结果
        """
        sup = super()
        def _do():
            
            im = UserControl.inst().check_accesstoken(userId, accesstoken)
            if im.error:
                return im

            return sup.delete_by_id(audioWordId)
        
        return self.run(_do)


    


  
