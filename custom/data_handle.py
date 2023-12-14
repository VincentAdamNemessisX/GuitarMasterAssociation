import json
from datetime import datetime

from django.forms.models import model_to_dict
from django.http import HttpResponse


def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError("Type not serializable")


def db_to_json2(request, data):
    # Convert QuerySet to list of model instances
    model_instances = list(data)

    # Convert datetime objects to a serializable format directly on model instances
    serialized_data = [
        {key: convert_datetime(value) if isinstance(value, datetime) else getattr(value, 'url', value)
         for key, value in model_to_dict(model_instance).items()}
        for model_instance in model_instances
    ]

    # Construct the result dictionary
    result = {"message": 'success', "code": '0', "data": serialized_data}

    # Convert to JSON and return the response
    return HttpResponse(json.dumps(result), content_type="application/json")
