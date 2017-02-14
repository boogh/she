from django.shortcuts import render,redirect
from django.views import generic
from HE3.models import Project, Evaluation
from django.core.urlresolvers import reverse_lazy
# from .forms import ProjectForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView
from django.utils import timezone
# from .tables import EvaluationsTables

#
def showDashboard(request):
    model = Project
    template_name = 'HE3/dashboard.html'
    user = request.user
    projects = Project.objects.all()
    asmanager = projects.filter(manager=user.pk)
    asevalutor = projects.filter(evaluators=user.pk)
    now = timezone.now()
    context = {'asmanager': asmanager, 'asevalutor': asevalutor , 'now' : now.date()}

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
    fields = ['name', 'link', 'description', 'deadline', 'evaluators']
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
    fields = ['name', 'link', 'description', 'deadline', 'evaluators']
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')


class EvaluationCreate(CreateView):
    model = Evaluation
    fields = ['place', 'heurPrincip', 'description', 'recommendation', 'positivity' , 'severity' ,'frequency' ]
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

class EvaluationUpdate(UpdateView):
    model = Evaluation
    fields = ['place', 'heurPrincip', 'description', 'recommendation', 'positivity' , 'severity' ,'frequency' ]

    # def form_valid(self, form):
    #     user = self.request.user
    #     projectId = self.kwargs['pk']
    #     project = Project.objects.get(pk=projectId)
    #     form.instance.ofProject = project
    #     form.instance.evaluator = user
    #
    #     return super(EvaluationUpdate, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context= super(EvaluationUpdate,self).get_context_data(**kwargs)
        context['project'] = self.kwargs
        return context

def EvaluatorDelete(request , project_id):

    user = request.user
    project = Project.objects.get(pk=project_id)
    evaluator = project.evaluators.get(pk=user.pk)
    project.evaluators.remove(evaluator)

    return redirect('profiles:dashboard:user-dashboard')


def projectDetailForEvaluator(request, project_id):
    project = Project.objects.get(pk = project_id)
    user = request.user
    evaluationsOfUser = project.evaluation_for_project.filter(evaluator = user)

    # table = EvaluationsTables(evaluationsOfUser)
    # RequestConfig(request).configure(table)

    template_name = 'HE3/project_detail_for_evaluator.html'
    context = {'now': timezone.now().date() ,'project': project ,'evaluations' :evaluationsOfUser }

    return render(request,template_name, context )

def projectDetailForManager(request, project_id):
    project = Project.objects.get(pk = project_id)
    user = request.user
    evaluations= project.evaluation_for_project.all()
    evaluators=project.evaluators.all()
    # table = EvaluationsTables(evaluationsOfUser)
    # RequestConfig(request).configure(table)

    template_name = 'HE3/project_detail.html'
    context = {'now': timezone.now().date() ,'project': project ,'evaluations' :evaluations ,'evaluators':evaluators }

    return render(request,template_name, context )