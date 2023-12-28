import json
import random

import bs4
from django.db.models import Count, Subquery, OuterRef, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect

from collection.models import Collection
from custom.data_handle import handle_uploaded_image
from custom.goto_controller import redirect_referer
from custom.update_some_index import update_post_view_count, update_user_recent_post
from post.models import Post, PostLike
from user.get import get_sorted_authors_by_hot
from user.models import User
from zone.get import get_archived_posts
from zone.models import Zone
from .function import remove_post_by_id, get_posts_by_any_with_vague, get_recommend_posts


# Create your views here.
def index(request):
    hot_authors = get_sorted_authors_by_hot(1)[:4]
    recent_posts = Post.objects.filter(post_status=1).order_by('-post_create_time')[:6]
    return render(request, 'index.html')


def post_normal(request):
    if request.method == 'GET':
        if not request.GET.get('post_id'):
            return render(request, '404.html')
        try:
            current_post = Post.objects.get(post_id=request.GET.get('post_id'), post_status=1)
        except Post.DoesNotExist:
            return render(request, '404.html', {'error': '帖子不存在或审核中，请核实后重新浏览！'})
        current_zone_posts = current_post.zone_id.post_set.values().order_by("post_create_time").reverse()
        current_post_index = 0
        for post in current_zone_posts:
            if post['post_id'] == current_post.post_id:
                # print(current_post_index)
                break
            current_post_index += 1
        try:
            next_post = current_zone_posts[current_post_index + 1]
            if next_post:
                next_post = Post.objects.get(post_id=next_post['post_id'])
            else:
                next_post = None
        except IndexError:
            next_post = None
        try:
            prev_post = current_zone_posts[current_post_index - 1]
            if prev_post:
                prev_post = Post.objects.get(post_id=prev_post['post_id'])
            else:
                prev_post = None
        except AssertionError:
            prev_post = None
        if request.session.get('login_user_id'):
            current_post.is_liked = PostLike.objects.filter(user_id=request.session.get('login_user_id'),
                                                            post_id=current_post.post_id).exists()
            current_post.is_collected = Collection.objects.filter(user_id=request.session.get('login_user_id'),
                                                                  post_id=current_post.post_id).exists()
        else:
            current_post.is_liked = False
            current_post.is_collected = False
        hot_authors = get_sorted_authors_by_hot(1)[:4]
        recent_posts = Post.objects.filter(post_status=1).order_by('-post_create_time')[:6]
        archived_posts = get_archived_posts(zone_id=current_post.zone_id)
        # Subquery 用于获取每个专区的 post 数量
        subquery = Post.objects.filter(zone_id=OuterRef('zone_id')).values('zone_id').annotate(
            post_count=Count('zone_id')).values('post_count')[:1]
        # hot_zones 包含了每个热门专区以及其对应的 post 数量
        hot_zones = Zone.objects.filter(zone_status=1).annotate(
            post_count=Subquery(subquery)).order_by('-post_count')[:5]
        update_post_view_count(request)
        return render(request, 'post_details_normal.html',
                      {
                          'post': current_post,
                          'next_post': next_post, 'prev_post': prev_post,
                          'hot_zones': hot_zones, 'recent_posts': recent_posts,
                          'hot_authors': hot_authors, 'archived_posts': archived_posts
                      })
    return render(request, '500.html', {'error': '请求错误！'})


@update_user_recent_post
@update_post_view_count
def update_post_view_count(request):
    pass


def post_immersion(request):
    if request.method == 'GET':
        if not request.GET.get('post_id'):
            return render(request, '404.html')
        try:
            current_post = Post.objects.get(post_id=request.GET.get('post_id'), post_status=1)
        except Post.DoesNotExist:
            return render(request, '404.html', {'error': '帖子不存在或审核中，请核实后重新浏览！'})
        current_zone_posts = current_post.zone_id.post_set.values().order_by("post_create_time").reverse()
        current_post_index = 0
        for post in current_zone_posts:
            if post['post_id'] == current_post.post_id:
                # print(current_post_index)
                break
            current_post_index += 1
        try:
            next_post = current_zone_posts[current_post_index + 1]
            if next_post:
                next_post = Post.objects.get(post_id=next_post['post_id'])
            else:
                next_post = None
        except IndexError:
            next_post = None
        try:
            prev_post = current_zone_posts[current_post_index - 1]
            if prev_post:
                prev_post = Post.objects.get(post_id=prev_post['post_id'])
            else:
                prev_post = None
        except AssertionError:
            prev_post = None
        if request.session.get('login_user_id'):
            current_post.is_liked = PostLike.objects.filter(user_id=request.session.get('login_user_id'),
                                                            post_id=current_post.post_id).exists()
            current_post.is_collected = Collection.objects.filter(user_id=request.session.get('login_user_id'),
                                                                  post_id=current_post.post_id).exists()
        else:
            current_post.is_liked = False
            current_post.is_collected = False
        update_post_view_count(request)
        return render(request, 'post_details_immersion.html',
                      {
                          'post': current_post,
                          'next_post': next_post, 'prev_post': prev_post,
                      })
    return render(request, '500.html', {'error': '请求错误！'})


