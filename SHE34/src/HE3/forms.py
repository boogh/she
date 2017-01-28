from django import forms
from .models import Project
from django import utils
from datetime import date,timedelta
from authtools.models import User



class ProjectForm(forms.ModelForm):
    # name = forms.CharField(max_length=40)
    # link = forms.URLField(required=False)
    # description = forms.TimeField()
    # deadline = forms.TimeField()
    # manager = forms.ForeignKey(User, widget=forms.HiddenInput() ,related_name="project_manager")
    # # HEset = models.CharField()
    # evaluators = forms.ManyToManyField(User, default=manager, related_name="project_evaluator")
    # creationTime = forms.DateField()

    class Meta:
        model = Project
        fields = ('name' ,'link' ,'description' , 'deadline')
