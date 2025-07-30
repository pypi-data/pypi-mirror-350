import mxupy as mu
from .m.Developer import Developer


class DeveloperControl(mu.EntityXControl):
    class Meta:
        model_class = Developer
        
        
        
        
        
        
global developerControl
developerControl = DeveloperControl()
        
if __name__ == '__main__':
    
    print(developerControl.table_name)