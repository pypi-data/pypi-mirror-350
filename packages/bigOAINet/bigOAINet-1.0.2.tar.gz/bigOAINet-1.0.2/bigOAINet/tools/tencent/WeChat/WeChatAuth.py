from fastapi import Request, Response
from fastapi.responses import HTMLResponse
import hashlib
import hmac
import base64

from fastapi import APIRouter
router = APIRouter()

# https://api.bigoainet.com/wechat_callback

class WeChatAuth:
    """ 微信授权
        参考网址：https://mp.weixin.qq.com/
        需要设置的点：
            设置与开发 基本配置 公众号开发信息(AppId、AppSecret、白名单)
            设置与开发 基本配置 服务器配置（服务器回调地址、令牌、消息加解密密钥）
            设置与开发 公众号设置 功能设置 (网页域名设置)
    """
    
    def __init__(self, callback, token, encoding_aes_key):
        """ 

        Args:
            callback (str): 回调路径
            token (str): _description_. Defaults to ''.
            encoding_aes_key (str): _description_. Defaults to ''.
        """
        # https://api.bigoainet.com/wechat_callback
        # juyinliang1021 
        # 3dIPCljS02l773adcr8OiZzqL2aVXaZRQY22tsypAb6
        
    def auth(self, domain, type='snsapi_base', state=None):
        """ 用户授权

        Args:
            domain (str): 回调域名
            type (str): 回调类型 snsapi_base, snsapi_userinfo
            state (str): 用户自定义参数
        """
        from weixin.login import WeixinLogin
        from fastapi.responses import RedirectResponse
        # 这两个值应该要去数据库中获取
        wx_login = WeixinLogin('wx106361bfe14c4515', 'ed63832c0be62b52d95872846ff4765e')
        url = wx_login.authorize(domain + 'wechat_authed', type, state)
        print(url)
        return RedirectResponse(url)
        
    def authed(self, code):
        """ 用户授权回调

        Args:
            callback (str): 回调路径
            token (str): _description_. Defaults to ''.
            encoding_aes_key (str): _description_. Defaults to ''.
        """
        from weixin.login import WeixinLogin
        # 这两个值应该要去数据库中获取
        wx_login = WeixinLogin('wx106361bfe14c4515', 'ed63832c0be62b52d95872846ff4765e')
        data = wx_login.access_token(code)
        print(data)
        # 如果数据库中openid不存在，则添加openid和userId的绑定关系，并返回userId，否则直接返回userId
        
        
        
        user_info = wx_login.user_info(data.access_token, data.openid)
        print(user_info)
        return user_info
    
@app.get("/wechat_auth")
async def wechat_auth(request: Request):
    from fastapi.responses import RedirectResponse
    from tencent.WeChat.db.c.AuthUserControl import authUserControl
    url = authUserControl.auth(request.base_url, 1, request.query_params.get('type', 'snsapi_userinfo'), request.query_params.get('state', ''))
    return RedirectResponse(url)

@app.get("/wechat_authed")
async def wechat_authed(request: Request):
    print(request.query_params)
    from tencent.WeChat.db.c.AuthUserControl import authUserControl
    authUserControl.authed(request.query_params.get('code'), 'developerId=' + request.query_params.get('state'))

if __name__ == "__main__":
    print('a')