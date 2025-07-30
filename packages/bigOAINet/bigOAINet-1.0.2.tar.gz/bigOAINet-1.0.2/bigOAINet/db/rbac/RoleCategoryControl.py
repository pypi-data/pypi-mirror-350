import mxupy as mu
from bigOAINet.db.rbac.m.RoleCategory import RoleCategory

class RoleCategoryControl(mu.EntityXControl):
    class Meta:
        model_class = RoleCategory
