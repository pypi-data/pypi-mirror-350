import mxupy as mu
from bigOAINet.db.rbac.m.RightAndData import RightAndData

class RightAndDataControl(mu.EntityXControl):
    class Meta:
        model_class = RightAndData
        