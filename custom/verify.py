from datetime import datetime


def verify_current_user(request):
    if request.session.get('login_user_id') is None:
        return False
    if int(request.GET.get('user_id')) == int(request.session.get('login_user_id')):
        return True
    else:
        return False


def get_current_time():
    return datetime.now()
