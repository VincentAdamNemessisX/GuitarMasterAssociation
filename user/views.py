from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, HttpResponseRedirect

from custom import verify, data_handle
from custom.goto_controller import redirect_referer
from post.models import Post
from .get import get_specific_user
from .models import User


# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(user_name=username).exists():
            login_user = User.objects.get(user_name=username)
            if check_password(password, login_user.user_password):
                if login_user.user_status == 0:
                    return render(request, 'signin.html', {'error': '该用户已被禁用'})
                if login_user.user_status == 2:
                    return render(request, 'signin.html', {'error': '该用户已被冻结'})
                if login_user.user_status == 1:
                    request.session['login_username'] = login_user.user_name
                    request.session['login_user_id'] = login_user.user_id
                    request.session['login_user_headicon'] = login_user.user_headicon.url
                    request.session.set_expiry(60 * 60)
                    User.objects.filter(user_id=login_user.user_id).update(
                        user_last_active_time=verify.get_current_time())
                    return HttpResponseRedirect('/index/')
                else:
                    return render(request, 'signin.html', {'error': '未知错误'})
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


@redirect_referer
def signout(request):
    request.session.pop('login_username', None)
    request.session.pop('login_user_id', None)
    request.session.clear_expired()


def user(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if user_id:
            login_user = get_specific_user(user_id)
            return render(request, 'user.html', {'user': login_user})
        else:
            return render(request, 'user.html', {'error': '请传入用户id', 'back': 1})


def user_collection_more(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user_collections = User.objects.get(user_id=user_id).collection_set.order_by('-collection_create_time')
            # Get all post IDs associated with the user's collections
            post_ids = user_collections.values_list('post_id', flat=True)
            # Retrieve all posts associated with the user's collections
            associated_collection_posts = Post.objects.filter(post_id__in=post_ids).order_by('-post_create_time')[6:]
            return data_handle.db_to_json2(request, associated_collection_posts)
    return render(request, '500.html', {'error': '用户访问异常'})


def user_info_update(request):
    if request.method == 'GET':
        if verify.verify_current_user(request):
            current_user = get_specific_user(request.GET.get('user_id'))
            return render(request, 'user-update.html', {'user': current_user})
        else:
            return render(request, '500.html', {'error': '用户访问异常'})
    if request.method == 'POST':
        update_data = {}
        keys = ['user_name', 'user_nickname', 'user_email', 'user_sex',
                'user_description', 'user_headicon', 'user_wechat', 'user_qq', 'user_phone']
        current_user = get_specific_user(request.GET.get('user_id'))
        for key in keys:
            if key in request.POST:
                update_data[key] = request.POST.get(key)
        # print(update_data)
        if verify.verify_current_user(request):
            try:
                if User.objects.filter(user_id=request.session['login_user_id']).update(**update_data):
                    return render(request, 'user-update.html',
                                  {'success': '更新成功', 'user': current_user})
            except Exception as e:
                return render(request, 'user-update.html',
                              {'error': '更新失败, 错误状态码：'
                                        + str(e.args[0]) + ',错误信息：' + e.args[1],
                               'user': current_user})
