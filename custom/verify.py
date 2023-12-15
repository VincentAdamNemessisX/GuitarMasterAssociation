from django.utils import timezone


def verify_current_user(request):
    if int(request.GET.get('user_id')) == int(request.session.get('login_user_id')):
        return True
    else:
        return False


def get_current_time():
    return timezone.now()
