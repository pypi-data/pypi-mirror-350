import random

import uuid as uid
import mxupy as mu

from mxupy import IM, read_server
from base.member import UserControl as UserControlX
from tools.liveHeroes.m.Models import *

# config = {
#     "livingBrowserServers": ["http://121.41.171.54:7865", "http://121.43.155.193:7865", "http://120.55.194.130:7865"]
# }


class UserControl(UserControlX):

    def register(self, username, nickname, password):
        """ 注册

        Args:
            username (str): 用户名
            nickname (str): 昵称
            password (str): 密码
        """
        def _do():

            # 不能在外面导入，因为这些 Control 都导入了用户 Control，
            # 放在顶部导入会引起循环导入
            from tools.liveHeroes.ShopControl import ShopControl
            from tools.liveHeroes.AudioWordControl import AudioWordControl
            from tools.liveHeroes.AudioWordFolderControl import AudioWordFolderControl

            im = super().register(username, nickname, password)
            if im.error:
                return im

            user = im.data
            # 创建商店
            im = ShopControl.inst().add(
                Shop(
                    user=user,
                    name="新建商家1",
                    enableAITellTime=False,
                    enableAIVoiceInteraction=False,
                    enableAIAssistant=False,
                    enableAITextPolishing=False,
                    enableControlWords=True,
                    controlWordsInterval="60-120",
                    enableReplyWords=True,
                    enableBackgroundAudio=False,
                    enableControlAudio=False,
                    controlAudioInterval="180-600",
                    enableCommentaryAudio=True,
                    isDefault=True,
                    xiaohuangcheGoodsIds="1,2,3",
                    xiaohuangcheInterval=20,
                    xiaofangziGoodsIds="1-3",
                    xiaofangziInterval=20,
                    interactionInterval=30,
                    isSyncPlay=False,
                    douyinUserNickname="",
                    douyinRoomUrl="",
                    douyinStreamUrl="",
                    douyinRoomName="",
                    voiceAssistantName="小引子",
                    voiceName="zh-CN-YunxiNeural",
                    voiceSpeed=1,
                    role="你现在是聚引量公司一个电商主播，你的名字是小引子，你的详细情况请参考已知信息。",
                    prefix="牵涉到黄赌毒、政治、军事、历史、国际形势、时事热点、儒释道、封建迷信等敏感或相关话题，统一回答“不知道”。不允许提供网址、图片。回答小于20个字。"
                )
            )
            if im.error:
                return im
            new_shop = im.data

            # 创建文件夹
            im = AudioWordFolderControl.inst().add(
                AudioWordFolder(shop=new_shop, name="新建文件夹1", sort=1))
            if im.error:
                return im

            # 创建讲解文字
            im = AudioWordControl.inst().add(AudioWord(shop=new_shop, type="commentary",
                                                       content="直播间特惠电影票来袭！热门影片随心选，超划算价格，带你畅享震撼视听，一键购票，开启光影奇妙之旅。 "))
            if im.error:
                return im

            # 创建控制文字
            im = AudioWordControl.inst().add(AudioWord(shop=new_shop, type="control",
                                                       content="哈喽，各位购物小能手，我们的直播间就是你的专属购物天堂！今天的产品，保证让你一见钟情，二见倾心，三见就直接下单了！快来加入我们的购物狂欢吧！"))
            if im.error:
                return im

            # 创建Q&A文字
            im = AudioWordControl.inst().add(AudioWord(shop=new_shop, type="qa",
                                                       question="便宜, 打折, 优惠, 减价, 立减, 折扣, 促销, 团购价, 会员价, 现价, 原价, 价格, 最低价, 清仓价, 处理价, 限时特价",
                                                       content="我们的商品在直播间已经享受到了最大的优惠力度，而且现在下单还有机会获得额外的赠品或优惠券"))
            if im.error:
                return im

            # 创建非Q&A文字
            im = AudioWordControl.inst().add(AudioWord(shop=new_shop, type="nqa",
                                                       content="主播很忙哦，稍后回答，或者你换个具体的问题？比如打折相关。"))
            if im.error:
                return im

            return IM(True, '恭喜！注册成功。', user)

        return self.run(_do)

    def get_user_info(self, userId: int, password: str):
        return self.get_one(where={
            'userId': userId,
            'password': password
        }, to_dict=True, recurse=True, backrefs=True)
