import uuid as uid
from peewee import *
import base64
import json
import os
import mxupy as mu
from mxupy import IM
from playhouse.shortcuts import model_to_dict
from .m.models import *
import random

class MyCardModelAndCatechismControl(mu.EntityXControl):

    class Meta:
        model_class = MyCardModelAndCatechism