from django.db.models import Sum

from collection.models import Collection
from post.models import Post
from review.models import Review
from .models import Zone


def get_all_zones():
    return Zone.objects.all()


def get_all_zones_by_status(status):
    return Zone.objects.filter(zone_status=status)


def get_archived_posts(zone_id):
    archived_posts_year = {}
    archived_posts_years = set(
        Post.objects.filter(post_status=1, zone_id=zone_id).values_list('post_create_time__year', flat=True))
    for year in archived_posts_years:
        archived_posts_year[year] = Post.objects.filter(post_status=1, zone_id=zone_id,
                                                        post_create_time__year=year).count()
        archived_posts_month = {}
        for month in range(12, 0, -1):
            archived_posts_month[month] = Post.objects.filter(post_status=1, zone_id=zone_id,
                                                              post_create_time__year=year,
                                                              post_create_time__month=month).count()
            if archived_posts_month[month] == 0:
                archived_posts_month.pop(month)
        archived_posts_year[year] = archived_posts_month
        if len(archived_posts_year[year].items()) == 0:
            archived_posts_year.pop(year)
    return archived_posts_year


def get_zones_by_heating(reverse=1):
    zones = Zone.objects.filter(zone_status=1)
    for zone in zones:
        zone.zone_heating = ((int(zone.zone_last_active_time.timestamp()) / 1000000)
                             + (Post.objects.filter(zone_id=zone.zone_id, post_status=1).count()
                                + Post.objects.filter(zone_id=zone.zone_id, post_status=1).count()) * 900
                             + Post.objects.filter(zone_id=zone.zone_id, post_status=1).aggregate(
                    Sum('post_view')).get('post_view__sum') * 50
                             + Post.objects.filter(zone_id=zone.zone_id, post_status=1).aggregate(
                    Sum('post_like')).get('post_like__sum') * 150
                             + Review.objects.filter(
                    post_id__in=zone.post_set.values_list('post_id', flat=True)).count() * 200
                             + Collection.objects.filter(
                    post_id__collection__in=zone.post_set.values_list('post_id', flat=True)).count() * 300
                             )
    if reverse == 1:
        zones = sorted(zones, key=lambda x: x.zone_heating, reverse=True)
    else:
        zones = sorted(zones, key=lambda x: x.zone_heating)
    # print(zones)
    return zones
