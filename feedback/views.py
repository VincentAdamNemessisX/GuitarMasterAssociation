# Create your views here.
from django.shortcuts import render
from .models import *


def faq_help(request):
    help_list = Help.objects.all()
    return render(request, 'help.html', {'help_list': help_list})
