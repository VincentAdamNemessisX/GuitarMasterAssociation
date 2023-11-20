"""GuitarMasterAssociation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from TestUnit.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('404/', notfound),
    path('about/', about),
    path('blog-1/', blog_1),
    path('blog-2/', blog_2),
    path('blog-3/', blog_3),
    path('blog-4/', blog_4),
    path('blog-5/', blog_5),
    path('blog-details/', blog_details),
    path('contact/', contact),
    path('event/', event),
    path('event-details/', event_details),
    path('faq/', faq),
    path('gallery/', gallery),
    path('index/', index),
    path('index-2/', index_2),
    path('member/', member),
    path('member-details/', member_details),
    path('pricing/', pricing),
    path('privacy/', privacy),
    path('search/', search),
    path('signin/', signin),
    path('signup/', signup),
    path('story/', story),
    path('story-details/', story_details),
]
