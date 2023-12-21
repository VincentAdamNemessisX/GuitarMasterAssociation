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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from TestUnit.views import *
from exceptionhandler import views as excep_views
from post.views import *
from user.views import *
from zone.views import *
from collection.views import *
from feedback.views import *

handler404 = excep_views.notfound
handler500 = excep_views.nopower

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index),
                  path('404/', excep_views.notfound),
                  path('500/', excep_views.nopower),
                  path('index/', index),
                  path('user/', user),
                  path('user/collection/more/', user_collection_more),
                  path('collection/remove/', delete_specific_collection),
                  path('post/remove/', delete_specific_post),
                  path('post/edit/', update_post),
                  path('user/update/', user_info_update),
                  path('signin/', signin),
                  path('signup/', signup),
                  path('signout/', signout),
                  path('zone/', zone),
                  path('post-normal/', post_normal),
                  path('post-immersion/', post_immersion),
                  path('random-post/', random_post),
                  path('about/', about),
                  path('contact/', contact),
                  path('help/', faq_help),
                  path('pricing/', pricing),
                  path('privacy/', privacy),
                  path('search/', search),
                  path('story/', story),
                  path('story-details/', story_details),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
document_root = settings.STATIC_ROOT
