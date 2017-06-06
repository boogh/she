from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView,CreateView , UpdateView
from HE3.models import Project, Evaluation, Screenshots,Environment, ListOfEval
from django.utils import timezone
from docx import Document
import csv
import merg.recommend as rec
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse_lazy
from HE3.forms import MergeEvaluationForm

# Create your views here.

#
# class DesktopMerge(DetailView):
#     model = Project
#     template_name = 'merge/project-merge-desktop.html'
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Project, pk=self.kwargs.get('pk'))
#
#     def get_context_data(self, **kwargs):
#         context = super(DesktopMerge, self).get_context_data(**kwargs)
#         project = self.get_object()
#         allEvaluations = project.evaluation_for_project.all()
#         # evaluationsOfUser = allEvaluations.filter(evaluator=self.request.user)
#         # evaluators = project.evaluators.all()
#         # tableAllE = EvaluationsTablesForManager(allEvaluations)
#         # RequestConfig(self.request).configure(tableAllE)
#
#         context = {'project': project,
#                    'now': timezone.now().date(),
#                    'evaluations': allEvaluations,
#                    }
#         return context

def mergeDesktop(request, project_id):

    project = Project.objects.get(pk = project_id);
    if (project.manager == request.user):
        template_name = 'merge/merge.html'
        allEvaluations = project.evaluation_for_project.all()
        alreadyMerged = allEvaluations.filter(merged =True).values_list('mergedFromEvaluations' , flat = True)
        remainedEvals = allEvaluations.filter(merged=False).exclude( pk__in = alreadyMerged)
        context = {'project': project,
                   'now': timezone.now().date(),
                   'evals': remainedEvals,
                   'mergedEvals': allEvaluations.filter(merged=True),
                   'evaluators': project.evaluators.filter(pk__in = remainedEvals.values_list('evaluator', flat= True).distinct()),
                   }
        return render(request,template_name,context)
    else:
        return HttpResponse('Only Manager can access this page!')

# def newEvalList(request , project_id):
#     project = Project.objects.get(pk=project_id)
#     if request.method == 'POST' :
#         # name = request.POST.get['name' , False]
#
#         if 'name' in request.POST and request.POST['name']:
#             name = request.POST['name']
#         else:
#             return redirect('merge:merge-project-desktop' , project_id )
#         evalList = ListOfEval.objects.create(ofProject = project , fromUser =request.user , name = name )
#
#         return redirect('merge:report-update',  evalList.id )
#     return redirect('merge:merge-project-desktop', project_id)

# def updateReport (request ,list_id):
#     eval_list = ListOfEval.objects.get(pk=list_id)
#     project = eval_list.ofProject
#
#     if project.manager == request.user:
#         template_name = 'merge/merge_update.html'
#         allEvaluations = project.evaluation_for_project.all()
#         evalInList= eval_list.evaluations.all()
#         evaluations = allEvaluations.exclude(id__in = evalInList)
#         context = {'project': project,
#                    'now': timezone.now().date(),
#                    'evaluations': evaluations,
#                     'eval_list' : eval_list,
#                    }
#         return render(request, template_name, context)
#     else:
#         return HttpResponse('Only Manager can access this page!')

# def addEvalToReport(request , list_id):
#
#     list = ListOfEval.objects.get(pk = list_id)
#     project = list.ofProject
#     if request.is_ajax():
#         ids = request.POST.getlist('ids[]')
#         if ids:
#             evals= Evaluation.objects.filter(pk__in= ids)
#             list.evaluations.add(*evals)
#     return HttpResponse('success!')

# def removeEvalFromReport(request , list_id):
#
#     list = ListOfEval.objects.get(pk = list_id)
#     project = list.ofProject
#     if request.is_ajax():
#         ids = request.POST.getlist('ids[]')
#         if ids:
#             evals= Evaluation.objects.filter(pk__in= ids)
#             list.evaluations.remove(*evals)
#     # return HttpResponseRedirect(reverse ( 'merge:report-update', args = (list.id ,  )))
#     return HttpResponse('success!')

# def deleteList(request , list_id):
#
#     list = ListOfEval.objects.get(pk = list_id)
#     project = list.ofProject
#     list.delete()
#     return redirect(request.META.get('HTTP_REFERER'))

