from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Sum
from custom import verify
from .models import User


# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(user_name=username).exists():
            user = User.objects.get(user_name=username)
            if check_password(password, user.user_password):
                if user.user_status == 0:
                    return render(request,'signin.html', {'error': '该用户已被禁用'})
                if user.user_status == 2:
                    return render(request,'signin.html', {'error': '该用户已被冻结'})
                if user.user_status == 1:
                    request.session['login_username'] = user.user_name
                    request.session['login_user_id'] = user.user_id
                    User.objects.filter(user_id=user.user_id).update(user_last_active_time=verify.get_current_time())
                    return HttpResponseRedirect('/index/')
                else:
                    return render(request,'signin.html', {'error': '未知错误'})
            else:
                return render(request, 'signin.html', {'error': '用户名或密码错误'})
        else:
            return render(request, 'signin.html', {'error': '用户名或密码错误'})
    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = make_password(request.POST.get('password'))
        sex = request.POST.get('sex')
        headicon = request.POST.get('headicon')
        if User.objects.filter(user_name=username).exists():
            return render(request, 'signup.html', {'error': '用户名已存在'})
        else:
            if User.objects.create(user_name=username, user_email=email, user_phone=phone, user_password=password,
                                   user_sex=sex, user_headicon=headicon):
                return render(request, 'signin.html', {'success': '注册成功'})
            return render(request, 'signup.html', {'error': '注册失败'})
    return render(request, 'signup.html')


def signout(request):
    request.session.pop('login_username', None)
    request.session.pop('login_user_id', None)
    request.session.clear_expired()
    return HttpResponseRedirect('/')


def user(request):
    current_user = verify.verify_current_user(request)
    if request.method == 'GET':
        userid = request.GET.get('userid')
        if userid:
            user = User.objects.get(user_id=userid)
            user.user_view = user.post_set.aggregate(Sum('post_view')).get('post_view__sum')
            user.user_like = user.post_set.aggregate(Sum('post_like')).get('post_like__sum')
            user.user_favorite = user.post_set.aggregate(Sum('post_favorite')).get('post_favorite__sum')
            return render(request, 'user.html', {'user': user, 'login_user': current_user})
        else:
            return render(request, 'user.html', {'error': '请传入用户id', 'login_user': current_user})
