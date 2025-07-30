import mxupy as mu
from ..m.User import User

class UserControl(mu.EntityXControl):
    class Meta:
        model_class = User
        
        
        
        
        
        
global userControl
userControl = UserControl()
        
if __name__ == '__main__':
    
    print(userControl.table_name)