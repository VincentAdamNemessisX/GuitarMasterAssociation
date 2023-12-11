from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class FrontEndLoginVerifyMiddleWare(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.session.get('login_username') is None:
            if request.path.strip('/') != 'signin':
                return HttpResponseRedirect('/signin')
