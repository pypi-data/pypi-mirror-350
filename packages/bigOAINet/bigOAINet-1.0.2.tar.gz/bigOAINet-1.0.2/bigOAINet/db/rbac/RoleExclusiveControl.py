import mxupy as mu
from bigOAINet.db.rbac.m.RoleExclusive import RoleExclusive

class RoleExclusiveControl(mu.EntityXControl):
    class Meta:
        model_class = RoleExclusive