def random_post(request):
    post_ids = Post.objects.all().values_list('post_id', flat=True)
    random.shuffle(list(post_ids))
    rd = random.randint(0, len(post_ids) - 1)
    specific_post = Post.objects.get(post_id=post_ids[rd])
    return redirect('/post-' + specific_post.post_layout_mode + '?post_id=' + str(specific_post.post_id))


def delete_specific_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        if post_id is None:
            return HttpResponse({'删除失败!', '400'})
        if remove_post_by_id(post_id):
            return HttpResponse({'200'})
        else:
            return HttpResponse({'删除失败!', '404'})
    return render(request, '500.html', {'error': '请求错误!'})


@redirect_referer
def redirect_refer():
    pass


def update_post_like(request):
    if request.method == 'POST':
        if request.POST.get('post_id') is None:
            return HttpResponse(json.dumps({'获取帖子失败!'}))
        else:
            if request.POST.get("method") == "append":
                if add_post_like_count(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'用户未登录或帖子不存在，点赞失败!'})
            elif request.POST.get("method") == "remove":
                if remove_post_like_count(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'用户未登录或帖子不存在，取消点赞失败!', '404'})
            else:
                return HttpResponse({'未知方法点赞失败!'})
    return render(request, "500.html", {'error': '请求错误!'})


def update_post_collection(request):
    if request.method == 'POST':
        if request.POST.get('post_id') is None:
            return HttpResponse({'获取帖子失败!'})
        else:
            if request.POST.get("method") == "append":
                if add_post_collection(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'用户未登录或帖子不存在，添加个人收藏失败!'})
            elif request.POST.get("method") == "remove":
                if remove_post_collection(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'用户未登录或帖子不存在，取消收藏失败!'})
            else:
                return HttpResponse({'未知方法收藏失败!', '400'})
    return render(request, "500.html", {'error': '请求错误!'})


def add_post_like_count(request):
    post = Post.objects.get(post_id=request.POST.get('post_id'))
    user = User.objects.get(user_id=request.session.get('login_user_id')) if request.session.get(
        'login_user_id') else None
    if post and user:
        if (post.post_id,) not in user.postlike_set.values_list("post_id"):
            post.post_like += 1
            post.save()
            post_like = PostLike.objects.create(user_id=user, post_id=post)
            post_like.save()
            return True
        else:
            return False
    else:
        return False


def add_post_collection(request):
    post = Post.objects.get(post_id=request.POST.get('post_id'))
    user = User.objects.get(user_id=request.session.get('login_user_id')) if request.session.get(
        'login_user_id') else None
    if post and user:
        if not Collection.objects.filter(user_id=user, post_id=post).exists():
            collection = Collection.objects.create(user_id=user, post_id=post)
            collection.save()
            return True
        else:
            return False
    else:
        return False


def remove_post_collection(request):
    post = Post.objects.get(post_id=request.POST.get('post_id'))
    user = User.objects.get(user_id=request.session.get('login_user_id')) if request.session.get(
        'login_user_id') else None
    if post and user:
        if Collection.objects.filter(user_id=user, post_id=post).exists():
            Collection.objects.filter(user_id=user, post_id=post).delete()
            return True
        else:
            return False
    else:
        return False


def remove_post_like_count(request):
    post = Post.objects.get(post_id=request.POST.get('post_id'))
    user = User.objects.get(user_id=request.session.get('login_user_id')) if request.session.get(
        'login_user_id') else None
    if post and user:
        if (post.post_id,) in user.postlike_set.values_list("post_id"):
            post.post_like -= 1
            post.save()
            post_like = PostLike.objects.get(user_id=user, post_id=post)
            post_like.delete()
            return True
        else:
            return False
    else:
        return False


def post_publish(request):
    if request.method == 'POST':
        return post_logic(request)
    return render(request, "post_publish.html")


def post_upload_image(request):
    if request.method == 'POST':
        if request.FILES.get('post-upload-image') is not None:
            # print(request.META.get("HTTP_HOST"))
            path = handle_uploaded_image(request.FILES.get('post-upload-image'))
            if path:
                return HttpResponse(json.dumps({"errno": 0,
                                                "data": {
                                                    "url": "/" + path,
                                                    "alt": path.split("/")[-1].split(".")[0],
                                                    "href": 'http://' + request.META.get("HTTP_HOST") + "/" + path}
                                                }),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({"errno": 400, "message": "后台获取图片信息失败！"}),
                                content_type='application/json')
    return HttpResponse(json.dumps({"errno": 401, "message": "api请求方式错误！"}),
                        content_type='application/json')


