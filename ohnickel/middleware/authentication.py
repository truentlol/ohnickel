
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
from ohnickel.models import User

from social_auth.db.django_models import UserSocialAuth



def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        try:
            social_auth_user = UserSocialAuth.objects.get(id=request.user.id)
        except:
            print "ERROR GETTING SOCIAL AUTH USER WITH USER ID: " + str(request.user.id)
            return


        #See if a a custom user object has already been created for this user
        try:
            user = User.objects.get(uid=social_auth_user.uid)

        except:
            #user doesnt exist, create
            user = User(username=social_auth_user.user,uid=social_auth_user.uid, email=request.user.email)
            user.save()


            print "User does not exist in session"
            return



        #request.user = user