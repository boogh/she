from django.db import models
from authtools.models import User
from datetime import datetime
# Create your models here.

#
# class HEset(models.Model):
#     setList = (("1" , "Visibility of System Status"),
#                 ("2" , "Match Between System and Real World"),
#                 ("3","User Control and Freedom"),
#                 ("4","Consistency and Standards"),
#                 ("5", "Error Prevention"),
#                 ("6", "Recognition Rather than Recall"),
#                 ("7", "Flexibility and Efficiency of Use"),
#                 ("8", "Aesthetic and Minimalistic Design"),
#                 ("9", "Help Users Recognize, Diagnose, and Recover from Errors"),
#                 ("10", "Help and Documentation"))
#
#
#     name = models.CharField(max_length=50)
#     set = models.CharField(max_length=200 , choices=setList)
#
#     def __str__(self):
#         return self.name


class Project(models.Model):
    setList = (("1", "Visibility of System Status"),
               ("2", "Match Between System and Real World"),
               ("3", "User Control and Freedom"),
               ("4", "Consistency and Standards"),
               ("5", "Error Prevention"),
               ("6", "Recognition Rather than Recall"),
               ("7", "Flexibility and Efficiency of Use"),
               ("8", "Aesthetic and Minimalistic Design"),
               ("9", "Help Users Recognize, Diagnose, and Recover from Errors"),
               ("10", "Help and Documentation"))

    name = models.CharField(max_length=40)
    link = models.URLField(blank=True)
    place = models.CharField(max_length=100 , default='general')
    description = models.TextField()
    manager = models.ForeignKey(User,related_name="project_manager")
    HE_Principle = models.CharField(max_length=300, choices= setList ,default="1")
    evaluators = models.ManyToManyField(User, default=manager, related_name="project_evaluator")
    # deadline = models.DateField(default=time.date())
    # creationTime = models.DateField(default=time.date())

    def __str__(self):
        return self.name

# class Evaluation(models.Model):
#     posOrNeg= (("p" , "Positive") , ("n" , "Negative"))
#     severityList= (("1" , "No problem at all"), ("2","Cosmetic problem"),("3" ,"Minor usability problem") ,("4","Major usability problem"),("5","Catastrophic"))
#     freq=(("1","almost never"),("2","rarely (< 10 % )") ,("3", "occasionally (11-50 %"),("4" ,"regularly(51-89 %"), ("5" , "constantly (>90 %"))
#     for_project= models.ForeignKey(Project,related_name="evaluation_for_this_project",on_delete=models.CASCADE)
#     evaluator = models.ForeignKey(Profile,related_name="evaluator",on_delete=models.CASCADE)
#     heurPrincip= models.CharField(max_length=200)
#     description = models.TextField()
#     recommendation= models.TextField(blank=True)
#     positivity = models.CharField(max_length=10, choices=posOrNeg , default="n")
#     severity = models.CharField(max_length=10 , choices=severityList,default="1")
#     frequency = models.CharField(max_length=10,choices=freq ,default="1")
#     screenshot = models.ImageField(name="Screenshot" , upload_to='screenshots/%Y-%m-%d/',
#                                 null=True,
#                                 blank=True)
#
#
#
# class ListOfEvaluations(models.Model):
#     name = models.CharField(max_length= 50)
#     ofProject = models.ForeignKey(Project)
#     fromUser= models.ForeignKey(Profile , related_name="project_manager")
#     evaluations = models.ManyToManyField(Evaluation)
#
#     def __str__(self):
#         return self.name