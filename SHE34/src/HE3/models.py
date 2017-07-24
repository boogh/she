from django.db import models
from authtools.models import User
from datetime import date,timedelta
from django import utils
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField



HEURISTICLIST = (("1", "Visibility of System Status"),
                 ("2", "Match Between System and Real World"),
                 ("3", "User Control and Freedom"),
                 ("4", "Consistency and Standards"),
                 ("5", "Error Prevention"),
                 ("6", "Recognition Rather than Recall"),
                 ("7", "Flexibility and Efficiency of Use"),
                 ("8", "Aesthetic and Minimalistic Design"),
                 ("9", "Help Users Recognize, Diagnose, and Recover from Errors"),
                 ("10", "Help and Documentation"))

POSITIVITY= (("p" , "Positive") , ("n" , "Negative"))
SEVERITY= (("1" , "No problem at all"), ("2", "Cosmetic problem"), ("3" , "Minor usability problem") , ("4", "Major usability problem"), ("5", "Catastrophic"))
FREQUENCY=(("1", "almost never"), ("2", "rarely (< 10 % )") , ("3", "occasionally (11-50 %"), ("4" , "regularly(51-89 %"), ("5" , "constantly (>90 %"))



# class HEset(models.Model):
#     HEURISTICLIST = (("1" , "Visibility of System Status"),
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
#     set = models.CharField(max_length=200 , choices=HEURISTICLIST)
#
#     def __str__(self):
#         return self.name

