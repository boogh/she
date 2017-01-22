
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^', views.showDashboard, name='dashboard'),
    # url(r'^' , views.ProjectList.as_view(), name='dashboard'),
]