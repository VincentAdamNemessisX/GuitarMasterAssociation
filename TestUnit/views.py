from django.shortcuts import render

from custom import verify


# Create your views here.
def about(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'about.html', {'login_user': current_user})


def blog_1(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'blog-1.html', {'login_user': current_user})


def blog_2(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'blog-2.html', {'login_user': current_user})


def blog_3(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'blog-3.html', {'login_user': current_user})


def blog_4(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'blog-4.html', {'login_user': current_user})


def blog_5(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'blog-5.html', {'login_user': current_user})


def blog_details(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'blog-details.html', {'login_user': current_user})


def contact(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'contact.html', {'login_user': current_user})


def event(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'event.html', {'login_user': current_user})


def event_details(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'event-details.html', {'login_user': current_user})


def faq(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'faq.html', {'login_user': current_user})


def gallery(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'gallery.html', {'login_user': current_user})



def member_details(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'member-details.html', {'login_user': current_user})


def pricing(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'pricing.html', {'login_user': current_user})


def privacy(request):
    current_user = verify.verify_current_user(request)
    print(current_user)
    return render(request, 'privacy.html', {'login_user': current_user})


def search(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'search.html', {'login_user': current_user})


def story(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'story.html', {'login_user': current_user})


def story_details(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'story-details.html', {'login_user': current_user})
