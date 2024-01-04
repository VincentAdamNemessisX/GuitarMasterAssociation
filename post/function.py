from itertools import chain

from collection.models import Collection
from review.models import Review
from .models import Post


def remove_post_by_id(post_id):
    """
    :param post_id: 要删除的id
    :return: 是否删除成功
    """
    if Post.objects.get(post_id=post_id):
        if Post.objects.filter(post_id=post_id).delete():
            return True
    else:
        return False


def get_posts_by_content(content):
    return Post.objects.filter(post_content__icontains=content, post_status=1)


def get_posts_by_user(user_name):
    return Post.objects.filter(user_id__user_name=user_name, post_status=1)


def get_posts_by_zone(zone_name):
    return Post.objects.filter(zone_id__zone_name=zone_name, post_status=1)


def get_posts_by_any_with_vague(content, user_name='', zone_name=''):
    """
    :param content: post_content
    :param user_name: post_author
    :param zone_name: post_zone
    :return: posts or False
    """
    posts = set()
    if Post.objects.filter(post_content__icontains=content, post_status=1).count() > 0:
        posts = chain(posts, Post.objects.filter(post_content__icontains=content, post_status=1))
    # posts = posts | Post.objects.filter(post_title__icontains=user_name, post_status=1)
    if Post.objects.filter(post_title__icontains=content, post_status=1).count() > 0:
        posts = chain(posts, Post.objects.filter(post_title__icontains=content, post_status=1))
    # posts = posts | Post.objects.filter(user_id__user_name=content, post_status=1)
    if Post.objects.filter(user_id__user_name__icontains=content, post_status=1).count() > 0:
        posts = chain(posts, Post.objects.filter(user_id__user_name__contains=content, post_status=1))
        posts = chain(posts, Post.objects.filter(user_id__user_nickname__icontains=content, post_status=1))
    # posts = posts | Post.objects.filter(zone_id__zone_name=content, post_status=1)
    if Post.objects.filter(zone_id__zone_name__icontains=content, post_status=1).count() > 0:
        posts = chain(posts, Post.objects.filter(zone_id__zone_name__icontains=content, post_status=1))
    posts_count = (Post.objects.filter(post_content__icontains=content, post_status=1).count()
                   + Post.objects.filter(post_title__icontains=content, post_status=1).count() +
                   Post.objects.filter(user_id__user_name__icontains=content, post_status=1).count() +
                   Post.objects.filter(zone_id__zone_name__icontains=content, post_status=1).count())
    if type(posts).__name__ == "chain":
        posts = set(posts)
        return posts, len(posts)
    else:
        return False, posts_count


def get_recommend_posts():
    return Post.objects.filter(post_status=1).order_by('post_like').order_by('post_view')


def get_the_most_popular_post():
    posts = Post.objects.filter(post_status=1)
    current_post_heating = 0
    the_most_popular_post = None
    for post in posts:
        post_heating = ((int(post.post_update_time.timestamp()) / 1000000)
                        + post.post_view * 50 + post.post_like * 150
                        + Review.objects.filter(post_id=post.post_id).count() * 200
                        + Collection.objects.filter(post_id=post.post_id).count() * 300
                        )
        if post_heating > current_post_heating:
            current_post_heating = post_heating
            the_most_popular_post = post
    return the_most_popular_post


def get_posts_order_by_hotness():
    posts = Post.objects.filter(post_status=1)
    for post in posts:
        post_heating = ((int(post.post_update_time.timestamp()) / 1000000)
                        + post.post_view * 50 + post.post_like * 150
                        + Review.objects.filter(post_id=post.post_id).count() * 200
                        + Collection.objects.filter(post_id=post.post_id).count() * 300
                        )
        post.post_heating = post_heating
    return sorted(posts, key=lambda post: post.post_heating, reverse=True)
