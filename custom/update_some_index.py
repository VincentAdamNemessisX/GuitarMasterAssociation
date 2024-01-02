from datetime import datetime

from post.models import Post, PostLike
from user.models import User, RecentBrowsing
from zone.models import Zone


def update_zone_active_time(func):
    def _(request, *args, **keys):
        func(request, *args, **keys)
        zone_info = Zone.objects.get(zone_id=request.GET.get('zone_id'))
        zone_info.zone_last_active_time = datetime.now()
        zone_info.save()
        return None

    return _


def update_post_view_count(func):
    def _(request, *args, **keys):
        func(request, *args, **keys)
        post = Post.objects.get(post_id=request.GET.get('post_id'))
        post.post_view += 1
        post.save()
        return None

    return _


def update_user_recent_post(func):
    def _(request, *args, **keys):
        func(request, *args, **keys)
        post = Post.objects.get(post_id=request.GET.get('post_id'))
        user = User.objects.get(user_id=request.session.get('login_user_id')) if request.session.get(
            'login_user_id') else None
        if post and user:
            if (post.post_id,) in user.recentbrowsing_set.values_list("recent_post_id"):
                RecentBrowsing.objects.get(recent_user_id=user.user_id,
                                           recent_post_id=post.post_id).recent_browsing_time = datetime.now()
            else:
                RecentBrowsing.objects.create(recent_user_id=user, recent_post_id=post,
                                              recent_browsing_time=datetime.now())
        return None

    return _
