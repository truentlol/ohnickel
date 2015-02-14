from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect
import hashlib
from django import forms
import re
import os


from ohnickel.settings import PROJECT_ROOT

#1E41E17182126BECB331504414C93700
import json
from django.core.files.base import ContentFile
from django.http import HttpResponse

from ohnickel.models import User

from ohnickel.controllers.base import *
from ohnickel.models import *



import datetime
from django.utils.timezone import localtime


def test(request):



    forum = Forum.objects.get(id=1)

    context = {
        'json_test': model_to_dict(forum)
    }

    return render(request, 'test.html', context)



def index(request):



#
#Index html
#
#['DoesNotExist', 'Meta', 'MultipleObjectsReturned', 'REQUIRED_FIELDS', 'USERNAME_FIELD', '__class__', '__delattr__', '__dict__',
# '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', u'__module__', '__ne__', '__new__', '__reduce__',
# '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_base_manager',
# '_default_manager', '_deferred', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order',
# '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state',
# 'check_password', 'clean', 'clean_fields', 'date_error_message', 'date_joined', 'delete', 'email', 'email_user', 'first_name', 'full_clean', 'get_absolute_url',
# 'get_all_permissions', 'get_full_name', 'get_group_permissions', 'get_next_by_date_joined', 'get_next_by_last_login', 'get_previous_by_date_joined', 'get_previous_by_last_login',
# 'get_profile', 'get_short_name', 'get_username', 'groups', 'has_module_perms', 'has_perm', 'has_perms', 'has_usable_password', 'id', 'is_active', 'is_anonymous', 'is_authenticated',
# 'is_staff', 'is_superuser', 'last_login', 'last_name', 'logentry_set', 'natural_key', 'objects', 'password', 'pk', 'prepare_database_save', 'save', 'save_base', 'serializable_value',
# 'set_password', 'set_unusable_password', 'unique_error_message', 'user_permissions', 'username', 'validate_unique']
#




    user = get_current_user(request)






    context = {
        'index': 'lol',
        'msg': '',
        'sesh': request.user.email,
        'user': user
    }
    return render(request, 'index.html', context)








def get_current_utc():
    from datetime import datetime
    from dateutil import tz

    from_zone = tz.tzutc()

    utc = datetime.utcnow()
    utc = utc.replace(tzinfo=from_zone)
    return utc



