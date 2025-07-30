import mxupy as mu
import bigOAINet as bigo
import uuid as uid

class UserControl(mu.EntityXControl):
    class Meta:
        model_class = bigo.User
        
    def check_accesstoken(self, userId, accessToken):
        """ 检查令牌

        Args:
            userId (int): 用户id
            accessToken (str): 令牌
        """
        def _do():
        
            im = mu.IM()
            
            if not accessToken:
                im.success = False
                im.msg = '访问令牌不能为空！'
                return im
            
            im = self.get_one_by_id(userId)
            if im.data is None:
                return im.set_error('用户不存在！')
            user = im.data
            im.data = ''
            
            if user.accessToken != accessToken:
                im.success = False
                im.msg = '访问令牌错误！'
                return im

            return im
    
        return self.run(_do)

    def is_admin(self, userId):
        """ 管理员否

        Args:
            userId (str): 用户id
        """
        def _do():
            
            im = self.get_one_by_id(userId)
            if im.data is None:
                return im.set_error('用户不存在！')
            user = im.data
            im.data = user.roles.split(',').contains('admin')
            return im
        
        return self.run(_do)

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
            
            im = self.exists({'username':username})
            if im.error:
                return im
            
            if im.data:
                return mu.IM(False, '用户名已经存在，请使用其他用户名！')
            
            im = self.add(
                bigo.User(
                    avatar="0",
                    username=username,
                    nickname=nickname,
                    password=password,
                    accessToken=uid.uuid4().hex,
                    roles="user"
                )
            )
            if im.error:
                return im
            user = im.data
            
            return mu.IM(True, '恭喜！注册成功。', user)

        return self.run(_do)

    def login(self, username, password):
        """ 登录

        Args:
            username (str): 用户名
            password (str): 密码
        """
        def _do():
            
            if not password:
                return mu.IM(False, '密码不能为空', code=500)
            
            im = self.get_one(where=[{'username':username},{'password':password}])
            if im.error:
                return im
            
            user = im.data
            if not user:
                return mu.IM(False, '用户名或密码错误！')

            # 更新令牌
            # user.accessToken = '1'
            user.accessToken = uid.uuid4().hex
            im = self.update_by_id(user.userId, user, 'accessToken')
            if im.error:
                return im
            
            return mu.IM(msg='登录成功！', data=user)

        return self.run(_do)

    def reset_password(self, userId):
        """ 重置密码

        Args:
            userId (int): 用户id
        """
        def _do():
            
            return self.update_by_id(userId, {'password':'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'})

        return self.run(_do)
    
    def update_by_kv(self, userId, key, value, accessToken):
        """ 用 key he value 修改用户

        Args:
            userId (int): 用户id
            key (str): 键，字段名
            value (any): 值
            accessToken (str): 访问令牌
            
        Returns:
            IM: 结果
        """
        def _do():
            
            im = UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im

            # 如果是更新默认屏幕，那先将所有屏幕置为非默认
            return self.update(where={
                'userId': userId
            }, model={
                key: value,
            })

        return self.run(_do)
    
    def change_password(self,userId, oldPWD, newPWD, accessToken):
        def _do():
            im = UserControl.inst().check_accesstoken(userId, accessToken)
            if im.error:
                return im

            im = self.exists({'userId':userId,'password': oldPWD})
            if im.error:
                return im

            return self.update(where={
                'userId': userId
            }, model={
                'password': newPWD
            })

        return self.run(_do)

    def logout(self,userId):
        def _do():
            return mu.IM(True)

        return self.run(_do)
        
if __name__ == '__main__':
    print(UserControl().inst().table_name)
    