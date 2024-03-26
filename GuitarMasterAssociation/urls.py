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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from TestUnit.views import *
from collection.views import *
from exceptionhandler import views as excep_views
from feedback.views import *
from message.views import *
from post.views import *
from review.views import *
from user.views import *
from zone.views import *

handler404 = excep_views.notfound
handler500 = excep_views.nopower

urlpatterns = [
                  re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                  url(r'^favicon.ico$', RedirectView.as_view(url=r'/static/fav.png')),
                  path('admin/', admin.site.urls),
                  path('', index),
                  path('404/', excep_views.notfound),
                  path('500/', excep_views.nopower),
                  path('index/', index),
                  path('user/', user),
                  path('user/update/', user_info_update),
                  path('user/collection/more/', user_collection_more),
                  path('collection/remove/', delete_specific_collection),
                  path('post/publish/', post_publish),
                  path('post/update/', update_post),
                  path('post/remove/', delete_specific_post),
                  path('search/posts/', search_posts),
                  path('review/get/all/', get_init_reviews),
                  path('review/get/children/', get_specific_review_children),
                  path('review/get/more/', load_more_reviews),
                  path('signin/', signin),
                  path('signup/', signup),
                  path('signout/', signout),
                  path('zone/', zone),
                  path('help/', faq_help),
                  path('post-normal/', post_normal),
                  path('post/like/', update_post_like),
                  path('post/collect/', update_post_collection),
                  path('post-immersion/', post_immersion),
                  path('random-post/', random_post),
                  path('message/help/', message_help),
                  path('rank/', rank),
                  path('api/post/upload/image/', post_upload_image),
                  path('api/post/review/', publish_review),
                  path('api/get/messages/', get_messages),
                  path('api/read/message/', read_message),
                  path('api/review/pass/audit/', pass_audit_review),
                  path('api/review/reject/audit/', reject_audit_review),
                  path('api/post/pass/audit/', pass_audit_post),
                  path('api/post/reject/audit/', reject_audit_post),
                  path('api/user/freeze/', freeze_user),
                  path('api/user/unfreeze/', unfreeze_user),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
document_root = settings.STATIC_ROOT