def update_post(request):
    if request.method == 'GET':
        if request.GET.get('post_id') is None:
            return render(request, "post-edit.html", {'error': '参数异常'})
        post = Post.objects.get(post_id=request.GET.get('post_id'))
        if post is None:
            return render(request, "post-edit.html", {'error': '该帖子不存在'})
        return render(request, "post-edit.html", {'post': post})
    if request.method == 'POST':
        return post_logic(request, method='update')


def post_logic(request, method='post'):
    if request.POST.get('post_title') is None or request.POST.get('post_content') is None:
        return HttpResponse(json.dumps({'status': 402, 'message': '标题和内容异常!'}),
                            content_type='application/json')
    if request.POST.get('zone_id') is None or request.POST.get('post_layout_mode') is None:
        return HttpResponse(json.dumps({'status': 402, 'message': '所属专区和页面布局方式异常!'}),
                            content_type='application/json')
    post_image_path = \
        bs4.BeautifulSoup(request.POST.get('post_content'), 'html.parser').find('img')
    author = User.objects.get(user_id=request.session.get('login_user_id'))
    zone = Zone.objects.get(zone_id=request.POST.get('zone_id'))
    if author is None:
        return HttpResponse(json.dumps({'status': 402, 'message': '未登录用户非法操作!'}),
                            content_type='application/json')
    if zone is None:
        return HttpResponse(json.dumps({'status': 402, 'message': '所属专区不存在,请刷新后重试!'}),
                            content_type='application/json')
    if post_image_path:
        post_image_path = post_image_path.get("src").split("/", 2)[-1]
        if method == 'post':
            post = Post.objects.create(
                user_id=author,
                zone_id=zone,
                post_title=request.POST.get('post_title'),
                post_content=request.POST.get('post_content'),
                post_layout_mode=request.POST.get('post_layout_mode'),
                post_status=2,
                post_image=post_image_path,
            )
            post.save()
        elif method == 'update':
            post = Post.objects.get(post_id=request.POST.get('post_id'))
            post.post_title = request.POST.get('post_title')
            post.user_id = author
            post.zone_id = zone
            post.post_content = request.POST.get('post_content')
            post.post_layout_mode = request.POST.get('post_layout_mode')
            post.post_image = post_image_path
            post.save()
        else:
            post = None
    else:
        if method == 'post':
            post = Post.objects.create(
                user_id=author,
                zone_id=zone,
                post_title=request.POST.get('post_title'),
                post_content=request.POST.get('post_content'),
                post_layout_mode=request.POST.get('post_layout_mode'),
                post_status=2,
            )
        elif method == 'update':
            post = Post.objects.get(post_id=request.POST.get('post_id'))
            post.user_id = author
            post.zone_id = zone
            post.post_title = request.POST.get('post_title')
            post.post_content = request.POST.get('post_content')
            post.post_layout_mode = request.POST.get('post_layout_mode')
            post.save()
        else:
            post = None
    if post:
        pst = Post.objects.get(post_id=post.post_id)
        data = {'post_id': pst.post_id, 'post_layout_mode': pst.post_layout_mode}
        return HttpResponse(json.dumps({'status': 200, 'data': data}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status': 402, 'message': '操作失败!'}), content_type='application/json')


def search_posts(request):
    if request.method == 'GET':
        recommend_posts = get_recommend_posts()
        site_data = {
            'site_views': Post.objects.filter(post_status=1).aggregate(site_views=Sum('post_view')).get('site_views'),
            'site_users': User.objects.all().count(),
        }

        if request.GET.get('keyword') is None:
            return render(request, "post-search.html",
                          {
                              'k': request.GET.get('keyword'),
                              'error': '参数异常',
                              'recommend': recommend_posts,
                              'site_data': site_data
                          })
        result, result_count = get_posts_by_any_with_vague(request.GET.get('keyword'))
        if result:
            return render(request, "post-search.html",
                          {
                              'k': request.GET.get('keyword'),
                              'result': result,
                              'result_count': result_count,
                              'recommend': recommend_posts,
                              'site_data': site_data
                          })
        else:
            return render(request, "post-search.html",
                          {
                              'k': request.GET.get('keyword'),
                              'err': '没有找到相关帖子',
                              'recommend': recommend_posts,
                              'site_data': site_data
                          })
    return render(request, "post-search.html")
