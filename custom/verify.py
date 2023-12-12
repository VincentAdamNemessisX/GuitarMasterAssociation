from user.models import User


def verify_current_user(request):
    current_username = None
    if request.session.get('login_username') is not None:
        current_username = request.session.get('login_username')
    if current_username is None:
        current_user = None
    else:
        current_user = User.objects.get(user_name=current_username)
        if current_user.user_nickname:
            current_user.user_name = current_user.user_nickname
    return current_user
