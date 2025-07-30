import json
from django.db.models import Model
from django.forms.models import model_to_dict


def model_to_json(model, **kwargs):
    return json.dumps(model_to_data(model), ensure_ascii=False, **kwargs)


def model_to_data(model):
    return sure_model_data(model_to_dict(model))


def sure_model_data(data):
    if isinstance(data, dict):
        for k in list(data):
            v = data[k]
            if isinstance(v, Model):
                data[k] = model_to_data(data[k])
            elif isinstance(v, (dict, list)):
                data[k] = sure_model_data(data[k])
    elif isinstance(data, list):
        for index, item in enumerate(data):
            if isinstance(item, Model):
                data[index] = model_to_data(item)
            elif isinstance(item, (dict, list)):
                data[index] = sure_model_data(item)
    return data
