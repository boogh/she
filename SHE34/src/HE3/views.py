from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from HE3.models import Project, Evaluation, SetOfHeuristics, HeuristicPrinciples
from django.core.urlresolvers import reverse_lazy,reverse
# from .forms import ProjectForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView, ListView,DetailView
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# from .tables import EvaluationsTables

#
@login_required
def showDashboard(request):
    model = Project
    template_name = 'HE3/dashboard.html'
    user = request.user
    projects = Project.objects.all()
    heuristicSets = SetOfHeuristics.objects.all().filter(creator = user)
    asmanager = projects.filter(manager=user.pk)
    asevalutor = projects.filter(evaluators=user.pk)
    now = timezone.now()
    context = {'asmanager': asmanager, 'asevalutor': asevalutor , 'heuristicSets' : heuristicSets , 'now' : now.date()}

    return render(request, template_name, context)


# class ProjectDetail(generic.detail.DetailView):
#     model = Project
#     template_name = 'HE3/project_detail.html'
#     context_object_name = 'project'
#
#     def get_context_data(self,model, **kwargs):
#         context = super(ProjectDetail, self).get_context_data(**kwargs)
#         context['now'] = timezone.now().date()
#
#         return context



# class ProjectForEvaluatorDetail(generic.detail.DetailView):
#     model = Project
#     template_name = 'HE3/project_detail_for_evaluator.html'
#     context_object_name = 'project'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProjectForEvaluatorDetail, self).get_context_data(**kwargs)
#         now = timezone.now()
#         context['now'] = now.date()
#         return context


# class ProjectList(generic.list.ListView):
#     model = Project
#     template_name = 'music/project_list.html'
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Project.objects.all()
#         # queryset= super(ProjectList,self).get_queryset()
#         queryset1= queryset.filter(manager=user.pk)
#         # queryset2 = queryset.filter(evalutors = user.pk)
#
#         return queryset1
#     def get_context_data(self, **kwargs):
#         context =

# class ProjectList(LoginRequiredMixin,generic.ListView):
#     template_name = 'HE/dashboard.html'
#     model = Project
#
# def addProject(request):

class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'link', 'setOfHeuristics', 'description', 'deadline', 'evaluators']
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')

    def form_valid(self, form):
        user = self.request.user
        form.instance.manager = user
        return super(ProjectCreate, self).form_valid(form)

# class ProjectCreate(FormView):
#     template_name = 'HE3/project_form.html'
#     form_class = ProjectForm
#     success_url = reverse_lazy('profiles:dashboard:user-dashboard')
#
#     def form_valid(self, form):
#         user = self.request.user
#         form.instance.manager = user
#         return super(ProjectCreate, self).form_valid(form)

class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name', 'link', 'setOfHeuristics', 'description', 'deadline', 'evaluators']
    # success_url = reverse_lazy('profiles:dashboard:user-dashboard')

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('profiles:dashboard:project_detail' , kwargs={'pk' : pk})


# class ProjectDelete(DeleteView):
#     model = Project
#     # success_url = reverse_lazy('profiles:dashboard:user-dashboard')
#     # success_url =  reverse_lazy(request.META.get('HTTP_REFERER'))
#     def get_success_url(self):
#         return reverse_lazy(self.request.META.get('HTTP_REFERER'))

@login_required
def projectDelete(request, project_id):
    Project.objects.get(pk=project_id).delete()
    return redirect('profiles:dashboard:user-dashboard')



