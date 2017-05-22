from django import forms
from .models import Project,Evaluation,SetOfHeuristics,HeuristicPrinciples
from django import utils
from datetime import date,timedelta
from authtools.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

#
# class ProjectForm(forms.ModelForm):
#     # name = forms.CharField(max_length=40)
#     # link = forms.URLField(required=False)
#     # description = forms.TimeField()
#     # deadline = forms.TimeField()
#     # manager = forms.ForeignKey(User, widget=forms.HiddenInput() ,related_name="project_manager")
#     # # HEset = models.CharField()
#     # evaluators = forms.ManyToManyField(User, default=manager, related_name="project_evaluator")
#     # creationTime = forms.DateField()
#     helper = FormHelper()
#     helper.form_method ='POST'
#     helper.add_input(Submit('submit' ,'submit' , css_class='btn-primary'))
#
#
#
#     class Meta:
#         model = Project
#         fields = ('name' ,'link' ,'description' , 'deadline', 'evaluators')

class Principle(forms.Form):
    title = forms.CharField(max_length=500 , required= True)
    description = forms.CharField(widget=forms.Textarea , required=False)

# class Evaluation_form(forms.Form):

class EvaluationForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(MyOrderForm, self).__init__(*args, **kwargs)
    #     if 'initial' in kwargs:
    #         self.fields['customer'].queryset = Customer.objects.filter(account=initial.account)

    heurPrincip = forms.ModelMultipleChoiceField(queryset= HeuristicPrinciples.objects.all())

    class Meta:
        model = Evaluation
        fields = ('title' , 'place' , 'a_place', 'tags' , 'description', 'recommendation' , 'positivity', 'severity' ,'frequency','screenshots')
        # ofProject = models.ForeignKey(Project, related_name="evaluation_for_project", verbose_name='Project')
        # evaluator = models.ForeignKey(User, related_name="evaluator", verbose_name='Evaluator')
        # heurPrincip = models.ManyToManyField(HeuristicPrinciples, related_name='heuristic_principle',
        #                                      verbose_name='Heuristic Principle', blank=True)
        # title = models.CharField(max_length=300, default='title', verbose_name='Title')
        # place = models.CharField(max_length=300, default='general')
        # a_place = models.CharField(max_length=1000, blank=True, verbose_name="Alternate Names of the Place")
        # tags = models.CharField(max_length=400, default='tags')
        # description = models.TextField()
        # recommendation = models.TextField(blank=True)
        # positivity = models.CharField(max_length=10, choices=POSITIVITY, default="n")
        # severity = models.CharField(max_length=10, choices=SEVERITY, default="1")
        # frequency = models.CharField(max_length=10, choices=FREQUENCY, default="1")
        # screenshots = models.ManyToManyField(Screenshot, blank=True, name="screenshots", related_name="screenshots")