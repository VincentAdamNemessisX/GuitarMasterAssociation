from django.shortcuts import render
from user.models import User


# Create your views here.
def about(request):
    return render(request,  'about.html')


def blog_1(request):
    return render(request,  'blog-1.html')


def blog_2(request):
    return render(request,  'blog-2.html')


def blog_3(request):
    return render(request,  'blog-3.html')


def blog_4(request):
    return render(request,  'blog-4.html')


def blog_5(request):
    return render(request,  'blog-5.html')


def blog_details(request):
    return render(request,  'blog-details.html')


def contact(request):
    return render(request,  'contact.html')


def event(request):
    return render(request,  'event.html')


def event_details(request):
    return render(request,  'event-details.html')


def faq(request):
    return render(request,  'faq.html')


def gallery(request):
    return render(request,  'gallery.html')


def index_2(request):
    return render(request,  'index-2.html')


def member(request):
    return render(request,  'member.html')


def member_details(request):
    return render(request, 'member-details.html')


def pricing(request):
    return render(request, 'pricing.html')


def privacy(request):
    return render(request, 'privacy.html')


def search(request):
    return render(request, 'search.html')


def story(request):
    return render(request, 'story.html')


def story_details(request):
    return render(request, 'story-details.html')
