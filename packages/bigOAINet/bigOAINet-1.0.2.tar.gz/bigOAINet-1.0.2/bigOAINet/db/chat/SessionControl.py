from mxupy import EntityXControl
import bigOAINet as bigo

class SessionControl(EntityXControl):
    class Meta:
        model_class = bigo.Session
        