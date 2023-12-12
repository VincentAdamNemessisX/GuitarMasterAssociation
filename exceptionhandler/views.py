from django.shortcuts import render


# Create your views here.
def notfound(request, exception):
    return render(request,  '404.html', {'error': exception})


def nopower(request):
    return render(request,  '500.html')
