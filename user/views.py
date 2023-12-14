import json

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Sum

from collection.models import Collection
from custom import verify, data_handle
from post.models import Post
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
            user.user_collection = user.collection_set.filter(user_id=userid).count()
            user.post = user.post_set.order_by('-post_create_time')
            user.post_count = user.post_set.count()
            user.collection = user.collection_set.order_by('-collection_create_time')
            user.collection_count = user.collection_set.count()
            if user.collection_count > 6:
                user.collection = user.collection[:6]
            user.recent = user.recentbrowsing_set.order_by('-recent_create_time')[:10]
            user.recent_count = user.recentbrowsing_set.count()
            user.post = user.post_set.order_by('-post_create_time')
            user.post_count = user.post_set.count()
            return render(request, 'user.html', {'user': user, 'login_user': current_user})
        else:
            return render(request, 'user.html', {'error': '请传入用户id', 'login_user': current_user})


def user_collection_more(request):
    current_user = verify.verify_current_user(request)
    if request.method == 'POST':
        userid = request.POST.get('user_id')
        if userid:
            user_collections = User.objects.get(user_id=userid).collection_set.order_by('-collection_create_time')
            # Get all post IDs associated with the user's collections
            post_ids = user_collections.values_list('post_id', flat=True)
            # Retrieve all posts associated with the user's collections
            associated_collection_posts = Post.objects.filter(post_id__in=post_ids).order_by('-post_create_time')[6:]
            return data_handle.db_to_json2(request, associated_collection_posts)
    return render(request, '500.html', {'error': '用户访问异常', 'login_user': current_user})
