from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template,Context
from django.views import generic
from HE3.models import Project
from django.core.urlresolvers import reverse_lazy
# from django.contrib.auth.mixins import LoginRequiredMixin
# from HE3.forms import ProjectForm

from django.views.generic.edit import CreateView,UpdateView,DeleteView
#
def showDashboard(request):
    model = Project
    template_name = 'HE3/dashboard.html'
    user = request.user
    projects = Project.objects.all()
    asmanager = projects.filter(manager=user.pk)
    asevalutor = projects.filter(evaluators =user.pk)
    context ={'asmanager' : asmanager , 'asevalutor' : asevalutor}

    return render(request, template_name,context)


class ProjectDetail(generic.detail.DetailView):
    model = Project
    template_name = 'HE3/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)

        return context

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

# def addProject(request):

class ProjectCreate(CreateView):
    model = Project
    fields = ['name' ,'link','description','deadline','evaluators']
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')

    def form_valid(self, form):
        user = self.request.user
        form.instance.manager =user
        return super(ProjectCreate,self).form_valid(form)

class ProjectUpdate(UpdateView):
    model = Project
    fields = ['name' ,'link','description','deadline','evaluators']
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')

class ProjectDelete(DeleteView):
    model =Project
    success_url = reverse_lazy('profiles:dashboard:user-dashboard')