# def display_meta(request):
#     values = request.META.items()
#     values.sort()
#     html = []
#     for k, v in values:
#         html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
#     return HttpResponse('<table>%s</table>' % '\n'.join(html))

# def recommend(request , eval_id):
#
#     template_name = 'merge/recommendations.html'
#     eval = Evaluation.objects.get(id = eval_id)
#     project =eval.ofProject
#     resultplace = rec.placebase(eval)
#     resultdes = rec.descriptionBase(eval)
#     # result = rec.nearestN(eval)
#     # context = {'result': eval.ofProject}
#     resultids = set(resultplace + resultdes)
#     recommendList = project.evaluation_for_project.filter(pk__in =resultids)
#     # return render(request,template_name="merge/project-merge-desktop.html" , context=context )
#     # return render(request,template_name="merge/project-merge-desktop.html" , context=context )
#     return render(request,template_name=template_name,context={'recommendList' :recommendList}  )


# content base
@login_required
def recommend(request , eval_id):

    eval = Evaluation.objects.get(id = eval_id)
    project =eval.ofProject
    resultplace = rec.placebase(eval)
    # resultdes = rec.descriptionBase(eval)
    result = rec.nearestN(eval)
    # context = {'result': eval.ofProject}

    recPlaceBase = project.evaluation_for_project.filter(pk__in =resultplace)
    recDesBase = project.evaluation_for_project.filter(pk__in =result['resultDes'])
    recRecBase = project.evaluation_for_project.filter(pk__in =result['resultRec'])
    recTagseBase = project.evaluation_for_project.filter(pk__in =result['resultTags'])

    if request.is_ajax():
        # template_name = 'HE3/evaluations/e-panel-list.html'
        template_name = 'merge/user-based-evals.html'
        allRecommendedEvals = (recDesBase | recRecBase | recTagseBase).distinct()
        allEvaluations = project.evaluation_for_project.all()
        alreadyMerged = allEvaluations.filter(merged=True).values_list('mergedFromEvaluations', flat=True)

        context = {'evals' : allRecommendedEvals.exclude(pk__in= alreadyMerged) ,
                   'used_evaluations': allRecommendedEvals.filter(pk__in =alreadyMerged),
                   'evaluators': project.evaluators.filter(pk__in = allRecommendedEvals.values_list('evaluator', flat= True).distinct()),
                   }

    else:
        template_name = 'merge/recommendations.html'
        context = {'placeBase': recPlaceBase,
                   'desBase': recDesBase,
                   'recBase': recRecBase,
                   'tagBase': recTagseBase}

    return render(request,template_name=template_name,context= context )

# place base
def recommendAjax(request, eval_id):

    eval = Evaluation.objects.get(id=eval_id)
    project = eval.ofProject
    resultplace = rec.placebase(eval)
    result = {}
    result['evaluations'] = resultplace
    recPlaceBase = project.evaluation_for_project.filter(pk__in =resultplace)

    return render_to_response(template_name='HE3/evaluations/e-panel-list.html' , context= {'evaluations' : recPlaceBase})

# class EvaluationList(CreateView):
#     model = ListOfEval
#     template_name = 'merge/form-evaluation-list.html'
#     fields = ['name','evaluations']
#
#     def form_valid(self, form):
#         user = self.request.user
#         projectId = self.kwargs['pk']
#         project = Project.objects.get(pk=projectId)
#         form.instance.ofProject = project
#         form.instance.fromUser = user
#
#         return super(EvaluationList, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(EvaluationList, self).get_context_data(**kwargs)
#         context['project'] = self.kwargs
#         return context
#
#
#         # ofProject = models.ForeignKey(Project)
#         # fromUser = models.ForeignKey(User, related_name="Merge_manager")
#         # evaluations = models.ManyToManyField(Evaluation)
#         # name = models.CharField(max_length=50)
#         # logo = models.ImageField(name='Eval-Merg-Logo', upload_to='logo/%Y-%m-%d/', null=True, blank=True)
#         # mergeUrl = models.URLField(blank=True, null=True)
#         # exportedFile = models.FileField(blank=True, null=True)
#
#         # def form_valid(self, form):
#         #        user = self.request.user
#         #        projectId = self.kwargs['pk']
#         #        project = Project.objects.get(pk=projectId)
#         #        form.instance.ofProject = project
#         #        form.instance.evaluator = user
#         #
#         #        return super(EvaluationCreate, self).form_valid(form)
#         #
#         #    def get_context_data(self, **kwargs):
#         #        context= super(EvaluationCreate,self).get_context_data(**kwargs)
#         #        context['project'] = self.kwargs
#         #        return context

