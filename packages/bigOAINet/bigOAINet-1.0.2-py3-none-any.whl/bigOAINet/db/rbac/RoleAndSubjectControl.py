import mxupy as mu
from bigOAINet.db.rbac.m.RoleAndSubject import RoleAndSubject

class RoleAndSubjectControl(mu.EntityXControl):
    class Meta:
        model_class = RoleAndSubject
