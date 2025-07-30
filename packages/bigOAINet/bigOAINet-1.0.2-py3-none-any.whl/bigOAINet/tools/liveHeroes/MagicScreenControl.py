import mxupy as mu

from mxupy import IM

from liveheroes.m.Models import MagicScreen
from liveheroes.UserControl import UserControl


class MagicScreenControl(mu.EntityXControl):

    class Meta:
        model_class = MagicScreen

    def get_default(self, userId):
        """ 获取默认魔屏

        Args:
            userId (int): 用户id

        Returns:
            IM: 结果
        """
        def _do():

            return self.get_one(
                where=[
                    {'userId': userId},
                    {'isDefault': True}
                ])

        return self.run(_do)

    def set_default(self, magicScreenId, userId):
        """ 设置默认魔屏

        Args:
            magicScreenId (int): 魔屏id
            userId (int): 用户id

        Returns:
            IM: 结果
        """
        def _do():

            im = self.get_one_by_id(magicScreenId)
            if im.check_data().error:
                return im
            screen = im.data

            if screen.userId != userId:
                return IM(False, '设置默认魔屏失败，此魔屏不属于此用户。')

            # 将用户所有魔屏设为 false
            im = self.update({'userId': userId}, {'isDefault': False})
            if im.error:
                return im

            im = self.update_by_id(magicScreenId, {'isDefault': True})
            if im.error:
                return im

            return im

        return self.run(_do)

    def add_or_update(self, model):
        """ 添加或修改

        Args:
            model (Model): 魔屏

        Returns:
            IM: 结果
        """
        sup = super()

        def _do():
            if model.magicScreenId != -1:
                im = self.update(where={'userId': model.userId}, model={
                                 'isDefault': False})
                if im.error:
                    return im

            model.isDefault = True
            return sup.add_or_update(model)

        return self.run(_do)

    def update_by_kv(self, magicScreenId, userId, key, value, accesstoken):
        """ 用 key he value 修改魔屏

        Args:
            magicScreenId (int): 魔屏id
            userId (int): 用户id
            key (str): 键，字段名
            value (any): 值
            accesstoken (str): 访问令牌

        Returns:
            IM: 结果
        """
        def _do():

            im = UserControl.inst().check_accesstoken(userId, accesstoken)
            if im.error:
                return im

            # 如果是更新默认屏幕，那先将所有屏幕置为非默认
            if key == "isDefault":
                im = self.update(where={
                    'userId': userId
                }, model={
                    key: False,
                })
                if im.error:
                    return im

            return self.update(where={
                'magicScreenId': magicScreenId
            }, model={
                key: value,
            })

        return self.run(_do)

    def get_list(self, select=None, where=None, order_by=None, group_by=None, having=None, limit=None, offset=None, to_dict=False, recurse=False, backrefs=False, max_depth=1):
        """ 获取默认魔屏

        Args:
            userId (int): 用户id

        Returns:
            IM: 结果
        """
        sup = super()

        def _do():

            im = sup.get_list(select=select, where=where, order_by=order_by, group_by=group_by, having=having,
                              limit=limit, offset=offset, to_dict=to_dict, recurse=recurse, backrefs=backrefs, max_depth=max_depth)
            for m in im.data:
                print(m.isDefault)
                print(m.name)
                print(m)
            return im

        return self.run(_do)
