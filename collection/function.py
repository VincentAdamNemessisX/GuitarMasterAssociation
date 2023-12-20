from collection.models import Collection


def remove_collection_by_id(collection_id):
    """
    :param collection_id: 要删除的id
    :return: 是否删除成功 
    """
    if Collection.objects.get(collection_id=collection_id):
        if Collection.objects.filter(collection_id=collection_id).delete():
            return True
    else:
        return False
