from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView,CreateView
from HE3.models import Project , ListOfEval, Evaluation
from django.utils import timezone
from docx import Document
import csv
import merg.recommend as rec
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt



from django.core.urlresolvers import reverse_lazy

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

def makeReport(request, project_id):

    project = Project.objects.get(pk = project_id);
    if (project.manager == request.user):
        template_name = 'merge/merge.html'
        allEvaluations = project.evaluation_for_project.all()
        context = {'project': project,
                   'now': timezone.now().date(),
                   'evaluations': allEvaluations,
                   }
        return render(request,template_name,context)
    else:
        return HttpResponse('Only Manager can access this page!')

# @csrf_exempt

def newEvalList(request , project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST' :
        # name = request.POST.get['name' , False]

        if 'name' in request.POST and request.POST['name']:
            name = request.POST['name']
        else:
            return redirect('merge:merge-project-desktop' , project_id )
        evalList = ListOfEval.objects.create(ofProject = project , fromUser =request.user , name = name )

        return redirect('merge:report-update',  evalList.id )
    return redirect('merge:merge-project-desktop', project_id)


def updateReport (request ,list_id):
    eval_list = ListOfEval.objects.get(pk=list_id)
    project = eval_list.ofProject

    if project.manager == request.user:
        template_name = 'merge/merge_update.html'
        allEvaluations = project.evaluation_for_project.all()
        evalInList= eval_list.evaluations.all()
        evaluations = allEvaluations.exclude(id__in = evalInList)
        context = {'project': project,
                   'now': timezone.now().date(),
                   'evaluations': evaluations,
                    'eval_list' : eval_list,
                   }
        return render(request, template_name, context)
    else:
        return HttpResponse('Only Manager can access this page!')

@csrf_exempt
def addEvalToReport(request , list_id):
    print('list_id =  ' , list_id)
    list = ListOfEval.objects.get(pk = list_id)
    project = list.ofProject
    if request.is_ajax():
        ids = request.POST.getlist('ids[]')
        if ids:
            evals= Evaluation.objects.filter(pk__in= ids)
            list.evaluations.add(*evals)
    # return redirect('merge:report-update', list_id)
    # return HttpResponseRedirect(reverse ( 'merge:report-update', args = (list.id ,  )))
    return HttpResponse('success!')




def deleteList(request , list_id):

    list = ListOfEval.objects.get(pk = list_id)
    project = list.ofProject
    list.delete()
    return redirect(request.META.get('HTTP_REFERER'))



def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))



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
    # return render(request,template_name="merge/project-merge-desktop.html" , context=context )
    # return render(request,template_name="merge/project-merge-desktop.html" , context=context )

    if request.is_ajax():
        template_name = 'HE3/evaluations/e-panel-list.html'
        context = {'evaluations' : set (list(recDesBase) + list(recTagseBase) + list(recRecBase))}

    else:
        template_name = 'merge/recommendations.html'
        context = {'placeBase': recPlaceBase,
                   'desBase': recDesBase,
                   'recBase': recRecBase,
                   'tagBase': recTagseBase}

    return render(request,template_name=template_name,context= context )


def recommendAjax(request, eval_id):

    eval = Evaluation.objects.get(id=eval_id)
    project = eval.ofProject
    resultplace = rec.placebase(eval)
    result = {}
    result['evaluations'] = resultplace
    recPlaceBase = project.evaluation_for_project.filter(pk__in =resultplace)

    # return HttpResponse(json.dumps(result) , content_type='application/json')
    return render_to_response(template_name='HE3/evaluations/e-panel-list.html' , context= {'evaluations' : recPlaceBase})

class EvaluationList(CreateView):
    model = ListOfEval
    template_name = 'merge/form-evaluation-list.html'
    fields = ['name','evaluations']

    def form_valid(self, form):
        user = self.request.user
        projectId = self.kwargs['pk']
        project = Project.objects.get(pk=projectId)
        form.instance.ofProject = project
        form.instance.fromUser = user

        return super(EvaluationList, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EvaluationList, self).get_context_data(**kwargs)
        context['project'] = self.kwargs
        return context


        # ofProject = models.ForeignKey(Project)
        # fromUser = models.ForeignKey(User, related_name="Merge_manager")
        # evaluations = models.ManyToManyField(Evaluation)
        # name = models.CharField(max_length=50)
        # logo = models.ImageField(name='Eval-Merg-Logo', upload_to='logo/%Y-%m-%d/', null=True, blank=True)
        # mergeUrl = models.URLField(blank=True, null=True)
        # exportedFile = models.FileField(blank=True, null=True)

        # def form_valid(self, form):
        #        user = self.request.user
        #        projectId = self.kwargs['pk']
        #        project = Project.objects.get(pk=projectId)
        #        form.instance.ofProject = project
        #        form.instance.evaluator = user
        #
        #        return super(EvaluationCreate, self).form_valid(form)
        #
        #    def get_context_data(self, **kwargs):
        #        context= super(EvaluationCreate,self).get_context_data(**kwargs)
        #        context['project'] = self.kwargs
        #        return context

@login_required
def exportHtmlFile(request , list_id):

    listofeval = ListOfEval.objects.get(pk=list_id)
    evaluations = listofeval.evaluations.all().order_by('heurPrincip')
    project = listofeval.ofProject
    template_name = 'merge/htmlexport.html'
    context = { 'project' : project ,
                'evaluations': evaluations}

    return render(request,template_name=template_name,context=context)

@login_required
def exportDocFile(request, list_id):
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


@login_required
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