import random

from django.db.models import Count, Subquery, OuterRef
from django.shortcuts import render, redirect

from post.models import Post
from user.get import get_sorted_authors_by_hot
from zone.get import get_archived_posts
from zone.models import Zone


# Create your views here.
def index(request):
    return render(request, 'index.html')


def post_normal(request):
    if request.method == 'GET':
        if not request.GET.get('post_id'):
            return render(request, '404.html')
        current_post = Post.objects.get(post_id=request.GET.get('post_id'), post_status=1)
        hot_authors = get_sorted_authors_by_hot(0)[:4]
        recent_posts = Post.objects.filter(post_status=1).order_by('-post_create_time')[:6]
        archived_posts = get_archived_posts(zone_id=current_post.zone_id)
        # Subquery 用于获取每个专区的 post 数量
        subquery = Post.objects.filter(zone_id=OuterRef('zone_id')).values('zone_id').annotate(
            post_count=Count('zone_id')).values('post_count')[:1]
        # hot_zones 包含了每个热门专区以及其对应的 post 数量
        hot_zones = Zone.objects.filter(zone_status=1).annotate(
            post_count=Subquery(subquery)).order_by('-post_count')[:5]
        return render(request, 'post_details_normal.html',
                      {
                          'post': current_post,
                          'hot_zones': hot_zones, 'recent_posts': recent_posts,
                          'hot_authors': hot_authors, 'archived_posts': archived_posts
                      })


def post_immersion(request):
    if request.method == 'GET':
        if not request.GET.get('post_id'):
            return render(request, '404.html')
    return render(request, 'post_details_immersion.html')


def random_post(request):
    post_ids = Post.objects.all().values_list('post_id', flat=True)
    random.shuffle(list(post_ids))
    rd = random.randint(0, len(post_ids) - 1)
    specific_post = Post.objects.get(post_id=post_ids[rd])
    return redirect('/post-' + specific_post.post_layout_mode + '?post_id=' + str(specific_post.post_id))
