from django.db.models import Sum

from collection.models import Collection
from post.models import Post
from review.models import Review
from .models import User


def get_sorted_authors_by_hot(reverse=1):
    users = User.objects.all()
    if reverse == 1:
        reverse = True
    else:
        reverse = False
    for user in users:
        if Post.objects.filter(user_id=user.user_id, post_status=1).count() * 900:
            user.hot_volume = Post.objects.filter(user_id=user.user_id, post_status=1).count() * 900
            if Post.objects.filter(user_id=user.user_id, post_status=1)[0].post_view:
                user.hot_volume += (Post.objects.filter(user_id=user.user_id, post_status=1)
                                    .aggregate(Sum('post_view')).get('post_view__sum') * 50)
            if Post.objects.filter(user_id=user.user_id, post_status=1)[0].post_like:
                user.hot_volume += (Post.objects.filter(user_id=user.user_id, post_status=1)
                                    .aggregate(Sum('post_like')).get('post_like__sum') * 150)
        else:
            user.hot_volume = 0
        if Review.objects.filter(post_id__in=user.post_set.values_list('post_id', flat=True)):
            user.hot_volume += Review.objects.filter(
                post_id__in=user.post_set.values_list('post_id', flat=True)).count() * 300
        if Collection.objects.filter(post_id__in=user.post_set.values_list('post_id', flat=True)):
            user.hot_volume += Collection.objects.filter(
                post_id__in=user.post_set.values_list('post_id', flat=True)).count() * 400
    hot_authors = sorted(users, key=lambda x: x.hot_volume, reverse=reverse)
    return hot_authors


def get_specific_user(user_id):
    user = User.objects.get(user_id=user_id)
    user.user_view = user.post_set.aggregate(Sum('post_view')).get('post_view__sum')
    user.user_like = user.post_set.aggregate(Sum('post_like')).get('post_like__sum')
    user.user_collection = user.collection_set.filter(user_id=user_id).count()
    user.post = user.post_set.order_by('-post_create_time')
    user.post_count = user.post_set.count()
    user.collection = user.collection_set.order_by('-collection_create_time')
    user.collection_count = user.collection_set.count()
    if user.collection_count > 6:
        user.collection = user.collection[:6]
    user.recent = user.recentbrowsing_set.order_by('-recent_browsing_time')[:10]
    user.recent_count = user.recentbrowsing_set.count()
    user.post = user.post_set.order_by('-post_create_time')
    user.post_count = user.post_set.count()
    return user
