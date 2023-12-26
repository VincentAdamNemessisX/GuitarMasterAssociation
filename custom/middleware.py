from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from custom import verify, data_handle
from user.models import User
from zone.models import Zone


class FrontEndLoginVerifyMiddleWare(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        db_zones = Zone.objects.all().filter(zone_status=1)
        request.session['zones'] = data_handle.db_to_json(request, db_zones)
        skip_url = ['admin']
        if request.path.strip().strip('/') == "favicon.ico":
            return HttpResponseRedirect('/static/fav.png')
        for item in skip_url:
            if item in request.path:
                return
        if request.session.get('login_username') is None:
            verify_url = ['post/update', 'api/post/upload/image', 'post/publish', 'user/update']
            if request.path.strip('/') in verify_url:
                return HttpResponseRedirect('/signin')
        else:
            (User.objects.filter(user_id=request.session.get('login_user_id'))
             .update(user_last_active_time=verify.get_current_time()))
