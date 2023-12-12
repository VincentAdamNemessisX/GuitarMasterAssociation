from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class FrontEndLoginVerifyMiddleWare(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.path.strip().strip('/') == "favicon.ico":
            return HttpResponseRedirect('/static/fav.png')
        if 'admin' in request.path:
            return
        if request.session.get('login_username') is None:
            skip_url = ['signin', 'signup', 'signout', '404', '500']
            if not (request.path.strip().strip('/') in skip_url):
                return HttpResponseRedirect('/signin')
