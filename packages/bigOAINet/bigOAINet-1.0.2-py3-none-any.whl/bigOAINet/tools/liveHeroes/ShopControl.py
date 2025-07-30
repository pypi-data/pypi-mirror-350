import mxupy as mu

from mxupy import IM
from liveheroes.m.Models import *
from liveheroes.UserControl import UserControl

class ShopControl(mu.EntityXControl):

    class Meta:
        model_class = Shop

    def set_default(self, shopId, userId):
        """ 设置默认商家

        Args:
            shopId (int): 商家id
            userId (int): 用户id
            
        Returns:
            IM: 结果
        """
        def _do():
            
            im = self.get_one_by_id(shopId)
            if im.check_data().error:
                return im
            shop = im.data
            
            if shop.userId != userId:
                return IM(False, '设置默认网店失败，此网店不属于此用户。')
            
            # 将用户所有商店设为 false
            im = self.update({'userId':userId}, {'isDefault':False})
            if im.error:
                return im
            
            im = self.update_by_id(shopId, {'isDefault':True})
            if im.error:
                return im
            
            return im

        return self.run(_do)

    def delete_by_id(self, shopId):
        """ 删除商家

        Args:
            audioId (int): 商家id

        Returns:
            IM: 删除结果
        """
        sup = super()
        def _do():
            
            im = self.get_one_by_id(shopId, select=['userId'])
            if im.check_data().error:
                return im
            userId = im.data.userId
            
            im = self.get_count(where={'userId': userId})
            if im.error:
                return im
            
            if im.data <= 1:
                return IM(False, '删除失败。用户拥有的商家少于 2 个，不容许删除。')

            im = sup.delete_by_id(shopId)
            if im.error:
                return im

            return self.set_default(im.data.shopId, userId)
        
        return self.run(_do)

    def share(self, shopId, userId):
        """ 分享商家

        Args:
            shopId (int): 商家id
            userId (int): 用户id

        Returns:
            IM: 结果
        """
        def _do():
            
            from liveheroes.ShopShareControl import ShopShareControl
            
            im = UserControl.inst().exists_by_id(userId)
            if im.check_data().error:
                return im
            
            im = self.exists_by_id(shopId)
            if im.check_data().error:
                return im
            
            str1 = mu.guid4()
            for char in '0olijq92z':
                str1 = str1.replace(char, '8')
                
            im = ShopShareControl.inst().add(
                {
                    'userId': userId,
                    'shopId': shopId,
                    'code': f"{userId}w{shopId}w{str1}"
                }
            )
            if im.error:
                return im
            
            return im

        return self.run(_do)
    
    def _handle_shop_data(self, shop, userId=-1):
        """ 处理商家数据

        Args:
            shop (_type_): _description_
            userId (int, optional): _description_. Defaults to -1.

        Returns:
            _type_: _description_
        """
        
        from liveheroes.AudioWordFolderControl import AudioWordFolderControl
        from liveheroes.AudioWordControl import AudioWordControl
        
        new_shop = self.clone(shop)
        
        if userId > -1:
            new_shop.userId = userId
        
        new_shop.isDefault = False
        new_shop.douyinRoomUrl = ''

        im = self.add(new_shop)
        if im.error:
            return im
        shop2 = im.data
        shopId2 = shop2.shopId

        for af in shop.audioFolders:
            af1 = AudioWordFolderControl.inst().clone(af)
            af1.shopId = shopId2
            im = AudioWordFolderControl.inst().add(af1)
            if im.error:
                return im
            af2 = im.data

            for a in af.audios:
                a1 = AudioWordControl.inst().clone(a)
                a1.audioFolderId = af2.audioFolderId
                im = AudioWordControl.inst().add(a1)
                if im.error:
                    return im

       

            
        im.data = shop2
        
        return im
    
    def import_shop(self, userId, code):
        """ 按分享码导入商家

        Args:
            userId (int): 用户id
            code (str): 分享码
        """
        def _do():
            
            from liveheroes.ShopShareControl import ShopShareControl
            
            im = UserControl.inst().exists_by_id(userId)
            if im.check_data().error:
                return im

            im = ShopShareControl.inst().get_one(where={'code':code.lower()})
            if im.check_data().error:
                return im
            ss = im.data
            
            im = self.get_one_by_id(ss.shopId)
            if im.check_data().error:
                return im
            shop = im.data
           
            im = self._handle_shop_data(shop, userId)
            if im.error:
                return im

            im.data = ss.userId
            return im

        return self.run(_do)
         
    def add_with_clone(self, shopId):
        """ 克隆商户并添加

        Args:
            shopId (int): 商家id
        """
        def _do():

            im = self.get_one_by_id(shopId)
            if im.check_data().error:
                return im
            shop = im.data
            
            im = self._handle_shop_data(shop, -1)
            if im.error:
                return im
            shop2 = im.data
            
            im.data = shop2.shopId
            
            return im

        return self.run(_do)
