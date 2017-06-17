from django.contrib import admin
from .models import Project
from .models import Evaluation , HeuristicPrinciples ,SetOfHeuristics , Screenshots, Environment
# Register your models here.
# admin.site.register(HEset)
admin.site.register(Project)
admin.site.register(Evaluation)
admin.site.register(HeuristicPrinciples)
admin.site.register(SetOfHeuristics)
admin.site.register(Screenshots)
admin.site.register(Environment)