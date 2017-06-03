from django import forms
from django.forms import inlineformset_factory
from .models import Project,Evaluation,SetOfHeuristics,HeuristicPrinciples , Screenshots
from django import utils
from datetime import date,timedelta
from authtools.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Button, Layout , ButtonHolder,HTML,Field

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

class EvaluationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('project_id' , None)
        super(EvaluationForm, self).__init__(*args, **kwargs)
        project = Project.objects.get(pk=pk)
        princips = project.setOfHeuristics.SetOfHeuristics.all()
        self.fields['heurPrincip'].queryset = princips

    class Meta:
        model = Evaluation
        fields = ('title' , 'place' , 'a_place','link' ,'tags' , 'description', 'recommendation' , 'positivity', 'severity' ,'frequency','heurPrincip', 'screenshot','caption' )


# class MergedEvaluationForm(EvaluationForm):
#     pass

class EvaluationFormUpdate(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('eval_id' , None)
        super(EvaluationFormUpdate, self).__init__(*args, **kwargs)
        eval = Evaluation.objects.get(pk=pk)
        princips = eval.ofProject.setOfHeuristics.SetOfHeuristics.all()
        self.fields['heurPrincip'].queryset = princips

    class Meta:
        model = Evaluation
        fields = ('title' , 'place' , 'a_place','link' ,'tags' , 'description', 'recommendation' , 'positivity', 'severity' ,'frequency','heurPrincip', 'screenshot' ,'caption' )

class MergeEvaluationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop('eval_id' , None)
        super(MergeEvaluationForm, self).__init__(*args, **kwargs)
        eval = Evaluation.objects.get(pk=pk)
        princips = eval.ofProject.setOfHeuristics.SetOfHeuristics.all()
        self.fields['heurPrincip'].queryset = princips
        self.fields['merdedFromEvaluators'].queryset = eval.ofProject.evaluators
        self.fields['mergedScreenshots'].queryset = eval.mergedScreenshots.all()
        print('screenshots: ' , eval.mergedScreenshots.count())

    class Meta:
        model = Evaluation
        fields = ('title' , 'place' , 'a_place', 'description', 'recommendation' , 'positivity', 'severity' ,'frequency','heurPrincip' , 'merdedFromEvaluators', 'mergedScreenshots' )
        widgets = {
            'mergedScreenshots' : forms.CheckboxSelectMultiple()
        }

# class MergeEvaluationForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         pk = kwargs.pop('eval_id' , None)
#         super(MergeEvaluationForm, self).__init__(*args, **kwargs)
#         eval = Evaluation.objects.get(pk=pk)
#         princips = eval.ofProject.setOfHeuristics.SetOfHeuristics.all()
#         self.fields['heurPrincip'].queryset = princips
#         self.fields['merdedFromEvaluators'].queryset = eval.ofProject.evaluators
#         self.fields['mergedScreenshots'].queryset = eval.mergedScreenshots.all()
#
#         self.helper = FormHelper(self)
#
#         url = """<a class="btn btn-warning" href={% url "profiles:dashboard:evaluation-detail" """ + str(
#             pk) + """%}>Cancel</a>"""
#         layout = Layout(ButtonHolder(
#             Submit('Save', 'Save'),
#             HTML(url),
#
#         ))
#
#         self.helper.layout.insert(18,layout)
#
#
#     class Meta:
#         model = Evaluation
#         fields = ('title' , 'place' , 'a_place', 'description', 'recommendation' , 'positivity', 'severity' ,'frequency','heurPrincip' , 'merdedFromEvaluators', 'mergedScreenshots' )
#         widgets = {
#             'mergedScreenshots' : forms.CheckboxSelectMultiple()
#         }

# class EvaluationFormUpdate(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         pk = kwargs.pop('eval_id' , None)
#         super(EvaluationFormUpdate, self).__init__(*args, **kwargs)
#         eval = Evaluation.objects.get(pk=pk)
#         princips = eval.ofProject.setOfHeuristics.SetOfHeuristics.all()
#         self.fields['heurPrincip'].queryset = princips
#         self.helper = FormHelper(self)
#         url = """<a class="btn btn-warning" href={% url "profiles:dashboard:evaluation-detail" """+ str(pk)+ """%}>Cancel</a>"""
#
#         layout = Layout(ButtonHolder(
#             Submit('Save' , 'Save'),
#             HTML(url),
#         ))
#         self.helper.layout.insert(15,layout)
#         # self.helper.layout = Layout(
#         #     Div(
#         #         Submit('save', 'save', css_class='btn btn-primary'),
#         #         css_class='col-lg-offset-3 col-lg-9',
#         #         # Button('cancel', 'Cancel', css_class='btn-default',)
#         #     )
#         # )
#
#     class Meta:
#         model = Evaluation
#         fields = ('title' , 'place' , 'a_place','link' ,'tags' , 'description', 'recommendation' , 'positivity', 'severity' ,'frequency','heurPrincip', 'screenshot' ,'caption' )