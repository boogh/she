
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


# namespace = profiles:dashboard:
app_name='HE3'


urlpatterns = [
    url(r'^$', views.showDashboard, name='user-dashboard'),
    # url(r'^' , views.ProjectList.as_view(), name='dashboard'),
    url(r'^project/(?P<pk>[0-9]+)/$', login_required(views.ProjectDetail.as_view()), name='project_detail'),
    # url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view(), name='project_detail_for_evaluator'),
    # url(r'^project/(?P<project_id>[0-9]+)/$', views.projectDetailForManager, name='project_detail'),

    # url(r'^project/evaluator/(?P<pk>[0-9]+)/$', views.ProjectForEvaluatorDetail.as_view(), name='project_detail_for_evaluator'),
    # url(r'^project/evaluator/(?P<project_id>[0-9]+)/$', views.projectDetailForEvaluator, name='project_detail_for_evaluator'),

    url(r'^project/evaluator/(?P<project_id>[0-9]+)/deleteProject/$' , views.EvaluatorDelete , name='delete-evaluator'),

    url(r'^add_project/$' , login_required(views.ProjectCreate.as_view()),name='project_create'),
    url(r'^project/(?P<pk>[0-9]+)/update/$', login_required(views.ProjectUpdate.as_view()), name='project_update'),
    # url(r'^project/(?P<pk>[0-9]+)/delete/$', login_required(views.ProjectDelete.as_view()), name='project_delete'),
    url(r'^project/(?P<project_id>[0-9]+)/delete/$', views.projectDelete, name='project_delete'),

    url(r'^project/AddEvaluation/(?P<pk>[0-9]+)/$', login_required(views.EvaluationCreate.as_view()), name='Add-Evaluation'),
    url(r'^project/EvaluationDetail/(?P<pk>[0-9]+)/$', login_required(views.EvaluationDetail.as_view()), name='evaluation-detail'),
    url(r'^project/UpdateEvaluation/(?P<pk>[0-9]+)/$', login_required(views.EvaluationUpdate.as_view()), name='evaluation-update'),
    url(r'^project/DuplicateEvaluation/(?P<eval_id>[0-9]+)/$', views.evaluationDuplicate, name='evaluation-duplicate'),
    url(r'^project/DeleteEvaluation/(?P<eval_id>[0-9]+)/$', views.evaluationDelete, name='evaluation-delete'),

    url(r'^CreateHeuristicSet' , login_required(views.HeuristicSetCreate.as_view()), name='HeuristicSet-create'),
    url(r'^DeleteHeuristicSet/(?P<set_id>[0-9]+)/$' , views.setDelete, name='HeuristicSet_delete'),
    # url(r'^HeuristicPrincipleCreate/(?P<pk>[0-9]+)/$', login_required(views.HeuristicPrinciple.as_view()),name='add-principle'),
    url(r'^SetDetail/(?P<set_id>[0-9]+)/$', views.setDetail, name='set-detail'),
    url(r'^addPrinciple/(?P<set_id>[0-9]+)/$', views.addPrinciple, name='add-principle'),
    url(r'^updatePrinciple/(?P<p_id>[0-9]+)/$', views.updatePrinciple, name='update-principle'),
    url(r'^deletePrinciple/(?P<p_id>[0-9]+)/$', views.deletePrinciple, name='del-principle'),

    url(r'^CreateEnvironment', login_required(views.EnvironmentCreate.as_view()), name='environment-create'),
    url(r'^delEnvironment/(?P<env_id>[0-9]+)/', views.deleteEnvironment , name='environment-del'),
    url(r'^UpdateEnvironment/(?P<pk>[0-9]+)/', login_required(views.EnvironmentUpdate.as_view()) , name='environment-update'),

]