import mxupy as mu
from mxupy import IM

from base.member.m.User import User as MemberUser
from base.member.UserControl import userControl as memberUserControl

from m.Developer import Developer
from m.AuthUser import AuthUser
from m.AuthLog import AuthLog
from m.User import User

from .DeveloperControl import developerControl
from .UserControl import userControl
from .AuthLogControl import authLogControl

class AuthUserControl(mu.EntityXControl):
    class Meta:
        model_class = AuthUser
        
    def auth(self, url, developerId, type='snsapi_base', state=None):
        """ 用户授权

        Args:
            url (str): 回调路径
            developerId (int): 开发者id
            type (str): 回调类型 snsapi_base, snsapi_userinfo
            state (str): 用户自定义参数
        """
        from weixin.login import WeixinLogin
        
        state = str(developerId)
        
        im = IM()
        im = developerControl.get_one_by_id(developerId)
        if im.error:
            return im
        d = im.data
        
        # 这两个值应该要去数据库中获取
        wx_login = WeixinLogin(d.appId, d.appSecret)
        url = wx_login.authorize(url, type, state)
        print(url)
        return url
        
    def authed(self, code, state):
        """ 用户授权回调

        Args:
            callback (str): 回调路径
            token (str): _description_. Defaults to ''.
            encoding_aes_key (str): _description_. Defaults to ''.
        """
        from weixin.login import WeixinLogin
        im = IM()
        
        if not state:
            im.msg = '监测到无效微信授权'
            return im
        print(state)
        
        state = mu.str_to_obj(state)
        dId = int(getattr(state, 'developerId', -1))
        if dId < 1:
            im.msg = '监测到无效微信授权'
            return im
        
        im = developerControl.get_one_by_id(dId)
        if im.error:
            return im
        d = im.data
        
        # 这两个值应该要去数据库中获取
        wx_login = WeixinLogin(d.appId, d.appSecret)
        
        # 获取令牌和凭证
        data = wx_login.access_token(code)
        print(data)
        
        ui = wx_login.user_info(data.access_token, data.openid)
        
        userId = -1
        # 通过 openid 去数据库中拿 会员用户id
        im = self.get_one(where={'openid': data.openid})
        if not im.data:
            # 添加会员用户
            im = memberUserControl.get_one(where={'userName': data.openid})
            if not im.data:
                im = memberUserControl.add(
                    MemberUser(userName=ui.openid, password=ui.openid, 
                                nickName=ui.nickname,realName=ui.nickname,
                                avatar=ui.headimgurl,gender=ui.sex,isActive=False))
                if im.error:
                    return im
                u = im.data
            else:
                u = im.data
            userId = u.id
            
            # 添加微信用户
            im = userControl.get_one(where={'openid': data.openid})
            if not im.data:
                im = userControl.add(
                    User(openid=ui.openid, userId=userId, developerId=dId,
                        isSubscribe=False, avatar=ui.headimgurl, sex=ui.sex,
                        country=ui.country,province=ui.province,city=ui.city))
                if im.error:
                    return im
            
            # 添加微信授权用户
            im = self.get_one(where={'openid': data.openid})
            if not im.data:
                im = self.add(
                    AuthUser(userId=u.id, openid=ui.openid, developerId=dId,
                            nickName=ui.nickname, avatar=ui.headimgurl, sex=ui.sex,
                            country=ui.country,province=ui.province,city=ui.city))
                if im.error:
                    return im
            
            authUser = im.data
        else:
            authUser = im.data
            userId = authUser.userId
        # 存储日志
        im = authLogControl.add(AuthLog(openid=data.openid, userId=userId, code=code, accessToken=data.access_token, developerId=dId, authUserId=authUser.id))
        if im.error:
                return im
        
        return userId, data.openid
        # # 如果数据库中openid不存在，则添加openid和userId的绑定关系，并返回userId，否则直接返回userId
        # print(user_info)
        # return user_info
    
        
if __name__ == '__main__':
    
    print('authUserControl.table_name')