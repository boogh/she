from django.conf.urls import url
from . import views

# namespace = merge

urlpatterns = [
    # url(r'^project/(?P<pk>[0-9]+)/$', views.DesktopMerge.as_view(), name='merge-project-desktop'),
    url(r'^project/(?P<project_id>[0-9]+)/$', views.mergeDesktop, name='merge-project-desktop'),
    # url(r'^project/(?P<list_id>[0-9]+)/update $', views.updateReport, name='report-update'),


    # should be removed
    # url(r'^project/(?P<pk>[0-9]+)/Making-an-Evaluation-list$', views.EvaluationList.as_view(), name='making-evaluation-list'),
    # url(r'^project/(?P<list_id>[0-9]+)/delete-list$', views.deleteList , name='delete-list'),
    #url(r'^project/(?P<list_id>[0-9]+)/add-evaluation-to-list', views.addEvalToReport , name='add-evaluation-to-list' ),
    #url(r'^project/(?P<list_id>[0-9]+)/remove-evaluation-from-list', views.removeEvalFromReport , name='remove-evaluation-from-list' ),
    # url(r'^project/(?P<project_id>[0-9]+)/newEvalList$', views.newEvalList, name='newEvalList-ajax'),


    # should be changed:
    # url(r'^project/(?P<list_id>[0-9]+)/merge_selected_evaluations', views.mergeEvals , name='merge_selected_evaluations' ),

    # changed url
    url(r'^project/(?P<project_id>[0-9]+)/merge_selected_evaluations', views.mergeEvaluations , name='merge_evaluations' ),
    url(r'^project/(?P<pk>[0-9]+)/update-merged-evaluation', views.UpdateMergedEvaluation.as_view() , name='update-merged-evaluation' ),
    url(r'^project/(?P<eval_id>[0-9]+)/(?P<se_eval_id>[0-9]+)/remove-selected-evaluation', views.removeSelectedEval , name='remove-selected-evaluation' ),
    url(r'^project/(?P<eval_id>[0-9]+)/(?P<se_eval_id>[0-9]+)/make-new-merge-evaluation', views.makeNewMergeEval , name='make-new-merge-evaluation' ),



    url(r'^project/(?P<project_id>[0-9]+)/(?P<merge>\d{1})/export-docx', views.exportDocFile, name='export-doc-file'),
    url(r'^project/(?P<project_id>[0-9]+)/(?P<merge>\d{1})/export-html$', views.exportHtmlEvals, name='export-html-file'),
    # url(r'^project/(?P<list_id>[0-9]+)/export-csv$', views.exportCsvFile, name='export-csv-file'),

    url(r'^project/(?P<eval_id>[0-9]+)/recommend$', views.recommend, name='recommend'),
    url(r'^project/(?P<eval_id>[0-9]+)/recommend_ajax$', views.recommendPlaceBase, name='recommend-ajax'),

     # -----report  ------
    url(r'^project/(?P<project_id>[0-9]+)/report-html$', views.reportHtml, name='report-html'),

]