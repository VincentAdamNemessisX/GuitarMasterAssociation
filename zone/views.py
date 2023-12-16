# Create your views here.
from django.db.models import Sum, Count, Subquery, OuterRef
from django.shortcuts import render
from collection.models import Collection
from post.models import Post
from review.models import Review
from user.get import get_sorted_authors_by_hot
from zone.get import get_archived_posts
from zone.models import Zone


def zone(request):
    if request.method == 'GET':
        zone_info = Zone.objects.filter(zone_id=request.GET.get('zone_id'), zone_status=1).first()
        hot_authors = get_sorted_authors_by_hot(0)[:4]
        recent_posts = Post.objects.filter(post_status=1).order_by('-post_create_time')[:6]
        archived_posts = get_archived_posts(zone_id=zone_info.zone_id)
        # Subquery 用于获取每个专区的 post 数量
        subquery = Post.objects.filter(zone_id=OuterRef('zone_id')).values('zone_id').annotate(
            post_count=Count('zone_id')).values('post_count')[:1]
        # hot_zones 包含了每个热门专区以及其对应的 post 数量
        hot_zones = Zone.objects.filter(zone_status=1).annotate(post_count=Subquery(subquery)).order_by('-post_count')[
                    :5]
        if zone_info is None:
            return render(request, '500.html', {'error': '请求错误或专区已下线'})
        current_page = int(request.GET.get('page')) if request.GET.get('page') else 1
        zone_info.posts_count = Post.objects.filter(zone_id=zone_info.zone_id, post_status=1).count()
        page_size = 9
        if zone_info.zone_layout_mode == 3:
            page_size = 10
        elif zone_info.zone_layout_mode == 4:
            page_size = 10
        elif zone_info.zone_layout_mode == 5:
            page_size = 6
        zone_info.page_count = zone_info.posts_count // page_size
        zone_info.page_list = []
        for i in range(0, zone_info.page_count + 1):
            zone_info.page_list.append(i + 1)
        if len(zone_info.page_list) > 5:
            zone_info.page_list = zone_info.page_list[:5]
            if current_page > zone_info.page_count | current_page < 1:
                current_page = 1
        zone_all_posts = Post.objects.filter(zone_id=zone_info.zone_id, post_status=1).order_by(
            '-post_create_time').all()
        zone_posts = zone_all_posts[(current_page - 1) * page_size:current_page * page_size]
        zone_info.heating = ((int(zone_info.zone_last_active_time.timestamp()) / 1000000)
                             + (Post.objects.filter(zone_id=zone_info.zone_id,
                                                    post_status=1).count() + Post.objects.filter(
                    zone_id=zone_info.zone_id, post_status=1).count()) * 900
                             + Post.objects.filter(zone_id=zone_info.zone_id, post_status=1).aggregate(
                    Sum('post_view')).get('post_view__sum') * 50
                             + Post.objects.filter(zone_id=zone_info.zone_id, post_status=1).aggregate(
                    Sum('post_like')).get('post_like__sum') * 150
                             + Review.objects.filter(
                    content_id__in=zone_all_posts.values_list('post_id', flat=True)).count() * 200
                             + Collection.objects.filter(
                    post_id__collection__in=zone_all_posts.values_list('post_id', flat=True)).count() * 300
                             )
        zone_info.heating = int(zone_info.heating)
        return render(request, 'zone-' + str(zone_info.zone_layout_mode) + '.html',
                      {'zone': zone_info, 'posts': zone_posts,
                       'hot_zones': hot_zones, 'recent_posts': recent_posts,
                       'hot_authors': hot_authors, 'archived_posts': archived_posts})
    return render(request, '500.html', {'error': '请求错误或专区已下线'})
