import uuid as uid
import mxupy as mu

from datetime import datetime, timedelta
from mxupy import IM, read_server

from liveheroes.m.Models import CardSerial
from liveheroes.UserControl import UserControl

# config = {
#     'appKeys': [{
#         'appId': 1,
#         'appKey': '46f04371-5e98-b705-5dee-88d7ddb2d6bi',
#         'isActive': True
#     }]
# }

class CardSerialControl(mu.EntityXControl):

    class Meta:
        model_class = CardSerial

    def activate_cardSerial(self, userId, cardSerial):
        """ 激活卡密。对用户来说，会叠加卡密时长。

        Args:
            userId (int): 用户id
            cardSerial (str): 卡密

        Returns:
            IM: 结果
        """

        def _do():
            
            im = self.get_one(where={'cardSerial':cardSerial})
            if im.check_data('没有找到卡密，请确认输入正确！').error:
                return im
            cs = im.data

            if cs.isActive:
                return IM(False, '该卡密已被激活！')

            cs.isActive = True
            cs.userId = userId
            cs.activeTime = datetime.now()
            if mu.isN(cs.expires):
                cs.expires = datetime.now()
            cs.expires = cs.expires + timedelta(days=cs.days)
            
            im = self.update_by_id(cs.cardSerialId, cs, fields=['isActive', 'userId', 'activeTime', 'expires'])
            if im.error:
                return im

            today = datetime.now().date()
            # 更新用户最新卡密状态
            im = UserControl.inst().get_one_by_id(userId)
            if im.check_data().error:
                return im
            user = im.data
            
            user_expires_datetime = mu.parseDateTime(user.expires).date()
            if user_expires_datetime <= today:
                user.expires = today + timedelta(days=cs.days)
            else:
                user.expires = user_expires_datetime + timedelta(days=cs.days)

            user.cardSerial = cs.cardSerial
            user.appType = cs.appType
            im = UserControl.inst().update_by_id(userId, user, fields=['expires', 'cardSerial', 'appType'])
            if im.error:
                return im

            return IM(True, f'卡密激活成功！到期时间 {user.expires}', cs)
        
        return self.run(_do)

    def id_key_check(self, appId, appKey):
        """ 校验 appId 和 appKey

        Args:
            appId (int): 应用id
            appKey (str): 应用key

        Returns:
            IM: 结果
        """
        def _do():
            
            apps = read_server().get('apps', {})
            is_valid = any(app['appId'] == int(appId) and app['appKey'] == str(appKey) for app in apps)
            if not is_valid:
                return IM(False, 'AppId 或 AppKey 错误，请检查。')
            return IM()
        
        return self.run(_do)

    def get_all_cardSerial(self, userId, accesstoken):
        """ 获取所有密匙

        Args:
            userId (int): 用户id
            accesstoken (str): 令牌

        Returns:
            IM: 结果
        """
        def _do():
            
            
            im = UserControl.inst().check_accesstoken(userId, accesstoken)
            if im.error:
                return im
            
            im = self.get_list()
            if im.error:
                return im
            
            user = { 'nickname': '', 'username': '' }
            u = None
            css = []
            for d in im.data:
                
                if d.userId == -1:
                    u = user
                else:
                    im = UserControl.inst().get_one_by_id(d.userId, select=['nickname', 'username'])
                    if im.error:
                        return im
                    u = im.data if im.data else user
                d.user = u
                css.append(d)
            
            im.data = mu.obj_to_dict(css)
            return im

        return self.run(_do)

    def create_cardSerial(self, type, days, appId, appKey):
        """ 创建卡密

        Args:
            type (str): 类型，pro、base
            days (int): 天数
            appId (int): 应用id
            appKey (str): 应用key
        """
        def _do():
            
            im = self.id_key_check(appId, appKey)
            if im.error:
                return im
            
            data = {
                'cardSerial': uid.uuid4().hex,
                'appType': type,
                'isActive': False,
                'userId': -1,
                'activeTime': '',
                'days': days,
                'expires': ''
            }
            return self.add(data)
        
        return self.run(_do)

    def deactivate_cardSerial(self, cardSerialId, appId, appKey):
        """ 停用卡密

        Args:
            cardSerialId (int): 卡密id
            appId (int): 应用id
            appKey (str): 应用key
        """
        def _do():
            
            im = self.id_key_check(appId, appKey)
            if im.error:
                return im

            im = self.update_by_id(cardSerialId, { 'isActive': False })
            if im.error:
                return im
            
            im.msg = '卡密停用成功。'
            return im
        
        return self.run(_do)

