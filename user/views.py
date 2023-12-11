from django.db.models.fields import json
from django.shortcuts import render, HttpResponseRedirect
from .models import User


# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(user_name=username).exists():
            user = User.objects.get(user_name=username)
            if user.user_password == password:
                request.session['login_username'] = user.user_name
                request.session['login_user_id'] = user.user_id
                request.session['login_user_status'] = user.user_status
                return HttpResponseRedirect('/index/')
            else:
                return render(request,'signin.html', {'error': '用户名或密码错误'})
        else:
            return render(request,'signin.html', {'error': '用户名或密码错误'})
    return render(request, 'signin.html')


def signup(request):
    return render(request, 'signup.html')