from django.shortcuts import render
from user.models import User


# Create your views here.
def index(request):
    current_user = User.objects.get(user_name=request.session.get('login_username'))
    return render(request,  'index.html', {'login_user': current_user})
