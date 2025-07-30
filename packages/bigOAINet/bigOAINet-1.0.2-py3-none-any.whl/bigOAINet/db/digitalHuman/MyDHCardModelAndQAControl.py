import uuid as uid
from peewee import *
import base64
import json
import os
import mxupy as mu
from mxupy import IM
from playhouse.shortcuts import model_to_dict
import bigOAINet as bigo
import random

class MyDHCardModelAndQAControl(mu.EntityXControl):

    class Meta:
        model_class = bigo.MyDHCardModelAndQA