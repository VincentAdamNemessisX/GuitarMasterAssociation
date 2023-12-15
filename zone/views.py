# Create your views here.
from django.db.models import Sum
from django.shortcuts import render
from collection.models import Collection
from post.models import Post
from review.models import Review
from zone.models import Zone
from custom.update_some_index import update_zone_active_time


def zone(request):
    if request.method == 'GET':
        zone_info = Zone.objects.filter(zone_id=request.GET.get('zone_id'), zone_status=1).first()
        if zone_info is None:
            return render(request, '500.html', {'error': '请求错误或专区已下线'})
        zone_posts = Post.objects.filter(zone_id=zone_info.zone_id, post_status=1).order_by('-post_create_time')
        zone_info.heating = ((int(zone_info.zone_last_active_time.timestamp()) / 1000000)
                             + (Post.objects.filter(zone_id=zone_info.zone_id,
                                                    post_status=1).count() + Post.objects.filter(
                    zone_id=zone_info.zone_id, post_status=1).count()) * 900
                             + Post.objects.filter(zone_id=zone_info.zone_id, post_status=1).aggregate(
                    Sum('post_view')).get('post_view__sum') * 50
                             + Post.objects.filter(zone_id=zone_info.zone_id, post_status=1).aggregate(
                    Sum('post_like')).get('post_like__sum') * 150
                             + Review.objects.filter(
                    content_id__in=zone_posts.values_list('post_id', flat=True)).count() * 200
                             + Collection.objects.filter(
                    post_id__collection__in=zone_posts.values_list('post_id', flat=True)).count() * 300
                             )
        zone_info.heating = int(zone_info.heating)
        return render(request, 'zone-' + str(zone_info.zone_layout_mode) + '.html',
                      {'zone': zone_info, 'posts': zone_posts})
    return render(request, '500.html', {'error': '请求错误或专区已下线'})
