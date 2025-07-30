import mxupy as mu
from bigOAINet.db.member.m.Department import Department

class DepartmentControl(mu.EntityXControl):
    class Meta:
        model_class = Department
        
        
        
        
        
        
        
if __name__ == '__main__':
    
    print(DepartmentControl.inst().table_name)