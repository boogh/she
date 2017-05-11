from django import forms
from .models import Project,SetOfHeuristics,HeuristicPrinciples
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

# class HeSet(forms.Form):
#
#     title = forms.CharField(max_length=500 , required= True)
#     description = forms.CharField(widget=forms.Textarea , required=False)

# class Evaluation_form(forms.Form):
