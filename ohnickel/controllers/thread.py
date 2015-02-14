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





def view(request, thread_id):
    thread = Thread.objects.get(id=thread_id)



    context = {
        'thread_id': thread_id,
        'thread': thread
    }

    return render(request, 'thread.html', context)



def create(request):
    if request.method == 'POST':

        if 'thread_name' not in request.POST or 'forum_id' not in request.POST:
            data = {'success': False, 'error_id': 1 ,'error_msg': 'All data not set'}
            return HttpResponse(json.dumps(data), 'application/json')


        #Make sure this user is logged in
        user = get_current_user(request)

        if not user:
            data = {'success': False, 'error_id': 2 ,'error_msg': 'User not logged in'}
            return HttpResponse(json.dumps(data), 'application/json')

        #make sure the user is an admin
        if user.is_admin is False:
            data = {'success': False, 'error_id': 3 ,'error_msg': 'User is not authorized to create a thread'}
            return HttpResponse(json.dumps(data), 'application/json')


        forum_id = request.POST['forum_id']

        try:
            forum = Forum.objects.get(id=forum_id)
        except:
            data = {'success': False, 'error_id': 4 ,'error_msg': 'Forum with ' + forum_id + " doesnt exist"}
            return HttpResponse(json.dumps(data), 'application/json')




        thread_name = request.POST['thread_name']





        thread = Thread(name=thread_name, forum=forum, user=user)
        thread.save()



        data = {'success': True, 'thread': model_to_dict(thread)}
        return HttpResponse(json.dumps(data), 'application/json')

    else:
        data = {'success': False, 'error_msg': 'request must be post'}
        return HttpResponse(json.dumps(data), 'application/json')


