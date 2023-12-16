from django.utils import timezone

from post.models import Post
from .models import Zone


def get_all_zones():
    return Zone.objects.all()


def get_all_zones_by_status(status):
    return Zone.objects.filter(zone_status=status)


def get_archived_posts(zone_id):
    timezone.activate(timezone.pytz.timezone('PRC'))
    archived_posts = Post.objects.filter(post_status=1, zone_id=zone_id)
    for index in range(len(archived_posts)):
        archived_posts[index].year = archived_posts[index].post_create_time.year
        archived_posts[index].month = archived_posts[index].post_create_time.month
    for i in archived_posts:
        print(i.year, i.month)
    return archived_posts
