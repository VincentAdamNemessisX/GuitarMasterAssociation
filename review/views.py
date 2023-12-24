from django.http import JsonResponse

from review.models import Review


# Create your views here.
def get_init_reviews(request):
    if request.method == 'POST':
        if request.POST.get('post_id'):
            post_id = request.POST.get('post_id')
            if post_id:
                reviews = Review.objects.filter(content_id=post_id, parent_id=None).order_by('-review_time_index')[:10]
                # 将关联的发布者信息也序列化为字典形式
                serialized_reviews = [
                    {
                        'review_id': review.review_id,
                        'content': review.review_content,
                        'author': {
                            'user_id': review.user_id.user_id,
                            'username': review.user_id.user_nickname if review.user_id.user_nickname else review.user_id.user_name,
                            'user_headicon': review.user_id.user_headicon.url,
                        },
                        'review_time': review.review_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'review_parent_id': review.parent_id.review_id if review.parent_id else None,
                        'children_count': Review.objects.filter(parent_id=review.review_id).count(),
                    }
                    for review in reviews
                ]
                return JsonResponse({'code': 200, 'all_reviews_count': Review.objects.filter(content_id=post_id).count(), 'data': serialized_reviews, 'msg': '获取成功'})
                # return data_handle.db_to_json2(request, reviews)
            else:
                return JsonResponse({'code': 400, 'msg': '参数错误'})
    return JsonResponse({'code': 401, 'msg': '请求方式错误'})


def load_more_reviews(request):
    if request.method == 'POST':
        if request.POST.get('post_id') and request.POST.get('page'):
            post_id = request.POST.get('post_id')
            page = request.POST.get('page')
            print(page)
            if post_id and page:
                reviews = Review.objects.filter(content_id=post_id, parent_id=None).order_by('-review_time_index')[
                          int(page) * 10:int(page) * 10 + 10]
                # 将关联的发布者信息也序列化为字典形式
                serialized_reviews = [
                    {
                        'review_id': review.review_id,
                        'content': review.review_content,
                        'author': {
                            'user_id': review.user_id.user_id,
                            'username': review.user_id.user_nickname if review.user_id.user_nickname else review.user_id.user_name,
                            'user_headicon': review.user_id.user_headicon.url,
                        },
                        'review_parent_id': review.parent_id.review_id if review.parent_id else None,
                        'review_time': review.review_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'children_count': Review.objects.filter(parent_id=review.review_id).count(),
                    }
                    for review in reviews
                ]
                return JsonResponse({'code': 200,'all_reviews_count': Review.objects.filter(content_id=post_id).count(), 'data': serialized_reviews, 'msg': '获取成功'})
                # return data_handle.db_to_json2(request, reviews)
            else:
                return JsonResponse({'code': 400, 'msg': '参数错误'})
        else:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
    return JsonResponse({'code': 401, 'msg': '请求方式错误'})


def get_specific_review_children(request):
    if request.method == 'POST':
        if request.POST.get('review_id'):
            review_id = request.POST.get('review_id')
            specific_review = Review.objects.get(review_id=review_id)
            if review_id:
                reviews = Review.objects.filter(parent_id=review_id).order_by('-review_time_index')
                # 将关联的发布者信息也序列化为字典形式
                serialized_reviews = [
                    {
                        'review_id': review.review_id,
                        'content': review.review_content,
                        'author': {
                            'user_id': review.user_id.user_id,
                            'username': review.user_id.user_nickname if review.user_id.user_nickname else review.user_id.user_name,
                            'user_headicon': review.user_id.user_headicon.url,
                        },
                        'review_parent_id': review.parent_id.review_id if review.parent_id else None,
                        'review_time': review.review_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'children_count': Review.objects.filter(parent_id=review.review_id).count(),
                    }
                    for review in reviews
                ]
                return JsonResponse({'code': 200, 'parent_id': specific_review.parent_id.review_id if specific_review.parent_id else None, 'data': serialized_reviews, 'msg': '获取成功'})
                # return data_handle.db_to_json2(request, reviews)
            else:
                return JsonResponse({'code': 400, 'msg': '参数错误'})
        return JsonResponse({'code': 401, 'msg': '请求方式错误'})
