from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from django.shortcuts import render, HttpResponseRedirect

from custom import verify, data_handle
from custom.goto_controller import redirect_referer
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
                    return render(request, 'signin.html', {'error': '该用户已被禁用'})
                if user.user_status == 2:
                    return render(request, 'signin.html', {'error': '该用户已被冻结'})
                if user.user_status == 1:
                    request.session['login_username'] = user.user_name
                    request.session['login_user_id'] = user.user_id
                    request.session['login_user_headicon'] = user.user_headicon.url
                    request.session.set_expiry(60 * 60)
                    User.objects.filter(user_id=user.user_id).update(user_last_active_time=verify.get_current_time())
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
        userid = request.GET.get('userid')
        if userid:
            login_user = User.objects.get(user_id=userid)
            login_user.user_view = login_user.post_set.aggregate(Sum('post_view')).get('post_view__sum')
            login_user.user_like = login_user.post_set.aggregate(Sum('post_like')).get('post_like__sum')
            login_user.user_collection = login_user.collection_set.filter(user_id=userid).count()
            login_user.post = login_user.post_set.order_by('-post_create_time')
            login_user.post_count = login_user.post_set.count()
            login_user.collection = login_user.collection_set.order_by('-collection_create_time')
            login_user.collection_count = login_user.collection_set.count()
            if login_user.collection_count > 6:
                login_user.collection = login_user.collection[:6]
            login_user.recent = login_user.recentbrowsing_set.order_by('-recent_create_time')[:10]
            login_user.recent_count = login_user.recentbrowsing_set.count()
            login_user.post = login_user.post_set.order_by('-post_create_time')
            login_user.post_count = login_user.post_set.count()
            return render(request, 'user.html', {'user': login_user})
        else:
            return render(request, 'user.html', {'error': '请传入用户id'})


def user_collection_more(request):
    if request.method == 'POST':
        userid = request.POST.get('user_id')
        if userid:
            user_collections = User.objects.get(user_id=userid).collection_set.order_by('-collection_create_time')
            # Get all post IDs associated with the user's collections
            post_ids = user_collections.values_list('post_id', flat=True)
            # Retrieve all posts associated with the user's collections
            associated_collection_posts = Post.objects.filter(post_id__in=post_ids).order_by('-post_create_time')[6:]
            return data_handle.db_to_json2(request, associated_collection_posts)
    return render(request, '500.html', {'error': '用户访问异常'})


def user_info_update(request):
    if request.method == 'GET':
        if verify.verify_current_user(request):
            current_user = User.objects.get(user_id=request.session['login_user_id'])
            return render(request, 'user-update.html', {'user': current_user})
        else:
            return render(request, '500.html', {'error': '用户访问异常'})
    if request.method == 'POST':
        update_data = request.POST
        if verify.verify_current_user(request):
            if User.objects.filter(user_id=request.session['login_user_id']).update(**update_data):
                return render(request, 'user-update.html', {'success': '更新成功'})
            else:
                return render(request, 'user-update.html', {'error': '更新失败'})
        return render(request, 'user-update.html')
