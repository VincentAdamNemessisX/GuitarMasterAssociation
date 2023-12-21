from copy import copy

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
        post_data = request.POST
        if User.objects.filter(user_name=username).exists():
            login_user = User.objects.get(user_name=username)
            if check_password(password, login_user.user_password):
                if login_user.user_status == 0:
                    return render(request, 'signin.html', {'error': '该用户已被禁用', 'info': post_data})
                if login_user.user_status == 2:
                    return render(request, 'signin.html', {'error': '该用户已被冻结', 'info': post_data})
                if login_user.user_status == 1:
                    request.session['login_username'] = login_user.user_name
                    request.session['login_user_id'] = login_user.user_id
                    request.session['login_user_headicon'] = login_user.user_headicon.url
                    request.session.set_expiry(60 * 60)
                    User.objects.filter(user_id=login_user.user_id).update(
                        user_last_active_time=verify.get_current_time())
                    return HttpResponseRedirect('/index/')
                else:
                    return render(request, 'signin.html', {'error': '未知错误', 'info': post_data})
            else:
                return render(request, 'signin.html', {'error': '用户名或密码错误', 'info': post_data})
        else:
            return render(request, 'signin.html', {'error': '用户名或密码错误', 'info': post_data})
    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = make_password(request.POST.get('password'))
        sex = request.POST.get('sex')
        headicon = request.POST.get('headicon')
        post_data = request.POST
        if User.objects.filter(user_name=username).exists():
            return render(request, 'signup.html', {'error': '用户名已存在', 'info': post_data})
        else:
            if User.objects.create(user_name=username, user_email=email, user_phone=phone, user_password=password,
                                   user_sex=sex, user_headicon=headicon):
                return render(request, 'signin.html', {'success': '注册成功'})
            return render(request, 'signup.html', {'error': '注册失败', 'info': post_data})
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
        post_data = copy(request.POST)
        post_data['user_sex'] = int(post_data['user_sex'])
        keys = ['user_name', 'user_nickname', 'user_email', 'user_sex',
                'user_description', 'user_wechat', 'user_qq', 'user_phone']
        current_user = get_specific_user(request.GET.get('user_id'))
        temp = current_user.__dict__
        for key in keys:
            if key in post_data.keys():
                if temp[key] == post_data[key]:
                    continue
                update_data[key] = post_data[key]
        if request.FILES.get('user_headicon'):
            if request.FILES.get('user_headicon') != temp['user_headicon'].split('/')[-1]:
                update_data['user_headicon'] = request.FILES.get('user_headicon')
                update_data['user_headicon'] = data_handle.handle_uploaded_file(update_data['user_headicon'],
                                                                                current_user.user_name).split('/')[-2:]
                update_data['user_headicon'] = '/'.join(update_data['user_headicon'])
        # print(update_data)
        if verify.verify_current_user(request):
            try:
                if len(update_data) > 0:
                    if User.objects.filter(user_id=request.session['login_user_id']).update(**update_data):
                        return render(request, 'user-update.html',
                                      {'success': '更新成功', 'user': current_user})
                return render(request, 'user-update.html', {'error': '请修改要更新的项', 'user': current_user})
            except Exception as e:
                return render(request, 'user-update.html',
                              {'error': '更新失败, 错误信息：'
                                        + str(e.args.__str__()),
                               'user': current_user})
