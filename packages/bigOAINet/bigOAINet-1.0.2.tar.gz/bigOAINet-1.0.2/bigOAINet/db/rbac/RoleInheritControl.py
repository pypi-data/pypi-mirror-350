import mxupy as mu
from bigOAINet.db.rbac.m.RoleInherit import RoleInherit

class RoleInheritControl(mu.EntityXControl):
    class Meta:
        model_class = RoleInherit
