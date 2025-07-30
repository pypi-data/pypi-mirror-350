import uuid as uid
from peewee import *
from datetime import datetime, timedelta
import mxupy as mu
from playhouse.shortcuts import model_to_dict
from .m.models import *


class NewsControl(mu.EntityXControl):

    class Meta:
        model_class = News