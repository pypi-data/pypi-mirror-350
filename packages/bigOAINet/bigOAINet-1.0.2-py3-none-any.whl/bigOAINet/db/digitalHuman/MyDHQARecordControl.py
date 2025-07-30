import uuid as uid
from peewee import *
import base64
import json
import os
import mxupy as mu
import bigOAINet as bigo
from playhouse.shortcuts import model_to_dict
import random

class MyDHQARecordControl(mu.EntityXControl):

    class Meta:
        model_class = bigo.MyDHQARecord