class EvaluationCreate(CreateView):
    model = Evaluation
    fields = ['title','place', 'heurPrincip', 'description', 'recommendation', 'positivity' , 'severity' ,'frequency' ]
    # success_url = reverse_lazy('profiles:dashboard:user-dashboard')

    def form_valid(self, form):
        user = self.request.user
        projectId = self.kwargs['pk']
        project = Project.objects.get(pk=projectId)
        form.instance.ofProject = project
        form.instance.evaluator = user

        return super(EvaluationCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context= super(EvaluationCreate,self).get_context_data(**kwargs)
        context['project'] = self.kwargs
        return context

class EvaluationDetail(DetailView):
    model =Evaluation
    template_name = 'HE3/evaluations/evaluation_detail.html'
    context_object_name = 'evaluation'


class EvaluationUpdate(UpdateView):
    model = Evaluation
    fields = ['title','place', 'heurPrincip', 'description', 'recommendation', 'positivity' , 'severity' ,'frequency' ]

    def get_context_data(self, **kwargs):
        context= super(EvaluationUpdate,self).get_context_data(**kwargs)
        context['project'] = self.kwargs
        return context

@login_required
def EvaluatorDelete(request , project_id):

    user = request.user
    project = Project.objects.get(pk=project_id)
    evaluator = project.evaluators.get(pk=user.pk)
    project.evaluators.remove(evaluator)
    return redirect('profiles:dashboard:user-dashboard')
    # return redirect(request.META.get('HTTP_REFERER'))

@login_required
def evaluationDuplicate(request , eval_id):

    eval = Evaluation.objects.get(id = eval_id)
    eval.pk =None
    eval.title = eval.title + '_copy'
    eval.save()

    # Evaluation.objects.create( ofProject=eval.ofProject,
    #     manager=eval.manager,
    #                           evaluator=request.user,
    #                            heurPrincip=eval.heurPrincip,
    #                            place=eval.place,
    #                            description=eval.description,
    #                            recommendation=eval.recommendation,
    #
    #
    #                           )
    return redirect(request.META.get('HTTP_REFERER'))

    # return redirect('profiles:dashboard:project_detail' , eval.ofProject.id)


# def projectDetailForEvaluator(request, project_id):
#     project = Project.objects.get(pk = project_id)
#     user = request.user
#     evaluationsOfUser = project.evaluation_for_project.filter(evaluator = user)
#
#     # table = EvaluationsTables(evaluationsOfUser)
#     # RequestConfig(request).configure(table)
#
#     template_name = 'HE3/project_detail.html'
#     context = {'now': timezone.now().date() ,'project': project ,'evaluations' :evaluationsOfUser }
#
#     return render(request,template_name, context )

# def projectDetailForManager(request, project_id):
#     project = Project.objects.get(pk = project_id)
#     user = request.user
#     evaluations= project.evaluation_for_project.all()
#     evaluators=project.evaluators.all()
#     # table = EvaluationsTables(evaluationsOfUser)
#     # RequestConfig(request).configure(table)
#
#     template_name = 'HE3/project_detail.html'
#     context = {'now': timezone.now().date() ,'project': project ,'evaluations' :evaluations ,'evaluators':evaluators }
#
#     return render(request,template_name, context )

class ProjectDetail(DetailView):
    model = Project
    template_name = 'HE3/project_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Project,pk =self.kwargs.get('pk'))
    def get_context_data(self, **kwargs):
        context = super(ProjectDetail,self).get_context_data(**kwargs)
        project = self.get_object()
        allEvaluations = project.evaluation_for_project.all()

        if (self.request.user == project.manager):
            evaluations = allEvaluations
        elif (self.request.user in project.evaluators.all()):
            evaluations = allEvaluations.filter(evaluator= self.request.user)

        context = { 'project' : project ,
                    'now' : timezone.now().date(),
                    'evaluations': evaluations,
                     }
        return context

def evaluationDelete(request , eval_id):
    Evaluation.objects.get(pk = eval_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))


class HeuristicSetCreate(CreateView):
    model = SetOfHeuristics
    fields = ['title', 'description']

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = user
        return super(HeuristicSetCreate , self).form_valid(form)

    # def get_success_url(self):
    #     set_id = self.kwargs['pk']
    #     return reverse('profiles:dashboard:set-detail' , kwargs={'set_id' : set_id})



@login_required
def setDelete(request, set_id):
    SetOfHeuristics.objects.get(pk=set_id).delete()
    return redirect('profiles:dashboard:user-dashboard')

# class HeuristicPrinciple(CreateView):
#     model = HeuristicPrinciples
#     fields = ['title' , 'description','SetOfHeuristics']
#     # success_url = reverse_lazy('profiles:dashboard:user-dashboard')


@login_required
def setDetail(request , set_id):
    set = SetOfHeuristics.objects.get(pk= set_id)

    return render(request, template_name='HE3/set/set_detail.html' , context={'set' : set})


