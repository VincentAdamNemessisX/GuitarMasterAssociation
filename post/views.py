import random

from django.db.models import Count, Subquery, OuterRef
from django.http import HttpResponse
from django.shortcuts import render, redirect

from custom.goto_controller import redirect_referer
from custom.update_some_index import update_post_view_count, update_user_recent_post
from post.models import Post
from user.get import get_sorted_authors_by_hot
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
                          'hot_zones': hot_zones, 'recent_posts': recent_posts,
                          'hot_authors': hot_authors, 'archived_posts': archived_posts
                      })


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
