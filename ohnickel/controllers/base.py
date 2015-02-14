


from social_auth.db.django_models import UserSocialAuth
from ohnickel.models import User





import json


def models_to_dict(model_list):
    list = []
    for model in model_list:
        list.append(model_to_dict(model))

    return list



def model_to_dict(model):

    from django.core import serializers

    serial_obj = serializers.serialize('json', [model])
    obj_as_dict = json.loads(serial_obj)[0]['fields']
    obj_as_dict['id'] = model.pk
    return obj_as_dict


    #
    #
    #model_dict = {}
    #for field, value in model.items:
    #    model_dict.update({field: value})
    #
    #return model_dict





def get_current_social_auth_user(request):
    try:
        social_auth_user = UserSocialAuth.objects.get(id=request.user.id)

        return social_auth_user
    except:
        print "User does not exist in session"
        return None


def get_current_user(request):
    try:
        social_auth_user = get_current_social_auth_user(request)
        if social_auth_user:
            user = User.objects.get(uid=social_auth_user.uid)
            return user
        else:
            return None

    except:
        print "User does not exist in session"
        return None
