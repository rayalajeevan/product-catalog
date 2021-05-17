from sqlalchemy.sql.elements import UnaryExpression
from .models import *

class SerilizerMixin:
    
    def serialize(qs,many=False,unwanted_keys=list()):
        if many:
            objs=list()
            for obj in qs:
                obj_dict=dict()
                for key,value in obj.__dict__.items():
                    if "_sa_instance_state" not in key and key not in unwanted_keys:
                        obj_dict[key]=value
                objs.append(obj_dict)
            return objs
        else:
            obj_dict=dict()
            list(map(lambda x:obj_dict.update({x:qs.__dict__[x]})  if "_sa_instance_state" not in x and x not in unwanted_keys else False,qs.__dict__.keys()))
            return obj_dict