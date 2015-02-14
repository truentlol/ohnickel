from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponseRedirect
import hashlib
from django import forms
import re
import os

from ohnickel.controllers.base import *


from ohnickel.settings import PROJECT_ROOT

import json
from django.core.files.base import ContentFile
from django.http import HttpResponse

from ohnickel.models import *





def view(request, forum_id):
    forum = Forum.objects.get(id=forum_id)



    context = {
        'forum_id': forum_id,
        'forum': forum
    }

    return render(request, 'forum.html', context)



def create(request):
    if request.method == 'POST':

        if 'forum_name' not in request.POST or 'forum_description' not in request.POST or 'forum_sticky' not in request.POST:
            data = {'success': False, 'error_id': 1 ,'error_msg': 'All data not set'}
            return HttpResponse(json.dumps(data), 'application/json')


        #Make sure this user is logged in
        user = get_current_user(request)

        if not user:
            data = {'success': False, 'error_id': 2 ,'error_msg': 'User not logged in'}
            return HttpResponse(json.dumps(data), 'application/json')

        #make sure the user is an admin
        if user.is_admin is False:
            data = {'success': False, 'error_id': 3 ,'error_msg': 'User is not authorized to create a forum'}
            return HttpResponse(json.dumps(data), 'application/json')



        forum_name = request.POST['forum_name']
        forum_description = request.POST['forum_description']
        forum_sticky = request.POST['forum_sticky']


        forum = Forum(name=forum_name, description=forum_description, sticky=forum_sticky, user=user)
        forum.save()



        data = {'success': True, 'forum': model_to_dict(forum)}
        return HttpResponse(json.dumps(data), 'application/json')

    else:
        data = {'success': False, 'error_msg': 'request must be post'}
        return HttpResponse(json.dumps(data), 'application/json')






def threads(request, forum_id):
    forum = Forum.objects.get(id=forum_id)

    data = {'success': True, 'threads':models_to_dict(forum.threads.all())}
    return HttpResponse(json.dumps(data), 'application/json')



def forums(request):

    forums = Forum.objects.all()




    data = {'success': True, 'forums':models_to_dict(forums)}
    return HttpResponse(json.dumps(data), 'application/json')