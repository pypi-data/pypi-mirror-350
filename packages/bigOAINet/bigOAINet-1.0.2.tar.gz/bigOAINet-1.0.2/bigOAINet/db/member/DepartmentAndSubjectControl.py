import mxupy as mu
from bigOAINet.db.member.m.DepartmentAndSubject import DepartmentAndSubject

class DepartmentAndSubjectControl(mu.EntityXControl):
    class Meta:
        model_class = DepartmentAndSubject
        
        
        
        
        
        
        
if __name__ == '__main__':
    
    print(DepartmentAndSubjectControl.inst().table_name)