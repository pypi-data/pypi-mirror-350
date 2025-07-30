import mxupy as mu

from liveheroes.m.Models import *
from liveheroes.UserControl import UserControl

class AudioWordFolderControl(mu.EntityXControl):

    class Meta:
        model_class = AudioWordFolder
    
    def delete_by_id(self, audioFolderId, userId, accesstoken):
        """ 删除音频文件夹，需校验令牌

        Args:
            audioFolderId (int): 音频文件夹id
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

            return sup.delete_by_id(audioFolderId)
        
        return self.run(_do)

