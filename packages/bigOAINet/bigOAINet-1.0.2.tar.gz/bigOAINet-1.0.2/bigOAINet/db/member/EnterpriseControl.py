import mxupy as mu
from bigOAINet.db.member.m.Enterprise import Enterprise

class EnterpriseControl(mu.EntityXControl):
    class Meta:
        model_class = Enterprise
        
        
        