import mxupy as mu
from bigOAINet.db.rbac.m.RoleAndRight import RoleAndRight

class RoleAndRightControl(mu.EntityXControl):
    class Meta:
        model_class = RoleAndRight
