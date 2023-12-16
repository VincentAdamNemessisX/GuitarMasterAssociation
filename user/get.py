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
        user.hot_volume = ((Post.objects.filter(user_id=user.user_id,
                                           post_status=1).count() + Post.objects.filter(
            user_id=user.user_id, post_status=1).count()) * 900
                      + Post.objects.filter(user_id=user.user_id, post_status=1).aggregate(
                    Sum('post_view')).get('post_view__sum') * 50
                      + Post.objects.filter(user_id=user.user_id, post_status=1).aggregate(
                    Sum('post_like')).get('post_like__sum') * 150
                      + Review.objects.filter(
                    content_id__in=user.post_set.values_list('post_id', flat=True)).count() * 300
                      + Collection.objects.filter(
                    post_id__collection__in=user.post_set.values_list('post_id', flat=True)).count() * 300
                      )
    hot_authors = sorted(users, key=lambda x: x.hot_volume, reverse=reverse)
    return hot_authors
