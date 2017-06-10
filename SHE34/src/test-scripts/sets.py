import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SHE34.settings.base')

import django
django.setup()

from authtools.models import User
from src.HE3.models import Project, Evaluation, SetOfHeuristics , HeuristicPrinciples
from random import choice

# class SetOfHeuristics(models.Model):
#     creator = models.ForeignKey(User , null=True)
#     title = models.CharField(max_length=500 , verbose_name='Title')
#     description = models.TextField(verbose_name='Description', blank= True)


SETCHOICES =()

HEURISTICSNIELSEN = (("1", "Visibility of System Status"),
                 ("2", "Match Between System and Real World"),
                 ("3", "User Control and Freedom"),
                 ("4", "Consistency and Standards"),
                 ("5", "Error Prevention"),
                 ("6", "Recognition Rather than Recall"),
                 ("7", "Flexibility and Efficiency of Use"),
                 ("8", "Aesthetic and Minimalistic Design"),
                 ("9", "Help Users Recognize, Diagnose, and Recover from Errors"),
                 ("10", "Help and Documentation"))