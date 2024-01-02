import json
import os
from datetime import datetime

from django.forms.models import model_to_dict
from django.http import HttpResponse


def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError("Type not serializable")


def db_to_json2(request, data):
    return HttpResponse(json.dumps(db_to_json(request, data)), content_type="application/json")


def db_to_json(request, data):
    # Convert QuerySet to list of model instances
    model_instances = list(data)
    # Convert datetime objects to a serializable format directly on model instances
    serialized_data = [
        {key: convert_datetime(value) if isinstance(value, datetime) else getattr(value, 'url', value)
         for key, value in model_to_dict(model_instance).items()}
        for model_instance in model_instances
    ]

    # Construct the result dictionary
    result = {"message": 'success', "code": '200', "data": serialized_data}
    # result = serialized_data
    # Convert to JSON and return the response
    # print(result)
    return result


def handle_uploaded_headicon(f, username):
    path = "media/user_headicon/" + username + "." + f.name.split('.')[1]
    with open(path, "wb") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path


def handle_uploaded_image(f):
    path = str("media/post/" + datetime.now().strftime('%Y') + "/" + datetime.now().strftime('%m'))
    if not os.path.exists(path):
        os.makedirs(path)
    # print(datetime.now().strftime('%Y-%m-%d-%h-%m'))
    path = ("media/post/" + str(datetime.now().strftime('%Y')) + "/"
            + str(datetime.now().strftime('%m')) +
            "/" + str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S-')) + f.name)
    with open(path, "wb") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path
