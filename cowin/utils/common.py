import os
import sys
import json


def load_json(json_file):
    if os.path.exists(json_file):
        with open(json_file) as jsfile:
            data = json.load(jsfile)
            return(data)

    return False


def singleton(class_name):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_name not in instances:
            instances[class_name] = class_name(*args, **kwargs)
        return instances[class_name]
    return getinstance
