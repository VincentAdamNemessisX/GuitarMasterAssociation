from django.shortcuts import render


# Create your views here.
def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


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
