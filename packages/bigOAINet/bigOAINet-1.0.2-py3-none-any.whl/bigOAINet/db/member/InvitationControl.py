import mxupy as mu
from bigOAINet.db.member.m.Invitation import Invitation

class InvitationControl(mu.EntityXControl):
    class Meta:
        model_class = Invitation
        
        
   