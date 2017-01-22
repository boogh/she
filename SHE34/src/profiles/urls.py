from django.conf.urls import url,include
from . import views
import HE3.urls

urlpatterns = [
    url(r'^me$', views.ShowProfile.as_view(), name='show_self'),
    url(r'^me/edit$', views.EditProfile.as_view(), name='edit_self'),
    url(r'^(?P<slug>[\w\-]+)$', views.ShowProfile.as_view(),
        name='show'),
    url(r'^me/dashboard', include(HE3.urls, namespace='dashboard')),
]
