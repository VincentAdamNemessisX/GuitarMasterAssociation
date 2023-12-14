import random

from django.shortcuts import render

from post.models import Post


# Create your views here.
def index(request):
    return render(request, 'index.html')


def post_normal(request):
    return render(request, 'post_details_normal.html')


def post_immersion(request):
    return render(request, 'post_details_immersion.html')


def random_post(request):
    post_ids = Post.objects.all().values_list('post_id', flat=True)
    random.shuffle(list(post_ids))
    rd = random.randint(0, len(post_ids) - 1)
    specific_post = Post.objects.get(post_id=post_ids[rd])
    return render(request, 'post_details_' + specific_post.post_layout_mode + '.html', {'post': specific_post})
