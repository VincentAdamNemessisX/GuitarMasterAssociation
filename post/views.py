import random

from django.db.models import Count, Subquery, OuterRef
from django.http import HttpResponse
from django.shortcuts import render, redirect

from collection.models import Collection
from custom.goto_controller import redirect_referer
from custom.update_some_index import update_post_view_count, update_user_recent_post
from post.models import Post, PostLike
from user.get import get_sorted_authors_by_hot
from user.models import User
from zone.get import get_archived_posts
from zone.models import Zone
from .function import remove_post_by_id


# Create your views here.
def index(request):
    hot_authors = get_sorted_authors_by_hot(1)[:4]
    recent_posts = Post.objects.filter(post_status=1).order_by('-post_create_time')[:6]
    return render(request, 'index.html')


def post_normal(request):
    if request.method == 'GET':
        if not request.GET.get('post_id'):
            return render(request, '404.html')
        current_post = Post.objects.get(post_id=request.GET.get('post_id'), post_status=1)
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
        update_post_view_count(request)
    return render(request, 'post_details_immersion.html')


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


def update_post(request):
    if request.method == 'GET':
        pass
        return render(request, "post-edit.html", {'post_id': request.GET.get('post_id')})


def update_post_like(request):
    if request.method == 'POST':
        if request.POST.get('post_id') is None:
            return HttpResponse({'更新失败!', '400'})
        else:
            if request.POST.get("method") == "append":
                if add_post_like_count(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'更新失败!', '404'})
            elif request.POST.get("method") == "remove":
                if remove_post_like_count(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'更新失败!', '404'})
            else:
                return HttpResponse({'更新失败!', '400'})
    return render(request, "500.html", {'error': '请求错误!'})


def update_post_collection(request):
    if request.method == 'POST':
        if request.POST.get('post_id') is None:
            return HttpResponse({'更新失败!', '400'})
        else:
            if request.POST.get("method") == "append":
                if add_post_collection(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'更新失败!', '404'})
            elif request.POST.get("method") == "remove":
                if remove_post_collection(request):
                    return HttpResponse({'200'})
                else:
                    return HttpResponse({'更新失败!', '404'})
            else:
                return HttpResponse({'更新失败!', '400'})
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
        if request.POST.get('post_title') is None or request.POST.get('post_content') is None:
            return HttpResponse({'发布失败!', '400'})
    return render(request, "post_publish.html")
