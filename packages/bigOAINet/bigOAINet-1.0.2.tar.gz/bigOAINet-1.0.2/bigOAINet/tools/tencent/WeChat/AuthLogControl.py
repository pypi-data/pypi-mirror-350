import mxupy as mu

from bigOAINet.tools.tencent.WeChat.m.AuthLog import *
class AuthLogControl(mu.EntityXControl):
    class Meta:
        model_class = AuthLog
        
    def printTableName(self):
        print(self.table_name)
        
        
if __name__ == '__main__':
    print('authLogControl.table_name')