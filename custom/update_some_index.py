from datetime import datetime

from django.shortcuts import redirect

from post.models import Post
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


def update_post_like_count(func):
    def _(request, *args, **keys):
        func(request, *args, **keys)
        post = Post.objects.get(post_id=request.GET.get('post_id'))
        post.post_like += 1
        post.save()
        return None
    return _
