from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User
import logging

class MITAuthBackend(RemoteUserBackend):
    def clean_username(self, username):
        if '@' in username:
            name, domain = username.split('@')
            assert domain.upper() == 'MIT.EDU'
            return name
        else:
            return username

    def authenticate(self, remote_user=None):
       # raise Exception(remote_user)
        logging.info('autheticate(' + remote_user + ')')
        try:
            user = User.objects.get(username=remote_user)
            return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        logging.info('get_user(' + str(user_id) + ')')
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class MITAuthMiddleware(RemoteUserMiddleware):
    header = "SSL_CLIENT_S_DN_Email"

    def clean_username(self, username, request):
        if '@' in username:
            name, domain = username.split('@')
            assert domain.upper() == 'MIT.EDU'
            return name
        else:
            return username


    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, MITAuthBackend):
                        auth.logout(request)
                except ImportError:
                    # backend failed to load
                    auth.logout(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.get_username() == self.clean_username(username, request):
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        #raise Exception(self.clean_username(username, request))
        user = auth.authenticate(username=self.clean_username(username, request), password='PASSWORD')
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)
        else:
            user = User.objects.create_user(self.clean_username(username, request), username, 'PASSWORD')
            user.first_name = request.META['SSL_CLIENT_S_DN_CN']
            user.save()
            user = auth.authenticate(username=self.clean_username(username, request), password='PASSWORD')
            request.user = user
            auth.login(request, user)
