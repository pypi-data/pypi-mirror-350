from fastapi import Request, Response
from fastapi.responses import HTMLResponse
import hashlib
import hmac
import base64


from fastapi import APIRouter
router = APIRouter()

# https://api.bigoainet.com/wechat_callback

class WeChat:
    """ 微信授权
        参考网址：https://mp.weixin.qq.com/
        需要设置的点：
            设置与开发 基本配置 公众号开发信息(AppId、AppSecret、白名单)
            设置与开发 基本配置 服务器配置（服务器验证地址、令牌、消息加解密密钥）
            设置与开发 公众号设置 功能设置 (网页域名设置)
    """
    TOKEN = "juyinliang1021"
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
        
    @staticmethod
    def check_signature(token, timestamp, nonce, signature):
        """ 校验（第一次配置回调界面时会用到）

        Args:
            token (_type_): _description_
            timestamp (_type_): _description_
            nonce (_type_): _description_
            signature (_type_): _description_

        Returns:
            _type_: _description_
        """
        # 对 token、timestamp、nonce 进行字典序排序并拼接
        sort_list = [token, timestamp, nonce]
        sort_list.sort()
        sort_str = ''.join(sort_list)

        # 进行 sha1 加密
        hashcode = hashlib.sha1()
        hashcode.update(sort_str.encode('utf-8'))
        hashcode = hashcode.hexdigest()

        # 判断加密后的字符串是否与 signature 一致
        if hmac.compare_digest(hashcode, signature):
            return True
        else:
            return False
    
@router.get("/wechat_callback")
async def wechat_callback(request: Request):
    
    signature = request.query_params.get("signature")
    timestamp = request.query_params.get("timestamp")
    nonce = request.query_params.get("nonce")
    echo_str = request.query_params.get("echoStr")
    
    if WeChat.check_signature(WeChat.TOKEN, timestamp, nonce, signature):
        return HTMLResponse(content=echo_str)
    else:
        return Response(content="认证失败", status_code=403)

if __name__ == "__main__":
    print('a')