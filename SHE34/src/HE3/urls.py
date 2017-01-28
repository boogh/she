
from django.conf.urls import url
from . import views

app_name='HE3'


urlpatterns = [
    url(r'^$', views.showDashboard, name='user-dashboard'),
    # url(r'^' , views.ProjectList.as_view(), name='dashboard'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='project_detail'),
    url(r'^add_project/$' , views.ProjectCreate.as_view(),name='project_create'),
]