import mxupy as mu
from bigOAINet.db.rbac.m.Right import Right

class RightControl(mu.EntityXControl):
    class Meta:
        model_class = Right
