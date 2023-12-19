from post.models import Post
from .models import Zone


def get_all_zones():
    return Zone.objects.all()


def get_all_zones_by_status(status):
    return Zone.objects.filter(zone_status=status)


def get_archived_posts(zone_id):
    archived_posts_year = {}
    archived_posts_years = set(Post.objects.filter(post_status=1, zone_id=zone_id).values_list('post_create_time__year', flat=True))
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
