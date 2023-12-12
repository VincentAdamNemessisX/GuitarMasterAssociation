from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class FrontEndLoginVerifyMiddleWare(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        skip_url = ['admin']
        if request.path.strip().strip('/') == "favicon.ico":
            return HttpResponseRedirect('/static/fav.png')
        for item in skip_url:
            if item in request.path:
                return
        if request.session.get('login_username') is None:
            verify_url = ['user']
            if request.path.strip('/') in verify_url:
                return HttpResponseRedirect('/signin')
