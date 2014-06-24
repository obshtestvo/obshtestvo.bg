import pickle
from django.contrib.messages.api import get_messages, constants
from django.forms import model_to_dict
from django.utils.datastructures import MultiValueDict

def get_updated_data(instance, new_data):
    data = model_to_dict(instance)
    data.update(dict(new_data))
    return MultiValueDict(data)

def errors(request):
    errors = {}
    for message in get_messages(request):
        if message.level == constants.ERROR:
            errors = dict(errors, **pickle.loads(message.message))
    return errors