#---- export methods ---

# -----------merging evaluations -----------------------------------------------------

def mergeFields(evalList):
    # result = {k : "" for k in evalList[0].__dict__.keys()}
    result ={}
    stringList = ['description' , 'recommendation']
    stringWithKomma = ['place' , 'a_place' ]
    forAvg = ['frequency' , 'severity']
    for field in stringList :
        allvalues = set([ i.__dict__[field] for i in evalList])
        result [field] = "\n" .join(allvalues)
    for field in stringWithKomma :
        allvalues = set([i.__dict__[field]for i in evalList])
        result[field] = ",".join(allvalues)
    for field in forAvg :
        allvalues = [int(i.__dict__[field]) for i in evalList]
        result[field] = str(sum(allvalues) / len(allvalues))

    heurPrincips =[]
    for e in evalList:
        heurPrincips.extend(list(e.heurPrincip.all()))
    heurPrincips = list(set(heurPrincips))

    return result , heurPrincips

# def mergeEvals(request , list_id):
#
#     list = ListOfEval.objects.get(pk=list_id)
#     project = list.ofProject
#     resultEval = Evaluation(ofProject = project , evaluator = project.manager)
#
#     if request.is_ajax():
#         ids = request.POST.getlist('ids[]')
#         name = request.POST.get('name')
#         addtolist = request.POST.get('addtolist')
#         if ids and len(ids) > 1:
#             evals = Evaluation.objects.filter(pk__in=ids)
#             fields , heurPrincips = mergeFields(evals)
#             resultEval.__dict__.update(fields)
#             if name:
#                 resultEval.title = name
#             else:
#                 resultEval.title = 'Merged Evaluations'
#             resultEval.save()
#             resultEval.heurPrincip.add(*heurPrincips)
#
#             if addtolist :
#                 list.evaluations.add(resultEval)
#
#             url = '/users/me/dashboard/project/UpdateEvaluation/' + str(resultEval.id) + '/'
#             response = {'status' : 1 , 'message' : 'You can edit the result of merge!' , 'url' : url}
#             return HttpResponse(json.dumps(response), content_type='application/json')
#     return HttpResponse('not success')

def mergeScreenshots(resultEval, listEvals):
    for eval in listEvals:
        screenobject =Screenshots(caption=eval.caption , screenshot =eval.screenshot)
        screenobject.save()
        resultEval.mergedScreenshots.add(screenobject)

# function to merge multiple evaluation
def mergeEvaluations(request , project_id):

    project = Project.objects.get(pk=project_id)
    resultEval = Evaluation(ofProject =project , evaluator=project.manager , merged= True)

    if request.is_ajax():
        ids = request.POST.getlist('ids[]')
        name = request.POST.get('name')

        if ids and len(ids) > 1:
            evals = Evaluation.objects.filter(pk__in=ids)
            fields , heurPrincips = mergeFields(evals)
            resultEval.__dict__.update(fields)
            if name:
                resultEval.title = name
            else:
                resultEval.title = 'Merged Evaluations'
            resultEval.save()
            resultEval.heurPrincip.add(*heurPrincips)
            mergeScreenshots(resultEval,evals)
            # adding evaluators and evaluations id to the merged evaluation
            eval_ids = evals.values_list('pk' ,flat=True)
            evaluator_ids = evals.values_list('evaluator_id' , flat=True).distinct()
            resultEval.mergedFromEvaluations.add(*eval_ids)
            resultEval.merdedFromEvaluators.add(*evaluator_ids)

            # url = '/users/me/dashboard/project/update-merged-evaluation/' + str(resultEval.id) + '/'
            url = '/merge/project/' + str(resultEval.id) +'/update-merged-evaluation/'
            response = {'status' : 1 , 'message' : 'You can edit the result of merge!' , 'url' : url}
            return HttpResponse(json.dumps(response), content_type='application/json')
    return HttpResponse('not success')

