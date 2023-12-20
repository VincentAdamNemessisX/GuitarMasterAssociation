from .models import Post


def remove_post_by_id(post_id):
    """
    :param post_id: 要删除的id
    :return: 是否删除成功
    """
    if Post.objects.get(collection_id=post_id):
        if Post.objects.filter(collection_id=post_id).delete():
            return True
    else:
        return False