class SetOfHeuristics(models.Model):
    creator = models.ForeignKey(User , null=True)
    title = models.CharField(max_length=500 , verbose_name='Title')
    description = models.TextField(verbose_name='Description', blank= True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('profiles:dashboard:set-detail', kwargs={'set_id': self.pk})

class HeuristicPrinciples(models.Model):
    belongsToSet = models.ForeignKey(SetOfHeuristics , related_name= 'SetOfHeuristics')
    title = models.CharField(max_length=500 , verbose_name='Heuristic Principle' )
    description = models.TextField(blank= True , verbose_name='Description' ,help_text='This description is used as a hint for the principle')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('profiles:dashboard:set-detail', kwargs={'set_id': self.belongsToSet.pk})

class Screenshots(models.Model):
        # ofEvaluation = models.ForeignKey(Evaluation , related_name='screenshot_of_evaluation')
    caption = models.CharField(max_length=1000, blank=True)
    screenshot = ThumbnailerImageField(verbose_name="Screenshot", upload_to='screenshots/%Y-%m-%d/')

    # def thumbnail(self):
    #     return render_to_string('HE3/thumbnail.html', {'image': self})

    def __str__(self):
        if self.screenshot:
            return  "" + self.screenshot['big'].url
        else:
            return 'Screenshot' + str (self.id) + " : "



class Project(models.Model):
    manager = models.ForeignKey(User)
    setOfHeuristics = models.ForeignKey(SetOfHeuristics,related_name='project_SetOfHeuristics' , verbose_name='Set of Heuristic principles')
    evaluators = models.ManyToManyField(User, related_name="project_evaluator")
    name = models.CharField(max_length=40)
    link = models.URLField(blank=True , help_text="Example: http://www.example.com")
    description = models.TextField()
    creationTime = models.DateField(auto_now_add=True)
    deadline = models.DateField(default= date.today() + timedelta(days=15))

    class Meta:
        ordering =['manager' , 'name' , '-creationTime']
    def __str__(self):
        return self.name


    # def __iter__(self):
    #     return [self.name,
    #             self.link,
    #             self.description,
    #             self.manger,
    #             self.evaluators,
    #             self.creationTime,
    #             self.deadline,
    #            ]

class Evaluation(models.Model):
    POSITIVITY = (("p", "Positive"), ("n", "Negative"))
    SEVERITY = (("1", "No problem at all"), ("2", "Cosmetic problem"), ("3", "Minor usability problem"),
                ("4", "Major usability problem"), ("5", "Catastrophic"))
    FREQUENCY = (("1", "almost never"), ("2", "rarely (< 10 % )"), ("3", "occasionally (11-50 %)"), ("4", "regularly(51-89 %)"),
    ("5", "constantly (>90 %)"))

    ofProject= models.ForeignKey(Project,related_name="evaluation_for_project" , verbose_name='Project')
    evaluator = models.ForeignKey(User,related_name="evaluator" , verbose_name='Evaluator')
    heurPrincip= models.ManyToManyField(HeuristicPrinciples, related_name='heuristic_principle', verbose_name='Heuristic Principle', blank=True )
    title = models.CharField(max_length=300 ,verbose_name='Title' )
    place = models.CharField(max_length=300)
    # a_place = models.CharField(max_length=1000 , blank= True ,verbose_name="Alternate Names of the Place")
    link = models.URLField(blank=True , verbose_name= 'Link', help_text='The link of the page to which evaluation refers, example: http://www.example.com')
    tags = models.CharField(max_length=400, blank=True , help_text= 'Keywords of this evaluation')
    description = models.TextField()
    recommendation= models.TextField(blank=True)
    positivity = models.CharField(max_length=10, choices=POSITIVITY, default="n")
    severity = models.CharField(max_length=10, choices=SEVERITY, default="1")
    frequency = models.CharField(max_length=10, choices=FREQUENCY, default="1")
    screenshot = ThumbnailerImageField(blank=True ,upload_to='screenshots/%Y-%m-%d/')
    # caption = models.CharField(blank=True , max_length=1000, help_text='Enter a caption for the screenshot')

    # Fiels for merged evaluations
    merged = models.BooleanField(default=False)
    merdedFromEvaluators = models.ManyToManyField(User, related_name='fromEvaluators' , blank=True,null=True, verbose_name='Evaluators',help_text='Evaluators who found this issue')
    mergedFromEvaluations = models.ManyToManyField('self' ,verbose_name='Merged-From-Evaluations', related_name='fromEvaluations' , blank=True , null=True )
    mergedScreenshots = models.ManyToManyField(Screenshots ,blank=True , null= True, verbose_name="Merged-Screenshots" , related_name="screenshots" )

    class Meta:
        ordering= ['evaluator', 'place' , '-severity' ]

    def get_absolute_url(self):

        if self.merged == True:
            return reverse('merge:merge-project-desktop', kwargs={'project_id': self.ofProject.pk})
        return reverse('profiles:dashboard:project_detail', kwargs={'pk': self.ofProject.pk})


    def __str__(self):
        return self.title +' - place = ' + self.place + ' - from = ' + self.evaluator.name

# Name should be refactored to MergeLists
# class ListOfEval(models.Model):
#     ofProject = models.ForeignKey(Project)
#     fromUser = models.ForeignKey(User, related_name="Merge_manager")
#     evaluations = models.ManyToManyField(Evaluation , blank= True)
#     name = models.CharField(max_length= 50)
#
#     # these two should be deleted
#     mergeUrl = models.URLField(blank=True , null=True)
#     exportedFile= models.FileField(blank=True , null=True)
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('profiles:dashboard:project_detail', kwargs={'pk': self.ofProject.pk})

class Environment(models.Model):

    GENDER = (('1' , 'Male') , ('2' , 'Female') , ('3' , 'Other'))

    creator = models.ForeignKey(User, related_name= 'creator')
    age = models.IntegerField( verbose_name='Age' , blank=True , help_text='Enter your age')
    gender = models.CharField(max_length=15 , verbose_name='Gender' , blank=True  , choices=GENDER , help_text= 'Enter your gender')
    webbrowser = models.CharField(max_length= 100 , verbose_name='Webbrowser',blank=True, help_text='Types of webbrowser used for evaluation' )
    os = models.CharField(max_length=100 , verbose_name='Operation system' ,blank=True, help_text= 'Types of operation systems used in evaluation process, like windows and osx ...' )
    monitorSize = models.CharField(max_length=100 , verbose_name= 'Monitor size' ,blank=True, help_text='Size of monitor used in evaluation process')
    monitorResolution = models.CharField(max_length=100 , verbose_name='Monitor Resolution' ,blank=True, help_text='Resolution of the monitur used in evaluation process')
    otherData = models.CharField(max_length=500 , verbose_name='Other Relevant Data' ,blank=True, help_text='Enter other data related to environment involved in evaluation process')

