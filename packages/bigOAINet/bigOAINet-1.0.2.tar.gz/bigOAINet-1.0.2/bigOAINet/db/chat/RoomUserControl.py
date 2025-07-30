from mxupy import EntityXControl
import bigOAINet as bigo

class RoomUserControl(EntityXControl):
    class Meta:
        model_class = bigo.RoomUser
        