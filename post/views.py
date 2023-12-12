from django.shortcuts import render
from custom import verify


# Create your views here.
def index(request):
    current_user = verify.verify_current_user(request)
    return render(request, 'index.html', {'login_user': current_user})