class UpdateMergedEvaluation(UpdateView):

    # eval = Evaluation.objects.get(pk=eval_id)
    # project = eval.ofProject
    template_name ='HE3/evaluation_form.html'

    # form =MergeEvaluationForm(eval)
    model = Evaluation
    # fields = ['title','place', 'heurPrincip', 'description', 'recommendation', 'positivity' , 'severity' ,'frequency' ]
    form_class = MergeEvaluationForm

    def get_context_data(self, **kwargs):
        context = super(UpdateMergedEvaluation, self).get_context_data(**kwargs)
        eval = Evaluation.objects.get(pk=self.kwargs['pk'])
        context['project'] = eval.ofProject
        return context

    def get_form_kwargs(self):
        kwargs = super(UpdateMergedEvaluation, self).get_form_kwargs()
        kwargs['eval_id'] = self.kwargs['pk']
        return kwargs

    # return render(request, context={'project': project,'form' : form} ,template_name=template_name)

# ------------Report ----------------
def reportHtml(request , project_id):
    project = Project.objects.get(pk=project_id)
    mergedEvals = project.evaluation_for_project.filter(merged = True)
    evals = project.evaluation_for_project.filter(merged = False)
    environments = Environment.objects.filter(creator__in = project.evaluators.all()).order_by('creator')
    context = { 'project' : project ,
                'evaluations' : evals.order_by('positivity' , 'evaluator' , 'severity'),
                'mergedEvals' : mergedEvals,
                'environments' :environments,
                'pos_merge' :mergedEvals.filter(positivity = 'p'),
                'neg_merge' :mergedEvals.filter(positivity = 'n'),
    }

    return render (request , template_name='merge/report.html' , context=context)



# --------Export methods  ---------------------------------------------------------------

@login_required
def exportHtmlEvals(request, project_id, merge):
    project = Project.objects.get(pk=project_id)
    evals = project.evaluation_for_project.all()
    merged = False
    if int(merge[0]) == 0:
        evals = evals.filter(merged=False)
    elif int(merge[0]) == 1:
        merged = True
        evals = evals.filter(merged=True)

    template_name = 'merge/htmlexport.html'
    context = { 'evaluations' : evals ,
                'project': project ,
                'merged' :merged ,}

    return render(request,template_name=template_name,context=context)

@login_required
def exportDocFile(request, list_id ):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=demo.docx'

    listofeval = ListOfEval.objects.get(pk=list_id)
    project = listofeval.ofProject
    doc = fillDocFile(project, listofeval)
    doc.save(response)

    return response
@login_required
def exportCsvFile(request,list_id):
    listofeval = ListOfEval.objects.get(pk=list_id)
    evaluations = listofeval.evaluations.all().order_by('heurPrincip')
    project = listofeval.ofProject
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename = "Report.csv"'

    writer = csv.writer(response)
    writer.writerow([ 'Project: ', project.name,' Description: ' ,project.description,' link: ', project.link , ' Manager: ', project.manager])
    for e in evaluations:
        writer.writerow([e.title ,
                         e.place,
                         e.heurPrincip,
                         e.description,
                         e.recommendation,
                         e.get_positivity_display(),
                         e.get_severity_display(),
                         e.get_frequency_display(),
                         e.tags,
                         e.evaluator])

    return response

def fillDocFile(project, listofeval):
    doc = Document()
    doc.add_heading(str(project.name + 'Report'))
    p = doc.add_paragraph('A plain paragraph')
    p.add_run('bold').bold = True
    p.add_run(' and some')
    p.add_run('italic.').italic = True

    doc.add_heading('Heading, level 1', level=1)
    doc.add_paragraph('Intense quote', style='IntenseQuote')

    doc.add_paragraph(
        'first item in unordered list', style='ListBullet'
    )
    doc.add_paragraph(
        'first item in ordered list', style='ListNumber'
    )

    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    # for item in listofeval.objects.all():
    #     row_cells = table.add_row().cells
    #     row_cells[0].text = str(item.name)
    #     row_cells[1].text = str(item.genre)
    #     row_cells[2].text = item.artist

    doc.add_page_break()

    return doc

