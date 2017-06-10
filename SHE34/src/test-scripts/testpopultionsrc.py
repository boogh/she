import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SHE34.settings.base')

import django
django.setup()

from authtools.models import User
from src.HE3.models import Project, Evaluation, SetOfHeuristics , HeuristicPrinciples
from random import choice

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



def populate():
    user_items=[{'email': 'user1@user1.com', 'password': 'user1', 'name': 'user1'},
                {'email': 'user2@user2.com', 'password': 'user2', 'name': 'user2'},
                {'email': 'user3@user3.com', 'password': 'user3', 'name': 'user3'},
                {'email': 'user4@user4.com', 'password': 'user4', 'name': 'user4'},
                {'email': 'user5@user5.com', 'password': 'user5', 'name': 'user5'},
                {'email': 'user6@user6.com', 'password': 'user6', 'name': 'user6'},
                {'email': 'user7@user7.com', 'password': 'user7', 'name': 'user7'},
                {'email': 'user8@user8.com', 'password': 'user8', 'name': 'user8'},]


    setdata = [ { 'title' : 'Default-set' , 'disc' : 'Nielson Heuristic Principles'}]

    for user in user_items:
        addUser(user)

    for set in setdata:
        addSetHE(set , HEURISTICLIST)

    default_set = SetOfHeuristics.objects.get(title='Default-set')

    project_items = [
        {'name': 'p1', 'description': ' This is project 1', 'manager': 'user1',
                      'setOfHeuristics': default_set,
                      'evaluator': ['user2', 'user3', 'user4', 'user5', 'user1', 'user6', 'user7', 'user8']},
                     {'name': 'p2', 'description': ' This is project 2', 'manager': 'user2',
                      'setOfHeuristics': default_set,
                      'evaluator': ['user2', 'user3', 'user4', 'user5', 'user1', 'user6', 'user7', 'user8']},
                     {'name': 'p3', 'description': ' This is project 3', 'manager': 'user3',
                      'setOfHeuristics': default_set,
                      'evaluator': ['user1', 'user2', 'user4', 'user5']},
                     {'name': 'p4', 'description': ' This is project 4', 'manager': 'user4',
                      'setOfHeuristics': default_set,
                      'evaluator': ['user1', 'user2', 'user3', 'user5']},
                     {'name': 'p5', 'description': ' This is project 5', 'manager': 'user1',
                      'setOfHeuristics': default_set,
                      'evaluator': ['user2', 'user3', 'user4', 'user5']},
                     {'name': 'p6', 'description': ' This is project 6', 'manager': 'user2',
                      'setOfHeuristics': default_set,
                      'evaluator': ['user1', 'user3', 'user4', 'user5']},
                     {'name': 'p7', 'description': ' This is project 7', 'manager': 'user1',
                      'setOfHeuristics': default_set,
                      'evaluator': ['user2', 'user3', 'user4', 'user5']},
                     ]



    for project in project_items:
        addProject(project)

    listOfHE = default_set.SetOfHeuristics.all()


    eval_items = [
        {'ofProject': 'p1',
                       'evaluator': 'user2',
                       'place': '',
                       'heurPrincip': choice(listOfHE),
                       'description': 'This is an evaluation for project 1',
                       'recommendation': '',
                       'positivity': '',
                       'severity': '',
                       'frequency': '',
                       'screenshot': ''},
                      {'ofProject': 'p1',
                       'evaluator': 'user2',
                       'place': '',
                       'heurPrincip': choice(listOfHE),
                       'description': 'This is an evaluation for project 1',
                       'recommendation': '',
                       'positivity': '',
                       'severity': '',
                       'frequency': '',
                       'screenshot': ''},
                      {'ofProject': 'p1',
                       'evaluator': 'user3',
                       'place': '',
                       'heurPrincip': choice(listOfHE),
                       'description': 'This is an evaluation for project 1',
                       'recommendation': '',
                       'positivity': '',
                       'severity': '',
                       'frequency': '',
                       'screenshot': ''},
                      {'ofProject': 'p1',
                       'evaluator': 'user2',
                       'place': '',
                       'heurPrincip': choice(listOfHE),
                       'description': 'This is an evaluation for project 1',
                       'recommendation': '',
                       'positivity': '',
                       'severity': '',
                       'frequency': '',
                       'screenshot': ''},
                      ]

    for eval in eval_items:
        addEvaluation(eval)



def addSetHE(setdata , setitems):
    set , create = SetOfHeuristics.objects.get_or_create(creator=User.objects.get(name='user1'),title=setdata['title'] , discription=setdata['disc'])
    for item in setitems :
        title = item[0]+'- '+item[1]
        princip , create = HeuristicPrinciples.objects.get_or_create(belongsToSet = set , title = title )

    print('Added a set!')
    return set


def addUser(userdata):
    user = User.objects.get_or_create(email=userdata['email'] , name=userdata['name'])[0]
    user.set_password(userdata['password'])
    user.save()
    print("Added User")

def addProject(projectData):
    project,create = Project.objects.get_or_create(name=projectData['name'], description = projectData['description'], setOfHeuristics= projectData['setOfHeuristics'],
                                            manager=User.objects.get(name=projectData['manager']))
    project.save()
    for evaluator in projectData['evaluator']:
        project.evaluators.add(User.objects.get(name=evaluator))
    project.save()
    print('Added a Project')


def addEvaluation(eval):
    evaluation  = Evaluation(ofProject= Project.objects.get(name=eval['ofProject']),
                                                   evaluator = User.objects.get(name=eval['evaluator']),
                                                   description= eval['description'],
                                                   heurPrincip =eval['heurPrincip'])
    evaluation.save()
    print('Added a Evaluation')

if __name__ == '__main__':
    print('Running population script...')
    populate()