import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SHE34.settings.base')

import django
django.setup()

from authtools.models import User
from HE3.models import Project, Evaluation, SetOfHeuristics , HeuristicPrinciples

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




HEURISTICSNIELSEN_10 =[{'title': '1- Visibility of System Status' , 'description' :'The system should always keep users informed about what is going on, through appropriate feedback within reasonable time.'},
                       {'title': '2- Match Between System and Real World', 'description': "The system should speak the users' language, with words, phrases and concepts familiar to the user, rather than system-oriented terms. Follow real-world conventions, making information appear in a natural and logical order."},
                       {'title': '3- User Control and Freedom', 'description': 'Users often choose system functions by mistake and will need a clearly marked "emergency exit" to leave the unwanted state without having to go through an extended dialogue. Support undo and redo.'},
                       {'title': '4- Consistency and Standards', 'description': 'Users should not have to wonder whether different words, situations, or actions mean the same thing. '},
                       {'title': '5- Error Prevention', 'description': 'Even better than good error messages is a careful design which prevents a problem from occurring in the first place. Either eliminate error-prone conditions or check for them and present users with a confirmation option before they commit to the action.'},
                       {'title': '6- Recognition Rather than Recall', 'description': "Minimize the user's memory load by making objects, actions, and options visible. The user should not have to remember information from one part of the dialogue to another. Instructions for use of the system should be visible or easily retrievable whenever appropriate."},
                       {'title': '7- Flexibility and Efficiency of Use' , 'description' :'Accelerators (unseen by the novice user ) may often speed up the interaction for the expert user such that the system can cater to both inexperienced and experienced users. Allow users to tailor frequent actions.'},
                       {'title': '8- Aesthetic and Minimalistic Design' , 'description' :'Dialogues should not contain information which is irrelevant or rarely needed. Every extra unit of information in a dialogue competes with the relevant units of information and diminishes their relative visibility.'},
                       {'title': '9- Help Users Recognize, Diagnose, and Recover from Errors' , 'description' :'Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.'},
                       {'title': '10- Help and Documentation' , 'description' :"Even though it is better if the system can be used without documentation, it may be necessary to provide help and documentation. Any such information should be easy to search, focused on the user's task, list concrete steps to be carried out, and not be too large."},
                       ]
SCHNEIDERMAN=[{'title': "1- Strive for consistency" , 'description' : "Consistent sequences of actions should be required in similar situations; identical terminology should be used in prompts, menus, and help screens; and consistent commands should be employed throughout."},
              {'title': "2- Enable frequent users to use shortcuts", 'description': "As the frequency of use increases, so do the user's desires to reduce the number of interactions and to increase the pace of interaction. Abbreviations, function keys, hidden commands, and macro facilities are very helpful to an expert user."},
              {'title': "3- Offer informative feedback", 'description': "For every operator action, there should be some system feedback. For frequent and minor actions, the response can be modest, while for infrequent and major actions, the response should be more substantial."},
              {'title': "4- Design dialog to yield closure", 'description': "Sequences of actions should be organized into groups with a beginning, middle, and end. The informative feedback at the completion of a group of actions gives the operators the satisfaction of accomplishment, a sense of relief, the signal to drop contingency plans and options from their minds, and an indication that the way is clear to prepare for the next group of actions."},

              {'title': "5- Offer simple error handling", 'description': "As much as possible, design the system so the user cannot make a serious error. If an error is made, the system should be able to detect the error and offer simple, comprehensible mechanisms for handling the error."},
              {'title': "6- Permit easy reversal of actions", 'description': "This feature relieves anxiety, since the user knows that errors can be undone; it thus encourages exploration of unfamiliar options. The units of reversibility may be a single action, a data entry, or a complete group of actions."},
              {'title': "7- Support internal locus of control", 'description': "Experienced operators strongly desire the sense that they are in charge of the system and that the system responds to their actions. Design the system to make users the initiators of actions rather than the responders."},
              {'title': "8- Reduce short-term memory load", 'description': "The limitation of human information processing in short-term memory requires that displays be kept simple, multiple page displays be consolidated, window-motion frequency be reduced, and sufficient training time be allotted for codes, mnemonics, and sequences of actions. "},
              ]

setItems=[
    {'title' : 'Nielsen Heuristics',
     'description':"Jakob Nielsen's 10 general principles for interaction design. They are called 'heuristics' because they are broad rules of thumb and not specific usability guidelines.",
     'principles' : HEURISTICSNIELSEN_10},
    {'title' : 'Scheiderman Eight Golden Rules of ID',
     'description':'These rules were obtained from the text Designing the User Interface by Ben Shneiderman. Shneiderman proposed this collection of principles that are derived heuristically from experience and applicable in most interactive systems after being properly refined, extended, and interpreted.',
     'principles': SCHNEIDERMAN},
    # {'title' : ' 15 Heuristics of Muller and McClard ', 'description':''},
        ]

def addUser():
    user = User.objects.get_or_create(email='admin_set@admin_set.com' , name='admin_set')[0]
    user.set_password('admin_set_313')
    user.save()
    print("Added admin_set!")
    return user.pk


def addSet(setItems ,user_pk):
    for item in setItems:
        set, create = SetOfHeuristics.objects.get_or_create(creator=User.objects.get(pk=user_pk), title=item['title'],
                                                            description=item['description'])
        print('added ' , set.title)
        for princip in item['principles']:
            print('now reading the p-items... : ' )
            princip, create = HeuristicPrinciples.objects.get_or_create(belongsToSet=set, title=princip['title'] , description = princip['description'])
            print('added principle' , princip)

        # print('Added a set!')
def populate():

    addSet(setItems, addUser() )

if __name__ == '__main__':
    print('Running population script for sets...')
    populate()

# class SetOfHeuristics(models.Model):
#     creator = models.ForeignKey(User , null=True)
#     title = models.CharField(max_length=500 , verbose_name='Title')
#     description = models.TextField(verbose_name='Description', blank= True)
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return reverse('profiles:dashboard:set-detail', kwargs={'set_id': self.pk})
#
# class HeuristicPrinciples(models.Model):
#     belongsToSet = models.ForeignKey(SetOfHeuristics , related_name= 'SetOfHeuristics')
#     title = modcels.CharField(max_length=500 , verbose_name='Heuristic Principle' )
#     description = models.TextField(blank= True , verbose_name='Description' ,help_text='This description is used as a hint for the principle')
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return reverse('profiles:dashboard:set-detail', kwargs={'set_id': self.belongsToSet.pk})
