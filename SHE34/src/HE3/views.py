from django.shortcuts import render,redirect,get_object_or_404
from django.views import generic
from HE3.models import Project, Evaluation, SetOfHeuristics, HeuristicPrinciples, Environment , Screenshots
from django.core.urlresolvers import reverse_lazy,reverse
from .forms import Principle , EvaluationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView, ListView,DetailView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from HE3.forms import EvaluationForm, EvaluationFormUpdate
# from .tables import EvaluationsTables

#
@login_required
def showDashboard(request):
    model = Project
    template_name = 'HE3/dashboard.html'
    user = request.user
    projects = Project.objects.all()
    heuristicSets = SetOfHeuristics.objects.all().filter(creator = user)
    environments = Environment.objects.all().filter(creator = user)
    asmanager = projects.filter(manager=user.pk)
    asevalutor = projects.filter(evaluators=user.pk)
    now = timezone.now()
    context = {'asmanager': asmanager, 'asevalutor': asevalutor , 'heuristicSets' : heuristicSets , 'environments' :environments ,'now' : now.date()}

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
    # fields = ['title','place', 'heurPrincip', 'description', 'recommendation', 'positivity' , 'severity' ,'frequency' ]
    # success_url = reverse_lazy('profiles:dashboard:user-dashboard')
    form_class = EvaluationForm
    # form2 = modelform_factory(Screenshot, fields=['screenshot','caption'] )

    # def get(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     screenshotForm = ScreenshotForm()
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               screenshotForm=screenshotForm))
    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     screenshotForm = ScreenshotForm(self.request.POST)
    #     if (form.is_valid() and screenshotForm.is_valid() and
    #             screenshotForm.is_valid()):
    #         return self.form_valid(form, screenshotForm)
    #     else:
    #         return self.form_invalid(form, screenshotForm)

    def form_valid(self, form):
        user = self.request.user
        projectId = self.kwargs['pk']
        project = Project.objects.get(pk=projectId)
        form.instance.ofProject = project
        form.instance.evaluator = user
        # form.instance.s

        return super(EvaluationCreate, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context= super(EvaluationCreate,self).get_context_data(**kwargs)
        context['project'] = self.kwargs
        return context

    def get_form_kwargs(self):
        kwargs = super(EvaluationCreate, self ).get_form_kwargs()
        kwargs ['project_id'] = self.kwargs['pk']
        return kwargs


class EvaluationDetail(DetailView):
    model =Evaluation
    template_name = 'HE3/evaluations/evaluation_detail.html'
    context_object_name = 'evaluation'


class EvaluationUpdate(UpdateView):
    model = Evaluation
    # fields = ['title','place', 'heurPrincip', 'description', 'recommendation', 'positivity' , 'severity' ,'frequency' ]
    form_class = EvaluationFormUpdate

    def get_context_data(self, **kwargs):
        context= super(EvaluationUpdate,self).get_context_data(**kwargs)
        eval = Evaluation.objects.get(pk=self.kwargs['pk'])
        context['project'] = eval.ofProject
        return context

    def get_form_kwargs(self):
        kwargs = super(EvaluationUpdate, self ).get_form_kwargs()
        kwargs ['eval_id'] = self.kwargs['pk']
        return kwargs

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
            evaluations = allEvaluations.filter(merged=False)
            mergedEvals = allEvaluations.filter(merged=True)
        elif (self.request.user in project.evaluators.all()):
            evaluations = allEvaluations.filter(evaluator= self.request.user , merged=False)
            mergedEvals = allEvaluations.filter(evaluator= self.request.user , merged=True)

        context = { 'project' : project ,
                    'now' : timezone.now().date(),
                    'evaluations': evaluations,
                    'mergedEvals': mergedEvals,
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
    set = SetOfHeuristics.objects.get(pk=set_id)
    if request.user == set.creator :
        set.delete()

    return redirect('profiles:dashboard:user-dashboard')


# TODO convering to method with pop up effect
# class HeuristicPrinciple(CreateView):
#     model = HeuristicPrinciples
#     fields = ['title' , 'description','belongsToSet']
#     template_name = 'HE3/set/heuristicprinciples_form.html'


@login_required
def setDetail(request , set_id):
    set = SetOfHeuristics.objects.get(pk= set_id)
    princips = set.SetOfHeuristics.all()
    return render(request, template_name='HE3/set/set_detail.html' , context={'set' : set , 'princips' : princips})


@login_required
def addPrinciple(request, set_id):
    heurSet = SetOfHeuristics.objects.get(pk=set_id)

    if request.method == 'POST':
        form = Principle(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            princip = HeuristicPrinciples(title=title, description=description, belongsToSet=heurSet)
            princip.save()

    return redirect(heurSet)


@login_required
def deletePrinciple(request, p_id):

    princip = HeuristicPrinciples.objects.get(pk=p_id)

    if(request.user == princip.belongsToSet.creator):
        princip.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def updatePrinciple(request, p_id):

    princip = HeuristicPrinciples.objects.get(pk=p_id)
    if(request.user == princip.belongsToSet.creator):
        if request.method == 'POST':
            form = Principle(request.POST)
            if form.is_valid():
                princip.title = form.cleaned_data['title']
                princip.description = form.cleaned_data['description']
                princip.save()

    return redirect(request.META.get('HTTP_REFERER'))

class EnvironmentCreate(CreateView):
    model = Environment
    template_name = 'HE3/set/environment_form.html'
    fields = ['age', 'gender', 'os', 'webbrowser' , 'monitorSize', 'monitorResolustion', 'otherData']
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = user
        return super(EnvironmentCreate, self).form_valid(form)

def deleteEnvironment(request, env_id):

    env = Environment.objects.get(pk=env_id)
    if(request.user == env.creator):
        env.delete()

    return redirect('profiles:dashboard:user-dashboard')

class EnvironmentUpdate(UpdateView):
    model = Environment
    template_name = 'HE3/set/environment_form.html'
    fields = ['age', 'gender', 'os', 'webbrowser' , 'monitorSize', 'monitorResolustion', 'otherData']
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')

