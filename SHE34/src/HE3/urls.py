
from django.conf.urls import url
from . import views

app_name='HE3'


urlpatterns = [
    url(r'^$', views.showDashboard, name='user-dashboard'),
    # url(r'^' , views.ProjectList.as_view(), name='dashboard'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='project_detail'),

    # url(r'^project/evaluator/(?P<pk>[0-9]+)/$', views.ProjectForEvaluatorDetail.as_view(), name='project_detail_for_evaluator'),
    url(r'^project/evaluator/(?P<project_id>[0-9]+)/$', views.projectDetailForEvaluator, name='project_detail_for_evaluator'),

    url(r'^project/evaluator/(?P<project_id>[0-9]+)/deleteProject/$' , views.EvaluatorDelete , name='delete-evaluator'),

    url(r'^add_project/$' , views.ProjectCreate.as_view(),name='project_create'),
    url(r'^project/(?P<pk>[0-9]+)/update/$', views.ProjectUpdate.as_view(), name='project_update'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name='project_delete'),
    url(r'^project/AddEvaluation/(?P<pk>[0-9]+)/$', views.EvaluationCreate.as_view(), name='Add-Evaluation'),


]